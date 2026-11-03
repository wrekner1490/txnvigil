"""Event-time utilities (spec §6.3, §9, §12.2).

Event time is UTC, carried as ISO-8601 strings with milliseconds and ``Z``
(``"2026-08-14T21:03:11.402Z"``) or as integer epoch milliseconds. Display and diurnal features
(F14) use India Standard Time, a fixed UTC+05:30 offset (India has no DST). All functions are pure.
"""

from __future__ import annotations

import math
from datetime import UTC, datetime, timedelta, timezone
from typing import Final

__all__ = [
    "DAY_MS",
    "HOUR_MS",
    "IST",
    "MINUTE_MS",
    "SECOND_MS",
    "WEEK_MS",
    "cyclic_hour",
    "format_ts",
    "from_epoch_ms",
    "hour_of_day_ist",
    "is_night_ist",
    "parse_ts",
    "to_epoch_ms",
    "window_bounds",
]

IST: Final = timezone(timedelta(hours=5, minutes=30), "IST")

SECOND_MS: Final = 1_000
MINUTE_MS: Final = 60 * SECOND_MS
HOUR_MS: Final = 60 * MINUTE_MS
DAY_MS: Final = 24 * HOUR_MS
WEEK_MS: Final = 7 * DAY_MS

_HOURS_PER_DAY: Final = 24
_MINUTES_PER_HOUR: Final = 60
_EPOCH: Final = datetime(1970, 1, 1, tzinfo=UTC)
_ONE_MS: Final = timedelta(milliseconds=1)


def _require_int(value: object, what: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        msg = f"{what} must be int, got {type(value).__name__}"
        raise TypeError(msg)
    return value


def _require_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None or dt.utcoffset() is None:
        msg = f"naive datetime {dt.isoformat()} has no UTC offset; event time must be aware"
        raise ValueError(msg)
    return dt


def parse_ts(s: str) -> datetime:
    """Parse an ISO-8601 timestamp with a mandatory offset or ``Z``; return an aware UTC datetime.

    ``"2026-08-14T21:03:11.402Z"`` and ``"2026-08-15T02:33:11.402+05:30"`` give the same instant.
    Naive timestamps (no offset) and malformed strings raise ``ValueError``.
    """
    return _require_aware(datetime.fromisoformat(s)).astimezone(UTC)


def to_epoch_ms(dt: datetime) -> int:
    """Epoch milliseconds, floored (sub-millisecond part dropped). Naive -> ``ValueError``."""
    return (_require_aware(dt) - _EPOCH) // _ONE_MS


def from_epoch_ms(ms: int) -> datetime:
    """Aware UTC datetime for epoch milliseconds ``ms`` (exact, integer arithmetic)."""
    return _EPOCH + timedelta(milliseconds=_require_int(ms, "ms"))


def format_ts(dt: datetime) -> str:
    """Canonical event-time string: UTC, milliseconds, ``Z`` suffix. Naive -> ``ValueError``."""
    utc = _require_aware(dt).astimezone(UTC)
    return utc.replace(tzinfo=None).isoformat(timespec="milliseconds") + "Z"


def window_bounds(now_ms: int, window_ms: int, *, include_current: bool = True) -> tuple[int, int]:
    """Past-only event-time window ``(lo, hi)``: event ``t`` is inside iff ``lo < t <= hi``.

    With ``include_current=True`` (spec §9 "past-only, incl. cur"): ``lo = now_ms - window_ms``,
    ``hi = now_ms``, i.e. ``now_ms - window_ms < t <= now_ms``. An event exactly ``window_ms`` old
    is OUTSIDE; one ``window_ms - 1`` ms old is inside; nothing after ``now_ms`` is ever inside.

    With ``include_current=False`` the upper bound becomes ``now_ms - 1`` (events strictly before
    ``now_ms``), and ``lo`` is unchanged. Valkey equivalent: ``ZCOUNT key (lo hi``.
    """
    now = _require_int(now_ms, "now_ms")
    window = _require_int(window_ms, "window_ms")
    if window <= 0:
        msg = f"window_ms must be positive, got {window}"
        raise ValueError(msg)
    hi = now if include_current else now - 1
    return now - window, hi


def _ist(ms: int) -> datetime:
    return from_epoch_ms(ms).astimezone(IST)


def hour_of_day_ist(ms: int) -> int:
    """Hour of day 0-23 in IST for epoch milliseconds ``ms`` (18:30Z is 00 IST)."""
    return _ist(ms).hour


def cyclic_hour(ms: int) -> tuple[float, float]:
    """``(sin, cos)`` of the IST time of day (hour + minute / 60) on a 24-hour circle (F14)."""
    local = _ist(ms)
    fraction = (local.hour + local.minute / _MINUTES_PER_HOUR) / _HOURS_PER_DAY
    angle = 2.0 * math.pi * fraction
    return math.sin(angle), math.cos(angle)


def is_night_ist(ms: int, *, start: int = 23, end: int = 5) -> bool:
    """True if the IST hour ``h`` is in the night band ``[start, end)``, wrapping past midnight.

    Default: 23:00 to 04:59 IST. ``start == end`` means an empty band (never night).
    Hours must be in 0-23 (``ValueError`` otherwise).
    """
    for name, value in (("start", start), ("end", end)):
        if not 0 <= _require_int(value, name) < _HOURS_PER_DAY:
            msg = f"{name} must be an hour in 0-23, got {value}"
            raise ValueError(msg)
    hour = hour_of_day_ist(ms)
    if start <= end:
        return start <= hour < end
    return hour >= start or hour < end
