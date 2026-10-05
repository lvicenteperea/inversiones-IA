from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Product(Base):
    __tablename__ = "inv_products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isin: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    product_type: Mapped[str] = mapped_column(String(50), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="EUR")
    risk_level: Mapped[int | None] = mapped_column(nullable=True)
    annual_cost_pct: Mapped[Decimal | None] = mapped_column(Numeric(8, 4), nullable=True)
    income_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    data_source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    active: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Portfolio(Base):
    __tablename__ = "inv_portfolios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    initial_amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    monthly_income_target: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    targets: Mapped[list["PortfolioTarget"]] = relationship(back_populates="portfolio")


class PortfolioTarget(Base):
    __tablename__ = "inv_portfolio_targets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("inv_portfolios.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("inv_products.id"), nullable=False)
    target_pct: Mapped[Decimal] = mapped_column(Numeric(8, 4), nullable=False)

    portfolio: Mapped[Portfolio] = relationship(back_populates="targets")
    product: Mapped[Product] = relationship()


class Transaction(Base):
    __tablename__ = "inv_transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("inv_portfolios.id"), nullable=False)
    product_id: Mapped[int | None] = mapped_column(ForeignKey("inv_products.id"), nullable=True)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(30), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    units: Mapped[Decimal | None] = mapped_column(Numeric(24, 8), nullable=True)
    price: Mapped[Decimal | None] = mapped_column(Numeric(18, 8), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    portfolio: Mapped[Portfolio] = relationship()
    product: Mapped[Product | None] = relationship()


class Price(Base):
    __tablename__ = "inv_prices"
    __table_args__ = (UniqueConstraint("product_id", "price_date", name="uk_product_date"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("inv_products.id"), nullable=False)
    price_date: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="EUR")
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    source_type: Mapped[str] = mapped_column(String(30), nullable=False, default="manual")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    product: Mapped[Product] = relationship()
