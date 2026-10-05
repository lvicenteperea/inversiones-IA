from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Portfolio, PortfolioTarget, Product
from app.schemas import PortfolioCreate, PortfolioRead, PortfolioSummary, PortfolioTargetRead

router = APIRouter(prefix="/api/portfolios", tags=["portfolios"])


@router.get("", response_model=list[PortfolioRead])
def list_portfolios(db: Session = Depends(get_db)) -> list[Portfolio]:
    return list(db.scalars(select(Portfolio).order_by(Portfolio.name)))


@router.post("", response_model=PortfolioRead)
def create_portfolio(payload: PortfolioCreate, db: Session = Depends(get_db)) -> Portfolio:
    portfolio = Portfolio(**payload.model_dump())
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


@router.get("/{portfolio_id}/summary", response_model=PortfolioSummary)
def get_portfolio_summary(portfolio_id: int, db: Session = Depends(get_db)) -> PortfolioSummary:
    portfolio = db.get(Portfolio, portfolio_id)
    if portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    rows = db.execute(
        select(PortfolioTarget, Product)
        .join(Product, Product.id == PortfolioTarget.product_id)
        .where(PortfolioTarget.portfolio_id == portfolio_id)
        .order_by(Product.name)
    ).all()

    targets = [
        PortfolioTargetRead(
            product_id=product.id,
            product_name=product.name,
            product_type=product.product_type,
            target_pct=target.target_pct,
            target_amount=(portfolio.initial_amount * target.target_pct / Decimal("100")),
        )
        for target, product in rows
    ]

    return PortfolioSummary(
        portfolio_id=portfolio.id,
        name=portfolio.name,
        initial_amount=portfolio.initial_amount,
        monthly_income_target=portfolio.monthly_income_target,
        targets=targets,
    )
