from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    isin: str | None = None
    name: str
    product_type: str
    currency: str = "EUR"
    risk_level: int | None = Field(default=None, ge=1, le=7)
    annual_cost_pct: Decimal | None = None
    income_type: str | None = None
    data_source: str | None = None


class ProductRead(ProductCreate):
    id: int
    active: int

    model_config = {"from_attributes": True}


class PortfolioCreate(BaseModel):
    name: str
    description: str | None = None
    initial_amount: Decimal
    monthly_income_target: Decimal = Decimal("0")


class PortfolioRead(PortfolioCreate):
    id: int

    model_config = {"from_attributes": True}


class PriceCreate(BaseModel):
    product_id: int
    price_date: date
    price: Decimal
    currency: str = "EUR"
    source: str = "manual"
    source_type: str = "manual"


class PriceRead(PriceCreate):
    id: int

    model_config = {"from_attributes": True}


class PortfolioTargetRead(BaseModel):
    product_id: int
    product_name: str
    product_type: str
    target_pct: Decimal
    target_amount: Decimal


class PortfolioSummary(BaseModel):
    portfolio_id: int
    name: str
    initial_amount: Decimal
    monthly_income_target: Decimal
    targets: list[PortfolioTargetRead]
