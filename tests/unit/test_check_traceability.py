"""Unit tests for scripts/check_traceability.py (spec §4.10, DECISIONS T04)."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.check_traceability import (
    DEFAULT_CSV,
    EXPECTED_HEADER,
    REPO_ROOT,
    check,
    file_of_test_id,
    main,
    read_rows,
    split_test_ids,
)

pytestmark = pytest.mark.unit

HEADER = list(EXPECTED_HEADER)


def _row(
    req_id: str = "FR-01", priority: str = "MUST", tests: str = "tests/test_a.py"
) -> list[str]:
    return [req_id, priority, "US-01", "§6.3", "P0-T04", tests]


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_a.py").write_text("", encoding="utf-8")
    (tmp_path / "tests" / "test_b.py").write_text("", encoding="utf-8")
    return tmp_path


def test_valid_rows_pass(repo: Path) -> None:
    rows = [HEADER, _row(), _row("NFR-02", "SHOULD", ""), _row("FR-13a", "COULD", "")]
    report = check(rows, repo, strict=True)
    assert report.ok
    assert report.warnings == []
    assert report.by_priority == {"MUST": 1, "SHOULD": 1, "COULD": 1}
    assert report.must_with_tests == 1
    assert report.must_without_tests == 0


def test_header_mismatch_is_error(repo: Path) -> None:
    bad_header = ["requirement_id", "story_id", "design_section", "test_ids"]
    report = check([bad_header, _row()], repo, strict=False)
    assert not report.ok
    assert "header mismatch" in report.errors[0]


def test_empty_csv_is_error(repo: Path) -> None:
    assert not check([], repo, strict=False).ok


@pytest.mark.parametrize("bad_id", ["FR-1", "fr-01", "NFR-001", "XR-01", "FR-01A", "FR-01ab", ""])
def test_bad_requirement_id(repo: Path, bad_id: str) -> None:
    report = check([HEADER, _row(req_id=bad_id)], repo, strict=False)
    assert any("invalid requirement_id" in e for e in report.errors)


def test_bad_priority(repo: Path) -> None:
    report = check([HEADER, _row(priority="WONT")], repo, strict=False)
    assert any("invalid priority" in e for e in report.errors)


def test_duplicate_id(repo: Path) -> None:
    report = check([HEADER, _row(), _row()], repo, strict=False)
    assert any("duplicate requirement_id 'FR-01'" in e for e in report.errors)


def test_wrong_column_count(repo: Path) -> None:
    report = check([HEADER, ["FR-01", "MUST"]], repo, strict=False)
    assert any("expected 6 columns" in e for e in report.errors)


def test_missing_test_file_is_error_even_in_warn_mode(repo: Path) -> None:
    report = check([HEADER, _row(tests="tests/test_a.py;tests/nope.py")], repo, strict=False)
    assert report.errors == ["line 2: FR-01: test file not found: tests/nope.py"]


@pytest.mark.parametrize("bad_path", ["/etc/passwd", "../outside.py", "::name"])
def test_non_relative_test_path_is_error(repo: Path, bad_path: str) -> None:
    report = check([HEADER, _row(tests=bad_path)], repo, strict=False)
    assert any("repo-relative path" in e for e in report.errors)


def test_path_with_test_name_form(repo: Path) -> None:
    tests = "tests/test_a.py::test_x; tests/test_b.py::TestC::test_y ;"
    report = check([HEADER, _row(tests=tests)], repo, strict=True)
    assert report.ok
    assert report.must_with_tests == 1


def test_split_and_file_of() -> None:
    assert split_test_ids(" a.py ; ;b.py::t ") == ["a.py", "b.py::t"]
    assert file_of_test_id("tests/x.py::TestA::test_b") == "tests/x.py"
    assert file_of_test_id("tests/x.py") == "tests/x.py"


def test_must_without_tests_warns_by_default(repo: Path) -> None:
    report = check([HEADER, _row(tests="")], repo, strict=False)
    assert report.ok
    assert report.warnings == ["line 2: FR-01: MUST requirement has no linked test"]
    assert report.must_without_tests == 1


def test_must_without_tests_fails_in_strict(repo: Path) -> None:
    report = check([HEADER, _row(tests="")], repo, strict=True)
    assert report.errors == ["line 2: FR-01: MUST requirement has no linked test"]
    assert report.warnings == []


def test_main_exit_codes_and_annotations(
    repo: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    csv_path = repo / "trace.csv"
    csv_path.write_text(
        ",".join(HEADER) + "\nFR-01,MUST,,§6.3,,\nFR-02,MUST,,§7,,tests/test_a.py\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    assert main(["--csv", str(csv_path), "--root", str(repo)]) == 0
    out = capsys.readouterr().out
    assert "::warning title=traceability::line 2: FR-01" in out
    assert "MUST with tests=1, without tests=1" in out

    assert main(["--csv", str(csv_path), "--root", str(repo), "--strict"]) == 1
    captured = capsys.readouterr()
    assert "::error title=traceability::line 2: FR-01" in captured.out
    assert "ERROR: line 2: FR-01" in captured.err


def test_main_missing_csv(repo: Path) -> None:
    assert main(["--csv", str(repo / "absent.csv")]) == 1


def test_real_traceability_csv_passes_in_warn_mode() -> None:
    report = check(read_rows(DEFAULT_CSV), REPO_ROOT, strict=False)
    assert report.errors == []
    assert sum(report.by_priority.values()) > 0
