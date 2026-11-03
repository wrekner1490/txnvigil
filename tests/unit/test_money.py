"""Unit tests for core.money (spec §6.3 money in paise; §18.2 money helpers, no float)."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest

from core.money import (
    MICRO_TXN_MAX,
    PAISE_PER_RUPEE,
    Paise,
    add,
    format_inr,
    from_rupees,
    paise,
    to_rupees,
    total,
)

pytestmark = pytest.mark.unit

# Values typed Any so the type checker lets us pass wrong types on purpose.
FLOAT: Any = 12.5
TRUE: Any = True


# --------------------------------------------------------------------------- paise()
def test_paise_accepts_int() -> None:
    assert paise(0) == 0
    assert paise(1250000) == 1250000


@pytest.mark.parametrize("bad", [FLOAT, 1.0, TRUE, False, "100", None, Decimal(1)])
def test_paise_rejects_non_int(bad: Any) -> None:
    with pytest.raises(TypeError, match="must be int paise"):
        paise(bad)


def test_paise_rejects_negative_by_default() -> None:
    with pytest.raises(ValueError, match="negative amount"):
        paise(-1)


def test_paise_allows_negative_when_asked() -> None:
    assert paise(-500, allow_negative=True) == -500


def test_constants() -> None:
    assert PAISE_PER_RUPEE == 100
    assert MICRO_TXN_MAX == 1000  # ₹10, spec F06
    assert format_inr(MICRO_TXN_MAX) == "₹10.00"


# --------------------------------------------------------------------------- from_rupees()
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("12.5", 1250),
        ("12.50", 1250),
        ("12", 1200),
        ("0.05", 5),
        ("0", 0),
        ("1,234.50", 123450),
        ("1,234,567.89", 123456789),
        ("12,34,567.89", 123456789),
        ("1,00,00,000", 1000000000),
        ("₹1,000", 100000),
        ("₹ 12.5", 1250),
        ("  ₹99.99  ", 9999),
        ("+₹5", 500),
        ("12.500", 1250),  # trailing zeros are exact, not rounding
        ("007.10", 710),
    ],
)
def test_from_rupees_strings(text: str, expected: int) -> None:
    assert from_rupees(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [("-₹1,000.00", -100000), ("-12.5", -1250), ("-0.01", -1)],
)
def test_from_rupees_negative_strings(text: str, expected: int) -> None:
    assert from_rupees(text, allow_negative=True) == expected
    with pytest.raises(ValueError, match="negative amount"):
        from_rupees(text)


@pytest.mark.parametrize("text", ["12.345", "0.001", "1,234.567", "-1.999"])
def test_from_rupees_rejects_more_than_two_decimals(text: str) -> None:
    with pytest.raises(ValueError, match="more than 2 decimal places"):
        from_rupees(text, allow_negative=True)


@pytest.mark.parametrize(
    "text",
    [
        "",
        "   ",
        "abc",
        "12a",
        "12.",
        ".5",
        "1,2",
        "1,23,4567",
        ",123",
        "123,",
        "1.234,50",
        "12.5.0",
        "₹",
        "₹-5",
        "--5",
        "1e3",
        "NaN",
        "Infinity",
        "१२",  # non-ASCII digits are not accepted
        "12 34",
    ],
)
def test_from_rupees_rejects_garbage(text: str) -> None:
    with pytest.raises(ValueError, match="not a rupee amount"):
        from_rupees(text)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (Decimal("12.5"), 1250),
        (Decimal("12.50"), 1250),
        (Decimal("12.500"), 1250),
        (Decimal("0.01"), 1),
        (Decimal("1E3"), 100000),
        (Decimal("0E+50"), 0),
        (Decimal("0"), 0),
    ],
)
def test_from_rupees_decimal(value: Decimal, expected: int) -> None:
    assert from_rupees(value) == expected


def test_from_rupees_decimal_negative() -> None:
    assert from_rupees(Decimal("-7.25"), allow_negative=True) == -725


@pytest.mark.parametrize("value", [Decimal("12.345"), Decimal("0.001"), Decimal("1E-3")])
def test_from_rupees_decimal_rejects_sub_paise(value: Decimal) -> None:
    with pytest.raises(ValueError, match="more than 2 decimal places"):
        from_rupees(value)


@pytest.mark.parametrize(
    "value", [Decimal("NaN"), Decimal("sNaN"), Decimal("Infinity"), Decimal("-Infinity")]
)
def test_from_rupees_rejects_non_finite(value: Decimal) -> None:
    with pytest.raises(ValueError, match="must be finite"):
        from_rupees(value, allow_negative=True)


@pytest.mark.parametrize("value", [Decimal("1E20"), Decimal("1E999999"), "1" + "0" * 20])
def test_from_rupees_rejects_absurdly_large(value: Decimal | str) -> None:
    with pytest.raises(ValueError, match="too large"):
        from_rupees(value)


def test_from_rupees_largest_accepted() -> None:
    assert from_rupees("9" * 20) == int("9" * 20) * 100


def test_from_rupees_int() -> None:
    assert from_rupees(12) == 1200
    assert from_rupees(0) == 0
    assert from_rupees(-3, allow_negative=True) == -300


@pytest.mark.parametrize("bad", [FLOAT, 0.1, 1e3, TRUE, False])
def test_from_rupees_rejects_float_and_bool(bad: Any) -> None:
    with pytest.raises(TypeError, match="never"):
        from_rupees(bad)


@pytest.mark.parametrize("bad", [None, b"12", [12], object()])
def test_from_rupees_rejects_other_types(bad: Any) -> None:
    with pytest.raises(TypeError, match="must be str, Decimal or int"):
        from_rupees(bad)


# --------------------------------------------------------------------------- to_rupees()
@pytest.mark.parametrize(
    ("p", "expected"),
    [
        (0, "0.00"),
        (5, "0.05"),
        (50, "0.50"),
        (1250, "12.50"),
        (123456789, "1234567.89"),
        (-5, "-0.05"),
    ],
)
def test_to_rupees_exact_two_dp(p: int, expected: str) -> None:
    result = to_rupees(Paise(p))
    assert result == Decimal(expected)
    assert str(result) == expected
    assert result.as_tuple().exponent == -2


def test_to_rupees_huge_is_exact() -> None:
    p = Paise(10**40 + 1)
    assert str(to_rupees(p)) == "1" + "0" * 38 + ".01"  # no float / context-precision loss


def test_to_rupees_rejects_float() -> None:
    with pytest.raises(TypeError):
        to_rupees(FLOAT)


def test_round_trip_examples() -> None:
    for p in (0, 1, 99, 100, 101, 123456789):
        assert from_rupees(to_rupees(Paise(p))) == p


# --------------------------------------------------------------------------- format_inr()
@pytest.mark.parametrize(
    ("p", "expected"),
    [
        (0, "₹0.00"),
        (5, "₹0.05"),
        (99, "₹0.99"),
        (100, "₹1.00"),
        (99999, "₹999.99"),
        (100000, "₹1,000.00"),  # 1e3 rupees
        (9999999, "₹99,999.99"),
        (10000000, "₹1,00,000.00"),  # 1e5 rupees: first lakh group
        (123456789, "₹12,34,567.89"),
        (1000000000, "₹1,00,00,000.00"),  # 1e7 rupees: one crore
        (12345678901234, "₹1,23,45,67,89,012.34"),
    ],
)
def test_format_inr_indian_grouping(p: int, expected: str) -> None:
    assert format_inr(Paise(p)) == expected


def test_format_inr_negative() -> None:
    assert format_inr(paise(-100000, allow_negative=True)) == "-₹1,000.00"
    assert format_inr(paise(-5, allow_negative=True)) == "-₹0.05"


def test_format_inr_without_symbol() -> None:
    assert format_inr(Paise(123456789), symbol=False) == "12,34,567.89"
    assert format_inr(paise(-100, allow_negative=True), symbol=False) == "-1.00"


@pytest.mark.parametrize("p", [0, 5, 100000, 123456789, -100000, 10**18])
def test_format_then_parse_is_stable(p: int) -> None:
    assert from_rupees(format_inr(Paise(p)), allow_negative=True) == p
    assert from_rupees(format_inr(Paise(p), symbol=False), allow_negative=True) == p


@pytest.mark.parametrize("bad", [FLOAT, TRUE])
def test_format_inr_rejects_non_int(bad: Any) -> None:
    with pytest.raises(TypeError):
        format_inr(bad)


# --------------------------------------------------------------------------- add() / total()
def test_add_and_total() -> None:
    a, b, c = Paise(100), Paise(250), Paise(5)
    assert add(a, b, c) == 355
    assert add() == 0
    assert total([a, b, c]) == 355
    assert total([]) == 0
    assert total(Paise(x) for x in range(5)) == 10
    assert add(Paise(100), paise(-30, allow_negative=True)) == 70


@pytest.mark.parametrize("bad", [FLOAT, TRUE, "1", None])
def test_add_and_total_reject_non_int(bad: Any) -> None:
    with pytest.raises(TypeError):
        add(Paise(1), bad)
    with pytest.raises(TypeError):
        total([Paise(1), bad])
