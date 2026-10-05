# Inversiones IA

Simulador privado de carteras de inversion para probar estrategias conservadoras antes de invertir dinero real.

## Objetivo

El proyecto permite crear carteras virtuales, registrar productos, cargar precios historicos, simular retiradas periodicas y analizar la evolucion nominal y real ajustada por inflacion.

## Stack inicial

- Backend: FastAPI
- Base de datos: MariaDB/MySQL compatible
- ORM: SQLAlchemy
- Exportacion Excel: openpyxl
- Frontend: HTML, CSS y JavaScript simple

## Arranque local previsto

```bash
cp .env.example .env
docker compose up -d
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Despues abre:

```text
http://localhost:8000
```

## Aviso

Este proyecto es una herramienta de simulacion y seguimiento. No constituye asesoramiento financiero.
