"""Traceability check (spec §4.10, §17.1 step 11; DECISIONS T04).

Validates ``docs/traceability.csv``:

* header is exactly ``requirement_id,priority,story_id,design_section,task_ids,test_ids``;
* ``requirement_id`` is unique and matches ``FR-NN`` / ``NFR-NN`` (optional lowercase suffix);
* ``priority`` is one of MUST, SHOULD, COULD;
* every ``test_ids`` entry (``;``-separated, ``path`` or ``path::test_name``) names a file that
  exists relative to the repository root -- a missing file is an ERROR;
* a MUST row without tests is a WARNING by default and an ERROR with ``--strict``.

Phasing (DECISIONS T04): CI runs warn mode through P1 and switches to ``--strict`` from P2.
Exit code 1 on any ERROR, else 0. Under GitHub Actions (``GITHUB_ACTIONS=true``) findings are also
emitted as ``::warning::`` / ``::error::`` annotations. Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

EXPECTED_HEADER = (
    "requirement_id",
    "priority",
    "story_id",
    "design_section",
    "task_ids",
    "test_ids",
)
REQUIREMENT_ID_RE = re.compile(r"^(FR|NFR)-\d{2}[a-z]?$")
PRIORITIES = ("MUST", "SHOULD", "COULD")
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = REPO_ROOT / "docs" / "traceability.csv"

_COL_ID = EXPECTED_HEADER.index("requirement_id")
_COL_PRIORITY = EXPECTED_HEADER.index("priority")
_COL_TESTS = EXPECTED_HEADER.index("test_ids")


@dataclass
class Report:
    """Result of :func:`check`."""

    errors: list[str] = field(default_factory=list[str])
    warnings: list[str] = field(default_factory=list[str])
    by_priority: dict[str, int] = field(default_factory=dict[str, int])
    must_with_tests: int = 0
    must_without_tests: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors


def split_test_ids(cell: str) -> list[str]:
    """Split a ``test_ids`` cell into non-empty, stripped entries."""
    return [part.strip() for part in cell.split(";") if part.strip()]


def file_of_test_id(test_id: str) -> str:
    """Return the file part of ``path`` or ``path::test_name``."""
    return test_id.split("::", 1)[0].strip()


def _check_test_ids(line: int, req_id: str, cell: str, repo_root: Path, report: Report) -> int:
    """Validate one row's test ids; return how many entries it has."""
    entries = split_test_ids(cell)
    for entry in entries:
        rel = file_of_test_id(entry)
        posix = PurePosixPath(rel.replace("\\", "/"))
        if not rel or posix.is_absolute() or ".." in posix.parts:
            report.errors.append(
                f"line {line}: {req_id}: test id {entry!r} must be a repo-relative path"
            )
            continue
        if not (repo_root / posix).is_file():
            report.errors.append(f"line {line}: {req_id}: test file not found: {rel}")
    return len(entries)


def _check_id(line: int, req_id: str, seen: dict[str, int], report: Report) -> None:
    """Validate requirement_id format and uniqueness; record first occurrence in ``seen``."""
    if not REQUIREMENT_ID_RE.match(req_id):
        report.errors.append(f"line {line}: invalid requirement_id {req_id!r}")
    if req_id in seen:
        report.errors.append(
            f"line {line}: duplicate requirement_id {req_id!r} (first on line {seen[req_id]})"
        )
    else:
        seen[req_id] = line


def check(rows: Sequence[Sequence[str]], repo_root: Path, strict: bool) -> Report:
    """Check parsed CSV rows (``rows[0]`` is the header) against the traceability rules."""
    report = Report(by_priority=dict.fromkeys(PRIORITIES, 0))
    if not rows:
        report.errors.append("traceability CSV is empty (no header)")
        return report
    header = tuple(cell.strip() for cell in rows[0])
    if header != EXPECTED_HEADER:
        report.errors.append(
            f"header mismatch: expected {','.join(EXPECTED_HEADER)!r}, got {','.join(header)!r}"
        )
        return report

    seen: dict[str, int] = {}
    for line, row in enumerate(rows[1:], start=2):
        if not any(cell.strip() for cell in row):
            continue  # tolerate blank lines
        if len(row) != len(EXPECTED_HEADER):
            report.errors.append(
                f"line {line}: expected {len(EXPECTED_HEADER)} columns, got {len(row)}"
            )
            continue
        req_id = row[_COL_ID].strip()
        priority = row[_COL_PRIORITY].strip()
        _check_id(line, req_id, seen, report)

        if priority in report.by_priority:
            report.by_priority[priority] += 1
        else:
            report.errors.append(
                f"line {line}: {req_id}: invalid priority {priority!r} "
                f"(expected one of {', '.join(PRIORITIES)})"
            )

        n_tests = _check_test_ids(line, req_id, row[_COL_TESTS], repo_root, report)

        if priority == "MUST":
            if n_tests:
                report.must_with_tests += 1
            else:
                report.must_without_tests += 1
                message = f"line {line}: {req_id}: MUST requirement has no linked test"
                (report.errors if strict else report.warnings).append(message)
    return report


def read_rows(csv_path: Path) -> list[list[str]]:
    """Parse the CSV file into rows (header included)."""
    with csv_path.open(encoding="utf-8", newline="") as handle:
        return list(csv.reader(handle))


def format_summary(report: Report, strict: bool) -> str:
    counts = ", ".join(f"{p}={n}" for p, n in report.by_priority.items())
    mode = "strict" if strict else "warn"
    return (
        f"traceability ({mode} mode): {counts}; "
        f"MUST with tests={report.must_with_tests}, without tests={report.must_without_tests}; "
        f"errors={len(report.errors)}, warnings={len(report.warnings)}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="traceability CSV path")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="repository root")
    parser.add_argument(
        "--strict", action="store_true", help="MUST rows without tests are errors (P2+)"
    )
    args = parser.parse_args(argv)
    csv_path: Path = args.csv
    repo_root: Path = args.root
    strict: bool = args.strict

    if not csv_path.is_file():
        print(f"ERROR: traceability CSV not found: {csv_path}", file=sys.stderr)
        return 1

    report = check(read_rows(csv_path), repo_root, strict)
    in_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    for message in report.warnings:
        print(f"WARNING: {message}")
        if in_actions:
            print(f"::warning title=traceability::{message}")
    for message in report.errors:
        print(f"ERROR: {message}", file=sys.stderr)
        if in_actions:
            print(f"::error title=traceability::{message}")
    print(format_summary(report, strict))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
