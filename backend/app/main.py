from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import get_settings
from app.db import Base, engine
from app.routers import health, portfolios, prices, products, reports, simulation

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(health.router)
app.include_router(products.router)
app.include_router(portfolios.router)
app.include_router(prices.router)
app.include_router(simulation.router)
app.include_router(reports.router)

app.mount("/static", StaticFiles(directory="../frontend"), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse("../frontend/index.html")
