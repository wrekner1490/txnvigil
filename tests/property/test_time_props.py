"""Property tests for core.time (spec §9, §18.3); skipped without hypothesis, run in CI."""

from __future__ import annotations

import math

import pytest

hypothesis = pytest.importorskip("hypothesis")
st = pytest.importorskip("hypothesis.strategies")

from core.time import (  # noqa: E402
    DAY_MS,
    WEEK_MS,
    cyclic_hour,
    format_ts,
    from_epoch_ms,
    hour_of_day_ist,
    parse_ts,
    to_epoch_ms,
    window_bounds,
)

pytestmark = pytest.mark.property

# 1900-01-01 .. 2100-01-01 in epoch ms.
epoch_ms = st.integers(min_value=-2208988800000, max_value=4102444800000)
windows = st.integers(min_value=1, max_value=WEEK_MS)


@hypothesis.given(epoch_ms)
def test_epoch_round_trip(ms: int) -> None:
    assert to_epoch_ms(from_epoch_ms(ms)) == ms


@hypothesis.given(epoch_ms)
def test_format_parse_round_trip(ms: int) -> None:
    text = format_ts(from_epoch_ms(ms))
    assert text.endswith("Z")
    assert to_epoch_ms(parse_ts(text)) == ms
    assert format_ts(parse_ts(text)) == text


@hypothesis.given(
    epoch_ms, st.lists(st.integers(min_value=-DAY_MS, max_value=DAY_MS)), windows, windows
)
def test_window_count_monotone_and_past_only(
    now: int, offsets: list[int], w1: int, w2: int
) -> None:
    small, large = sorted((w1, w2))
    events = [now + o for o in offsets]

    def count(window: int, *, include_current: bool = True) -> int:
        lo, hi = window_bounds(now, window, include_current=include_current)
        return sum(lo < t <= hi for t in events)

    assert count(small) <= count(large)
    assert count(small, include_current=False) <= count(small)
    future = [t for t in events if t > now]
    lo, hi = window_bounds(now, large)
    assert not any(lo < t <= hi for t in future)


@hypothesis.given(epoch_ms)
def test_ist_features_in_range(ms: int) -> None:
    assert 0 <= hour_of_day_ist(ms) <= 23
    s, c = cyclic_hour(ms)
    assert math.isclose(s * s + c * c, 1.0, rel_tol=1e-9)
