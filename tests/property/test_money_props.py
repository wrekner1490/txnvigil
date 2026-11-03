"""Property tests for core.money (spec §18.3); skipped without hypothesis, run in CI."""

from __future__ import annotations

import pytest

hypothesis = pytest.importorskip("hypothesis")
st = pytest.importorskip("hypothesis.strategies")

from core.money import Paise, add, format_inr, from_rupees, to_rupees, total  # noqa: E402

pytestmark = pytest.mark.property

# |amount| < 10**20 rupees, the from_rupees limit.
amounts = st.integers(min_value=-(10**21) + 1, max_value=10**21 - 1)


@hypothesis.given(amounts)
def test_rupee_round_trip(p: int) -> None:
    assert from_rupees(to_rupees(Paise(p)), allow_negative=True) == p


@hypothesis.given(amounts, st.booleans())
def test_format_parse_stability(p: int, symbol: bool) -> None:
    text = format_inr(Paise(p), symbol=symbol)
    assert from_rupees(text, allow_negative=True) == p
    assert text.endswith(f".{abs(p) % 100:02d}")


@hypothesis.given(amounts)
def test_string_of_decimal_round_trip(p: int) -> None:
    assert from_rupees(str(to_rupees(Paise(p))), allow_negative=True) == p


@hypothesis.given(st.lists(amounts, max_size=50))
def test_total_matches_sum(values: list[int]) -> None:
    ps = [Paise(v) for v in values]
    assert total(ps) == sum(values)
    assert add(*ps) == sum(values)
