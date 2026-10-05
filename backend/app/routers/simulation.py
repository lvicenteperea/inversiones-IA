from decimal import Decimal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.simulation_service import simulate_compound_with_income

router = APIRouter(prefix="/api/simulation", tags=["simulation"])


class SimulationRequest(BaseModel):
    initial_amount: Decimal = Decimal("300000")
    annual_return_pct: Decimal = Decimal("3.5")
    monthly_income: Decimal = Decimal("650")
    years: int = Field(default=20, ge=1, le=50)
    inflation_pct: Decimal = Decimal("2.5")


@router.post("")
def run_simulation(payload: SimulationRequest) -> dict[str, object]:
    rows = simulate_compound_with_income(
        initial_amount=payload.initial_amount,
        annual_return_pct=payload.annual_return_pct,
        monthly_income=payload.monthly_income,
        years=payload.years,
        inflation_pct=payload.inflation_pct,
    )
    return {"input": payload.model_dump(mode="json"), "rows": rows}
