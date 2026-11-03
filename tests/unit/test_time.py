"""Unit tests for core.time (spec §6.3 ts format, §9 past-only windows, F14 IST features)."""

from __future__ import annotations

import math
from datetime import UTC, datetime, timedelta, timezone, tzinfo
from typing import Any

import pytest

from core.time import (
    DAY_MS,
    HOUR_MS,
    IST,
    MINUTE_MS,
    SECOND_MS,
    WEEK_MS,
    cyclic_hour,
    format_ts,
    from_epoch_ms,
    hour_of_day_ist,
    is_night_ist,
    parse_ts,
    to_epoch_ms,
    window_bounds,
)

pytestmark = pytest.mark.unit

SPEC_TS = "2026-08-14T21:03:11.402Z"  # spec §6.3 example
SPEC_MS = 1786741391402
FLOAT: Any = 1.5
TRUE: Any = True


def ms_of(s: str) -> int:
    return to_epoch_ms(parse_ts(s))


class _NoOffset(tzinfo):
    """A tzinfo whose utcoffset() is None: datetimes using it are naive per the datetime docs."""

    def utcoffset(self, dt: datetime | None) -> timedelta | None:
        return None

    def dst(self, dt: datetime | None) -> timedelta | None:
        return None

    def tzname(self, dt: datetime | None) -> str | None:
        return None


# --------------------------------------------------------------------------- constants
def test_constants() -> None:
    assert SECOND_MS == 1_000
    assert MINUTE_MS == 60_000
    assert HOUR_MS == 3_600_000
    assert DAY_MS == 86_400_000
    assert WEEK_MS == 604_800_000
    assert IST.utcoffset(None) == timedelta(hours=5, minutes=30)
    assert IST.dst(None) is None  # fixed offset, India has no DST


# --------------------------------------------------------------------------- parse_ts()
def test_parse_ts_spec_example() -> None:
    dt = parse_ts(SPEC_TS)
    assert dt == datetime(2026, 8, 14, 21, 3, 11, 402000, tzinfo=UTC)
    assert dt.tzinfo is UTC


@pytest.mark.parametrize(
    "s",
    [
        "2026-08-14T21:03:11.402+00:00",
        "2026-08-15T02:33:11.402+05:30",
        "2026-08-14T16:03:11.402-05:00",
    ],
)
def test_parse_ts_offsets_normalised_to_utc(s: str) -> None:
    dt = parse_ts(s)
    assert dt == parse_ts(SPEC_TS)
    assert dt.utcoffset() == timedelta(0)
    assert format_ts(dt) == SPEC_TS


@pytest.mark.parametrize("s", ["2026-08-14T21:03:11.402", "2026-08-14T21:03:11", "2026-08-14"])
def test_parse_ts_rejects_naive(s: str) -> None:
    with pytest.raises(ValueError, match="naive"):
        parse_ts(s)


@pytest.mark.parametrize("s", ["", "yesterday", "2026-13-01T00:00:00Z", "2026-08-14T25:00:00Z"])
def test_parse_ts_rejects_garbage(s: str) -> None:
    with pytest.raises(ValueError, match=r"Invalid isoformat|month|hour"):
        parse_ts(s)


# --------------------------------------------------------------------------- epoch ms
def test_to_epoch_ms_spec_example() -> None:
    assert to_epoch_ms(parse_ts(SPEC_TS)) == SPEC_MS


def test_epoch_zero_and_negative() -> None:
    assert to_epoch_ms(datetime(1970, 1, 1, tzinfo=UTC)) == 0
    assert from_epoch_ms(0) == datetime(1970, 1, 1, tzinfo=UTC)
    assert from_epoch_ms(-1) == datetime(1969, 12, 31, 23, 59, 59, 999000, tzinfo=UTC)
    assert to_epoch_ms(from_epoch_ms(-1)) == -1


def test_to_epoch_ms_floors_sub_millisecond() -> None:
    assert to_epoch_ms(datetime(1970, 1, 1, 0, 0, 0, 1999, tzinfo=UTC)) == 1
    assert to_epoch_ms(datetime(1969, 12, 31, 23, 59, 59, 999999, tzinfo=UTC)) == -1


def test_to_epoch_ms_accepts_any_aware_zone() -> None:
    ist_dt = datetime(2026, 8, 15, 2, 33, 11, 402000, tzinfo=IST)
    assert to_epoch_ms(ist_dt) == SPEC_MS


@pytest.mark.parametrize("dt", [datetime(2026, 1, 1), datetime(2026, 1, 1, tzinfo=_NoOffset())])  # noqa: DTZ001
def test_naive_datetimes_rejected(dt: datetime) -> None:
    with pytest.raises(ValueError, match="naive"):
        to_epoch_ms(dt)
    with pytest.raises(ValueError, match="naive"):
        format_ts(dt)


def test_from_epoch_ms_is_utc() -> None:
    dt = from_epoch_ms(SPEC_MS)
    assert dt.tzinfo is UTC
    assert format_ts(dt) == SPEC_TS


@pytest.mark.parametrize("bad", [FLOAT, TRUE, "0", None])
def test_from_epoch_ms_rejects_non_int(bad: Any) -> None:
    with pytest.raises(TypeError, match="must be int"):
        from_epoch_ms(bad)


@pytest.mark.parametrize("ms", [0, 1, -1, 999, SPEC_MS, 253402300799999, -62135596800000])
def test_round_trip_epoch_datetime_string(ms: int) -> None:
    dt = from_epoch_ms(ms)
    assert to_epoch_ms(dt) == ms
    assert ms_of(format_ts(dt)) == ms


# --------------------------------------------------------------------------- format_ts()
def test_format_ts_pads_milliseconds_and_truncates_micros() -> None:
    assert format_ts(datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)) == "2026-01-02T03:04:05.000Z"
    assert format_ts(datetime(2026, 1, 2, 3, 4, 5, 7999, tzinfo=UTC)) == "2026-01-02T03:04:05.007Z"


def test_format_ts_converts_to_utc() -> None:
    dt = datetime(2026, 1, 1, 0, 0, tzinfo=IST)
    assert format_ts(dt) == "2025-12-31T18:30:00.000Z"
    other = datetime(2026, 1, 1, 0, 0, tzinfo=timezone(timedelta(hours=-3)))
    assert format_ts(other) == "2026-01-01T03:00:00.000Z"


# --------------------------------------------------------------------------- window_bounds()
def inside(t: int, bounds: tuple[int, int]) -> bool:
    lo, hi = bounds
    return lo < t <= hi


def test_window_bounds_values() -> None:
    assert window_bounds(10_000, 1_000) == (9_000, 10_000)
    assert window_bounds(10_000, 1_000, include_current=False) == (9_000, 9_999)


def test_window_edges_exactly_one_hour() -> None:
    now = SPEC_MS
    b = window_bounds(now, HOUR_MS)
    assert not inside(now - HOUR_MS, b)  # exactly window_ms ago: OUTSIDE (§18.2 "exactly 1h")
    assert inside(now - HOUR_MS + 1, b)  # window_ms - 1 ms ago: inside
    assert not inside(now - HOUR_MS - 1, b)  # 1h + 1 ms ago: outside
    assert inside(now, b)  # current event included (incl. cur)
    assert not inside(now + 1, b)  # past-only: future never inside


def test_window_excluding_current() -> None:
    now = SPEC_MS
    b = window_bounds(now, DAY_MS, include_current=False)
    assert not inside(now, b)
    assert inside(now - 1, b)
    assert inside(now - DAY_MS + 1, b)
    assert not inside(now - DAY_MS, b)


def test_window_count_example() -> None:
    now = 100 * MINUTE_MS
    events = [now - 61 * MINUTE_MS, now - HOUR_MS, now - HOUR_MS + 1, now - 1, now, now + 1]
    b = window_bounds(now, HOUR_MS)
    assert sum(inside(t, b) for t in events) == 3


@pytest.mark.parametrize("window", [0, -1, -HOUR_MS])
def test_window_bounds_rejects_non_positive_window(window: int) -> None:
    with pytest.raises(ValueError, match="positive"):
        window_bounds(SPEC_MS, window)


@pytest.mark.parametrize(("now", "window"), [(FLOAT, 1), (1, FLOAT), (TRUE, 1), (1, TRUE)])
def test_window_bounds_rejects_non_int(now: Any, window: Any) -> None:
    with pytest.raises(TypeError, match="must be int"):
        window_bounds(now, window)


# --------------------------------------------------------------------------- IST features
@pytest.mark.parametrize(
    ("ts", "hour"),
    [
        ("2026-08-14T18:29:59.999Z", 23),
        ("2026-08-14T18:30:00.000Z", 0),  # midnight wrap: 18:30Z == 00:00 IST next day
        ("2026-08-14T00:00:00.000Z", 5),
        ("2026-08-14T06:29:59.999Z", 11),
        ("2026-08-14T06:30:00.000Z", 12),
        (SPEC_TS, 2),
    ],
)
def test_hour_of_day_ist(ts: str, hour: int) -> None:
    assert hour_of_day_ist(ms_of(ts)) == hour


def test_ist_midnight_is_next_calendar_day() -> None:
    local = from_epoch_ms(ms_of("2026-08-14T18:30:00Z")).astimezone(IST)
    assert (local.year, local.month, local.day, local.hour, local.minute) == (2026, 8, 15, 0, 0)


@pytest.mark.parametrize(
    ("ts", "expected"),
    [
        ("2026-08-14T18:30:00Z", (0.0, 1.0)),  # 00:00 IST
        ("2026-08-14T00:30:00Z", (1.0, 0.0)),  # 06:00 IST
        ("2026-08-14T06:30:00Z", (0.0, -1.0)),  # 12:00 IST
        ("2026-08-14T12:30:00Z", (-1.0, 0.0)),  # 18:00 IST
    ],
)
def test_cyclic_hour_quadrants(ts: str, expected: tuple[float, float]) -> None:
    s, c = cyclic_hour(ms_of(ts))
    assert s == pytest.approx(expected[0], abs=1e-12)
    assert c == pytest.approx(expected[1], abs=1e-12)


def test_cyclic_hour_uses_minutes_and_is_continuous_across_midnight() -> None:
    s1, c1 = cyclic_hour(ms_of("2026-08-14T18:29:00Z"))  # 23:59 IST
    s2, c2 = cyclic_hour(ms_of("2026-08-14T18:30:00Z"))  # 00:00 IST
    assert math.hypot(s1 - s2, c1 - c2) < 0.01
    half_hour = cyclic_hour(ms_of("2026-08-14T19:00:00Z"))  # 00:30 IST
    angle = 2 * math.pi * 0.5 / 24
    assert half_hour == pytest.approx((math.sin(angle), math.cos(angle)))


@pytest.mark.parametrize(
    ("ts", "night"),
    [
        ("2026-08-14T17:29:59.999Z", False),  # 22:59 IST
        ("2026-08-14T17:30:00.000Z", True),  # 23:00 IST (start inclusive)
        ("2026-08-14T18:30:00.000Z", True),  # 00:00 IST
        ("2026-08-14T23:29:59.999Z", True),  # 04:59 IST
        ("2026-08-14T23:30:00.000Z", False),  # 05:00 IST (end exclusive)
        ("2026-08-14T06:30:00.000Z", False),  # 12:00 IST
    ],
)
def test_is_night_ist_default_band(ts: str, night: bool) -> None:
    assert is_night_ist(ms_of(ts)) is night


def test_is_night_ist_non_wrapping_band() -> None:
    ms = ms_of("2026-08-14T20:30:00Z")  # 02:00 IST
    assert is_night_ist(ms, start=1, end=4) is True
    assert is_night_ist(ms, start=2, end=3) is True
    assert is_night_ist(ms, start=3, end=4) is False
    assert is_night_ist(ms, start=0, end=2) is False


def test_is_night_ist_empty_band() -> None:
    ms = ms_of("2026-08-14T20:30:00Z")
    assert is_night_ist(ms, start=2, end=2) is False


@pytest.mark.parametrize(("start", "end"), [(24, 5), (-1, 5), (23, 24), (23, -1)])
def test_is_night_ist_rejects_bad_hours(start: int, end: int) -> None:
    with pytest.raises(ValueError, match="hour in 0-23"):
        is_night_ist(SPEC_MS, start=start, end=end)


@pytest.mark.parametrize(("start", "end"), [(FLOAT, 5), (23, TRUE)])
def test_is_night_ist_rejects_non_int_hours(start: Any, end: Any) -> None:
    with pytest.raises(TypeError, match="must be int"):
        is_night_ist(SPEC_MS, start=start, end=end)
