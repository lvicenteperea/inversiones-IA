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

## Configuracion local

El proyecto usa un fichero `.env` local para la conexion a base de datos y otros parametros.

Crear el fichero local:

```bat
copy .env.example .env
```

Ejemplo de conexion probado en local:

```env
DATABASE_URL=mysql+pymysql://inv_user:inv_password@127.0.0.1:13306/inversiones_ia
```

El `.env` no se sube al repositorio. Cada entorno puede tener un puerto distinto.

Documentacion completa:

```text
docs/instalacion-local.md
```

## Arranque local con MariaDB ya instalada

```bat
cd C:\GitHub\inversiones-IA
git pull
copy .env.example .env
```

Editar `.env` y ajustar `DATABASE_URL`.

Despues:

```bat
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Si el entorno virtual ya existe:

```bat
cd C:\GitHub\inversiones-IA\backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

## Arranque local con Docker opcional

Docker solo es necesario si no se quiere usar una MariaDB local existente.

```bat
cd C:\GitHub\inversiones-IA
docker compose up -d
```

En ese caso, el puerto local publicado es `3307`, por lo que el `.env` debe usar:

```env
DATABASE_URL=mysql+pymysql://inv_user:inv_password@127.0.0.1:3307/inversiones_ia
```

## URLs locales

Con `uvicorn app.main:app --reload`, abrir:

```text
http://localhost:8000
```

URLs utiles:

```text
http://localhost:8000              Web inicial
http://localhost:8000/api/health   Health check
http://localhost:8000/docs         Swagger/OpenAPI
http://localhost:8000/api/reports/demo.xlsx  Excel demo
```

## Diagnostico rapido

Si aparece un error de conexion tipo `Can't connect to MySQL server on '127.0.0.1'`, revisar:

1. Que MariaDB este arrancada.
2. Que el puerto en `.env` sea correcto.
3. Que usuario/password sean correctos.
4. Que exista la base de datos `inversiones_ia`.

Comprobar puertos en Windows:

```bat
netstat -ano | findstr :13306
netstat -ano | findstr :3306
netstat -ano | findstr :3307
```

## Aviso

Este proyecto es una herramienta de simulacion y seguimiento. No constituye asesoramiento financiero.
