"""Money helpers: every amount is an integer number of paise (spec §6.3, §12.2, §18.2).

1 rupee = 100 paise. Floats are never accepted anywhere in this module, and nothing is ever rounded
silently: an input that is not an exact whole number of paise raises ``ValueError``. ``bool`` is
rejected even though it is a subclass of ``int``. All functions are pure (no I/O).
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from decimal import Decimal
from typing import Final, NewType, cast

__all__ = [
    "MICRO_TXN_MAX",
    "PAISE_PER_RUPEE",
    "Paise",
    "add",
    "format_inr",
    "from_rupees",
    "paise",
    "to_rupees",
    "total",
]

Paise = NewType("Paise", int)
"""An amount in paise (integer). Build one with :func:`paise` or :func:`from_rupees`."""

PAISE_PER_RUPEE: Final = 100
_RUPEE_DECIMALS: Final = 2
_MAX_RUPEE_DIGITS: Final = 20  # amounts >= 10**20 rupees are rejected (guards 10**huge blow-ups)

MICRO_TXN_MAX: Final[Paise] = Paise(1000)
"""Upper bound (inclusive) of a micro transaction: ₹10 (spec §9 F06, F26)."""

_RUPEE_SYMBOL: Final = "₹"
# Integer part: plain digits, Western grouping (1,234,567) or Indian grouping (12,34,567).
_AMOUNT_RE: Final = re.compile(
    r"(?P<sign>[+-]?)(?:₹\s*)?"
    r"(?P<int>\d+|\d{1,3}(?:,\d{3})+|\d{1,2}(?:,\d{2})*,\d{3})"
    r"(?:\.(?P<frac>\d+))?",
    re.ASCII,
)


def _require_int(value: object, what: str) -> int:
    """Return ``value`` if it is a real ``int`` (not ``bool``); otherwise raise ``TypeError``."""
    if isinstance(value, bool) or not isinstance(value, int):
        msg = f"{what} must be int paise, got {type(value).__name__}"
        raise TypeError(msg)
    return value


def paise(value: int, *, allow_negative: bool = False) -> Paise:
    """Validate an integer paise amount.

    Raises ``TypeError`` for ``bool``, ``float`` or any non-``int``; ``ValueError`` for a negative
    amount unless ``allow_negative`` is set (refunds, deltas).
    """
    v = _require_int(value, "amount")
    if v < 0 and not allow_negative:
        msg = f"negative amount {v} paise (pass allow_negative=True for refunds/deltas)"
        raise ValueError(msg)
    return Paise(v)


def _decimal_to_paise(d: Decimal) -> int:
    """Exact Decimal rupees -> int paise, using integer arithmetic only (no context rounding)."""
    if not d.is_finite():
        msg = f"amount must be finite, got {d}"
        raise ValueError(msg)
    sign, digits, raw_exponent = d.as_tuple()
    exponent = cast("int", raw_exponent)  # finite Decimals always have an int exponent
    coefficient = int("".join(map(str, digits)))
    if coefficient and len(digits) + exponent > _MAX_RUPEE_DIGITS:
        msg = f"amount {d} is too large"
        raise ValueError(msg)
    shift = exponent + _RUPEE_DECIMALS
    if shift >= 0:
        result = coefficient * 10**shift
    else:
        result, remainder = divmod(coefficient, 10**-shift)
        if remainder:
            msg = f"amount {d} has more than 2 decimal places (no silent rounding)"
            raise ValueError(msg)
    return -result if sign else result


def _parse_rupee_string(text: str) -> Decimal:
    match = _AMOUNT_RE.fullmatch(text.strip())
    if match is None:
        msg = f"not a rupee amount: {text!r}"
        raise ValueError(msg)
    number = match["sign"] + match["int"].replace(",", "")
    if match["frac"] is not None:
        number += "." + match["frac"]
    return Decimal(number)


def from_rupees(value: str | Decimal | int, *, allow_negative: bool = False) -> Paise:
    """Convert a rupee amount to paise, exactly.

    Accepts ``int`` rupees, ``Decimal`` rupees, or strings such as ``"12.5"``, ``"12.50"``,
    ``"1,234.50"``, ``"12,34,567.89"`` or ``"₹1,000"`` (also ``"-₹1,000.00"`` as produced by
    :func:`format_inr`). Any value that is not a whole number of paise raises ``ValueError``
    (e.g. ``"12.345"``); trailing zeros are fine (``"12.500"`` is 1250 paise). NaN, infinity, empty
    or malformed strings raise ``ValueError``; ``float``, ``bool`` and other types raise
    ``TypeError``. Negative results follow :func:`paise`'s ``allow_negative`` rule.
    """
    return paise(_rupees_to_paise_int(value), allow_negative=allow_negative)


def _rupees_to_paise_int(value: object) -> int:
    if isinstance(value, bool | float):
        msg = f"rupees must be str, Decimal or int, never {type(value).__name__}"
        raise TypeError(msg)
    if isinstance(value, int):
        return value * PAISE_PER_RUPEE
    if isinstance(value, Decimal):
        return _decimal_to_paise(value)
    if isinstance(value, str):
        return _decimal_to_paise(_parse_rupee_string(value))
    msg = f"rupees must be str, Decimal or int, got {type(value).__name__}"
    raise TypeError(msg)


def to_rupees(p: Paise) -> Decimal:
    """Exact rupee value of ``p`` with two decimal places (5 -> ``Decimal("0.05")``)."""
    v = _require_int(p, "amount")
    digits = tuple(int(c) for c in str(abs(v)))
    return Decimal((int(v < 0), digits, -_RUPEE_DECIMALS))


def _group_indian(rupees: int) -> str:
    """Indian digit grouping: last three digits, then groups of two (12,34,567)."""
    s = str(rupees)
    head, tail = s[:-3], s[-3:]
    groups: list[str] = []
    while head:
        groups.insert(0, head[-2:])
        head = head[:-2]
    return ",".join([*groups, tail])


def format_inr(p: Paise, *, symbol: bool = True) -> str:
    """Format paise as Indian rupees: ``₹12,34,567.89``, ``₹0.05``, ``-₹1,000.00``."""
    v = _require_int(p, "amount")
    rupees, rest = divmod(abs(v), PAISE_PER_RUPEE)
    sign = "-" if v < 0 else ""
    prefix = _RUPEE_SYMBOL if symbol else ""
    return f"{sign}{prefix}{_group_indian(rupees)}.{rest:02d}"


def total(amounts: Iterable[Paise]) -> Paise:
    """Sum paise amounts; every element must be an ``int`` (not ``bool``/``float``)."""
    return Paise(sum(_require_int(a, "amount") for a in amounts))


def add(*amounts: Paise) -> Paise:
    """Sum paise amounts given as arguments; see :func:`total`."""
    return total(amounts)
