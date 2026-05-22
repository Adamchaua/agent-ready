from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .generator import stale_outputs, write_outputs
from .scanner import scan
from .score import calculate_score


def main() -> int:
    parser = argparse.ArgumentParser(description="Make a repo ready for AI coding agents.")
    parser.add_argument("path", nargs="?", default=".", help="repository path to scan")
    parser.add_argument(
        "--write",
        action="store_true",
        help="write AGENTS.md, CLAUDE.md, CODEX.md and .agent files",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero when generated agent files are missing or stale",
    )
    parser.add_argument("--force", action="store_true", help="overwrite existing generated files")
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        help="extra directory path to skip; repeat as needed",
    )
    parser.add_argument("--json", action="store_true", help="print JSON summary")
    parser.add_argument("--score", action="store_true", help="print agent-readiness score")
    parser.add_argument("--version", action="store_true", help="print version")
    args = parser.parse_args()

    if args.version:
        print(__version__)
        return 0

    root = Path(args.path).resolve()
    summary = scan(root, extra_ignores=args.ignore)

    if args.check:
        stale = stale_outputs(root, summary)
        if stale:
            print("agent-ready files are missing or stale:")
            for path in stale:
                print(f"- {path.relative_to(root)}")
            print("run: agent-ready . --write --force")
            return 1
        print("agent-ready files are current")

    if args.write:
        written = write_outputs(root, summary, force=args.force)
        for path in written:
            print(f"wrote {path.relative_to(root)}")
        if not written:
            print("no files written; use --force to overwrite existing generated files")

    if args.json or (not args.write and not args.check and not args.score):
        payload = summary.to_dict()
        if args.score:
            payload["readiness"] = calculate_score(summary).to_dict()
        print(json.dumps(payload, indent=2))
    elif args.score:
        readiness = calculate_score(summary)
        print(f"agent-readiness: {readiness.score}/100 ({readiness.grade})")
        for recommendation in readiness.recommendations:
            print(f"- {recommendation}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
