"""Pre-commit guard (NFR-06, CP-0a D-D R6): no dataset files in the repo.

Fails if any given path is under ``data/`` (public datasets live in gitignored ``data/external/``)
or is a ``.parquet`` / ``.csv`` file larger than 1 MB. Paths come from pre-commit as arguments;
with no arguments there is nothing to check. Standard library only.
"""

from __future__ import annotations

import sys
from pathlib import Path, PurePosixPath

MAX_DATA_FILE_BYTES = 1_000_000  # 1 MB
DATA_SUFFIXES = frozenset({".parquet", ".csv"})


def problems(paths: list[str]) -> list[str]:
    """Return one message per offending path."""
    found: list[str] = []
    for raw in paths:
        posix = PurePosixPath(raw.replace("\\", "/"))
        if posix.parts and posix.parts[0] == "data":
            found.append(f"{raw}: files under data/ must not be committed (D-D R6)")
            continue
        path = Path(raw)
        if posix.suffix.lower() in DATA_SUFFIXES and path.is_file():
            size = path.stat().st_size
            if size > MAX_DATA_FILE_BYTES:
                found.append(f"{raw}: {size} bytes > 1 MB data file (use data/external/, D-D R6)")
    return found


def main(argv: list[str]) -> int:
    found = problems(argv)
    for message in found:
        print(message, file=sys.stderr)
    if not argv:
        print("check_large_files: no files given, nothing to check")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
