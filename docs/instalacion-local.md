# Instalacion local

Este documento resume como levantar el proyecto en local y como configurar la conexion a MariaDB.

## 1. Repositorio

Clonar o actualizar el repositorio:

```bat
git clone https://github.com/lvicenteperea/inversiones-IA.git
cd inversiones-IA
```

Si ya existe en local:

```bat
cd C:\GitHub\inversiones-IA
git pull
```

## 2. Fichero `.env`

El fichero `.env` contiene la configuracion local de cada maquina. No debe subirse al repositorio.

Crear el fichero a partir del ejemplo:

```bat
copy .env.example .env
```

La aplicacion busca el `.env` en estas ubicaciones:

```text
C:\GitHub\inversiones-IA\.env
C:\GitHub\inversiones-IA\backend\.env
```

Se recomienda usar el `.env` de la raiz del proyecto.

## 3. MariaDB local

Si ya existe una MariaDB local, solo hay que ajustar `DATABASE_URL` en el `.env`.

Ejemplo probado en local:

```env
DATABASE_URL=mysql+pymysql://inv_user:inv_password@127.0.0.1:13306/inversiones_ia
```

Formato general:

```env
DATABASE_URL=mysql+pymysql://USUARIO:PASSWORD@HOST:PUERTO/BASE_DATOS
```

Ejemplos habituales:

```env
# MariaDB local estandar
DATABASE_URL=mysql+pymysql://inv_user:inv_password@127.0.0.1:3306/inversiones_ia

# MariaDB local del entorno actual de Luis
DATABASE_URL=mysql+pymysql://inv_user:inv_password@127.0.0.1:13306/inversiones_ia

# MariaDB levantada con Docker Compose de este proyecto
DATABASE_URL=mysql+pymysql://inv_user:inv_password@127.0.0.1:3307/inversiones_ia
```

## 4. Crear base de datos y usuario

Si no existe la base de datos, ejecutar en MariaDB:

```sql
CREATE DATABASE IF NOT EXISTS inversiones_ia
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'inv_user'@'%'
IDENTIFIED BY 'inv_password';

GRANT ALL PRIVILEGES ON inversiones_ia.* TO 'inv_user'@'%';
FLUSH PRIVILEGES;
```

Despues ejecutar los scripts del proyecto:

```text
sql/001_init.sql
sql/002_seed_demo.sql
```

Si la aplicacion arranca con permisos suficientes, SQLAlchemy tambien puede crear las tablas definidas en los modelos, pero los scripts SQL dejan el entorno mas controlado.

## 5. Docker opcional

Docker no es obligatorio si ya se dispone de MariaDB local.

El fichero `docker-compose.yml` levanta una MariaDB 11.5 para desarrollo y expone el puerto local `3307` contra el puerto interno `3306` del contenedor:

```yaml
ports:
  - "3307:3306"
```

Para usar Docker:

```bat
cd C:\GitHub\inversiones-IA
docker compose up -d
```

Comprobar estado:

```bat
docker compose ps
docker logs inversiones_ia_db
```

En este modo, el `.env` debe usar:

```env
DATABASE_URL=mysql+pymysql://inv_user:inv_password@127.0.0.1:3307/inversiones_ia
```

## 6. Arrancar backend

Desde la carpeta `backend`:

```bat
cd C:\GitHub\inversiones-IA\backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Si el entorno virtual ya existe, basta con:

```bat
cd C:\GitHub\inversiones-IA\backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

## 7. URLs locales

Con `uvicorn app.main:app --reload`, la aplicacion queda disponible en:

```text
http://127.0.0.1:8000
http://localhost:8000
```

URLs utiles:

```text
http://localhost:8000              Web inicial
http://localhost:8000/api/health   Comprobacion de salud
http://localhost:8000/docs         Swagger/OpenAPI
http://localhost:8000/api/reports/demo.xlsx  Excel demo
```

## 8. Diagnostico de conexion MariaDB

Si aparece un error parecido a:

```text
Can't connect to MySQL server on '127.0.0.1'
WinError 10061
```

significa normalmente una de estas cosas:

1. MariaDB no esta arrancada.
2. El puerto del `.env` no coincide con el puerto real.
3. El usuario/password no son correctos.
4. La base de datos no existe.

Comprobar si hay servicio escuchando en el puerto:

```bat
netstat -ano | findstr :13306
netstat -ano | findstr :3306
netstat -ano | findstr :3307
```

Probar conexion manual:

```bat
mariadb -h 127.0.0.1 -P 13306 -u inv_user -pinv_password inversiones_ia
```

Ajustar el puerto en el `.env` y reiniciar `uvicorn`.

## 9. Flujo de trabajo recomendado

Antes de empezar:

```bat
git pull
```

Despues de cambios locales:

```bat
git status
git add .
git commit -m "Descripcion del cambio"
git push
```
