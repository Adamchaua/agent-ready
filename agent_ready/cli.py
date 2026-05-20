from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .generator import write_outputs
from .scanner import scan


def main() -> int:
    parser = argparse.ArgumentParser(description="Make a repo ready for AI coding agents.")
    parser.add_argument("path", nargs="?", default=".", help="repository path to scan")
    parser.add_argument("--write", action="store_true", help="write AGENTS.md, CLAUDE.md, CODEX.md and .agent files")
    parser.add_argument("--force", action="store_true", help="overwrite existing generated files")
    parser.add_argument("--json", action="store_true", help="print JSON summary")
    parser.add_argument("--version", action="store_true", help="print version")
    args = parser.parse_args()

    if args.version:
        print(__version__)
        return 0

    root = Path(args.path).resolve()
    summary = scan(root)

    if args.write:
        written = write_outputs(root, summary, force=args.force)
        for path in written:
            print(f"wrote {path.relative_to(root)}")
        if not written:
            print("no files written; use --force to overwrite existing generated files")

    if args.json or not args.write:
        print(json.dumps(summary.to_dict(), indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
