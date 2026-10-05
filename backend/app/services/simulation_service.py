from decimal import Decimal


def simulate_compound_with_income(
    initial_amount: Decimal,
    annual_return_pct: Decimal,
    monthly_income: Decimal,
    years: int,
    inflation_pct: Decimal,
) -> list[dict[str, Decimal | int]]:
    """Simple deterministic simulation for MVP dashboards.

    It assumes a constant annual return and monthly withdrawals.
    This is not a market forecast.
    """
    years = max(1, min(years, 50))
    monthly_return = (Decimal("1") + annual_return_pct / Decimal("100")) ** (Decimal("1") / Decimal("12")) - Decimal("1")
    inflation = inflation_pct / Decimal("100")

    value = initial_amount
    rows: list[dict[str, Decimal | int]] = []
    for month in range(0, years * 12 + 1):
        if month > 0:
            value = max(Decimal("0"), value * (Decimal("1") + monthly_return) - monthly_income)
        if month % 12 == 0:
            year = month // 12
            real_value = value / ((Decimal("1") + inflation) ** year)
            rows.append({"year": year, "nominal_value": value, "real_value": real_value})
    return rows
