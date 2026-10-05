from decimal import Decimal

from fastapi import APIRouter
from fastapi.responses import Response

from app.services.excel_service import build_demo_report
from app.services.simulation_service import simulate_compound_with_income

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/demo.xlsx")
def download_demo_report() -> Response:
    rows = simulate_compound_with_income(
        initial_amount=Decimal("300000"),
        annual_return_pct=Decimal("3.5"),
        monthly_income=Decimal("650"),
        years=20,
        inflation_pct=Decimal("2.5"),
    )
    content = build_demo_report(rows)
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=inversiones_ia_demo.xlsx"},
    )
