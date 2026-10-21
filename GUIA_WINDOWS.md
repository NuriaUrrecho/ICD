# Pruebas completas en Windows 11

Esta fase no necesita Proxmox. Docker crea cuatro contenedores locales: dos Apache, Flask y MariaDB.

## 1. Instalar Docker Desktop

1. Instala Docker Desktop para Windows.
2. Activa el backend WSL 2 y los contenedores Linux.
3. Abre Docker Desktop y espera a que indique que el motor está iniciado.
4. Abre PowerShell en la carpeta del proyecto.

Comprueba la instalación:

```powershell
docker version
docker compose version
```

## 2. Configurar secretos locales

```powershell
Copy-Item .env.compose.example .env
notepad .env
```

En `.env` escribe tu nombre y sustituye `DB_PASSWORD` y `SECRET_KEY`. Puedes generar la clave de Flask así:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

No subas `.env` a GitHub.

## 3. Construir y arrancar

```powershell
docker compose config
docker compose up --build -d
docker compose ps
```

Espera hasta que `mv1`, `mv2`, `db` y `mv3` aparezcan como `healthy`.

Abre:

- <http://localhost:8081> - Apache de MV1.
- <http://localhost:8082> - Apache de MV2.
- <http://localhost:5000> - Tablón Flask.
- <http://localhost:5000/health> - conexión real con MariaDB.
- <http://localhost:5000/api/avisos> - datos JSON.

## 4. Probar la interfaz

1. Publica un aviso con título, descripción, categoría y prioridad.
2. Comprueba que aparece con fecha y etiqueta de prioridad.
3. Filtra por categoría y prioridad.
4. Actualiza la página: el aviso debe persistir en MariaDB.
5. Elimina el aviso y confirma que desaparece.
6. Intenta enviar campos vacíos: debe aparecer un mensaje de error.

## 5. Ejecutar la prueba CRUD de la API

```powershell
powershell -ExecutionPolicy Bypass -File .\pruebas\probar_api.ps1
```

El script crea, consulta, actualiza, filtra y elimina un aviso temporal. Debe terminar con `Todas las pruebas CRUD han pasado`.

## 6. Comprobar MariaDB directamente

El endpoint `/health` ejecuta una consulta SQL. Como comprobación adicional:

```powershell
$line = Get-Content .env | Where-Object { $_ -match '^DB_PASSWORD=' }
$env:DB_PASSWORD = $line.Substring('DB_PASSWORD='.Length)
docker compose exec -e MYSQL_PWD=$env:DB_PASSWORD db mariadb -u avisos_app cpd_avisos -e "SELECT COUNT(*) AS avisos FROM avisos;"
Remove-Item Env:DB_PASSWORD
```

Si cambiaste `DB_USER` o `DB_NAME`, adapta el comando.

## 7. Pruebas Python aisladas

Estas pruebas utilizan una base SQLite temporal para comprobar rutas y validación, sin sustituir la prueba real con MariaDB:

```powershell
cd mv3
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -q
deactivate
cd ..
```

## 8. Diagnóstico

```powershell
docker compose ps
docker compose logs --tail 100 mv3
docker compose logs --tail 100 db
docker compose config
```

Si cambiaste el esquema y conservas datos antiguos, reinicia deliberadamente la base:

```powershell
docker compose down -v
docker compose up --build -d
```

`down -v` elimina el volumen local de MariaDB; no lo uses si necesitas conservar sus datos.

## 9. Parar el entorno

```powershell
docker compose down
```

Este comando conserva la base de datos. Para volver a arrancar: `docker compose up -d`.
