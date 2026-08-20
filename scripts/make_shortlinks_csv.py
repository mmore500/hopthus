#!/usr/bin/env python3
"""Concatenate YAML frontmatter from all Jekyll posts into one CSV table."""

import csv
import re
import sys
from pathlib import Path

import frontmatter

POST_GLOB = "**/_posts/*.md"
OUTPUT_PATH = "shortlinks.csv"

SLUG_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-(.+)\.md$")


def slug_key(path: Path) -> str:
    match = SLUG_RE.match(path.name)
    if not match:
        raise ValueError(f"filename does not match YYYY-MM-DD-<key>.md: {path}")
    return match.group(1)


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    paths = sorted(repo_root.glob(POST_GLOB))

    rows = [
        {
            "file": str(path.relative_to(repo_root)),
            "shortlink_key": slug_key(path),
            **frontmatter.load(path).metadata,
        }
        for path in paths
    ]

    all_keys = {key for row in rows for key in row}
    fieldnames = sorted(all_keys)
    rows.sort(key=lambda r: r["file"])

    with open(repo_root / OUTPUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to {OUTPUT_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
