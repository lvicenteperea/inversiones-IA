from io import BytesIO
from openpyxl import Workbook


def build_demo_report(rows: list[dict]) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Simulacion"
    ws.append(["Anio", "Valor nominal", "Valor real"])
    for row in rows:
        ws.append([row["year"], float(row["nominal_value"]), float(row["real_value"])])

    buffer = BytesIO()
    wb.save(buffer)
    return buffer.getvalue()
