from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Price
from app.schemas import PriceCreate, PriceRead

router = APIRouter(prefix="/api/prices", tags=["prices"])


@router.get("", response_model=list[PriceRead])
def list_prices(product_id: int | None = None, db: Session = Depends(get_db)) -> list[Price]:
    stmt = select(Price).order_by(Price.price_date.desc(), Price.product_id)
    if product_id is not None:
        stmt = stmt.where(Price.product_id == product_id)
    return list(db.scalars(stmt))


@router.post("", response_model=PriceRead)
def create_price(payload: PriceCreate, db: Session = Depends(get_db)) -> Price:
    price = Price(**payload.model_dump())
    db.add(price)
    db.commit()
    db.refresh(price)
    return price
