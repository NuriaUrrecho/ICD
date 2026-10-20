# Pruebas desde Windows 11

## Opción recomendada: Docker Desktop

### 1. Preparación

1. Instala Docker Desktop para Windows y usa contenedores Linux (backend WSL 2).
2. Abre PowerShell en la raíz del proyecto.
3. Crea la configuración local:

   ```powershell
   Copy-Item .env.compose.example .env
   notepad .env
   ```

4. Sustituye `STUDENT_NAME`, las tres IP descriptivas, `DB_PASSWORD` y `SECRET_KEY`. Para generar una clave segura:

   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

   En casa las IP pueden ser etiquetas como `localhost:8081`; en el laboratorio usa las IP asignadas. El archivo `.env` está excluido de Git.

### 2. Arranque

```powershell
docker compose config
docker compose up --build -d
docker compose ps
```

Espera hasta que `db`, `mv1`, `mv2` y `mv3` aparezcan como `healthy`. Si un contenedor falla, consulta `docker compose logs --tail 100 nombre_del_servicio`.

Servicios locales:

| Servicio | URL | Resultado esperado |
|---|---|---|
| Apache simulado MV1 | <http://localhost:8081> | Diseño azul, estudiante, IP y “MV1 · Apache” |
| Apache simulado MV2 | <http://localhost:8082> | Diseño claro distinto, estudiante, IP y “MV2” |
| Flask MV3 | <http://localhost:5000> | Inventario en español y datos de estudiante/IP |
| Estado MV3 | <http://localhost:5000/api/health> | `{"database":"connected","status":"ok"}` |

Nginx se usa únicamente como sustituto ligero de Apache en la prueba doméstica de las páginas estáticas. Los instaladores del laboratorio sí usan Apache.

### 3. CRUD web

1. En MV3, pulsa **Registrar equipo**.
2. Completa todos los campos obligatorios y guarda.
3. Busca el equipo por nombre, marca, modelo, serie o ubicación.
4. Edita su estado y verifica el cambio.
5. Elimínalo y confirma que desaparece.
6. Prueba una IP inválida y un número de serie repetido: la aplicación debe rechazarlos.

### 4. API REST automatizada

```powershell
powershell -ExecutionPolicy Bypass -File .\pruebas\probar_api.ps1
```

El script crea un equipo temporal, lo lee, actualiza, busca y elimina. Debe terminar con “Todas las pruebas CRUD han pasado”. Para probar una MV real:

```powershell
.\pruebas\probar_api.ps1 -BaseUrl http://IP_MV3:5000
```

Endpoints disponibles:

| Método | Ruta | Función |
|---|---|---|
| GET | `/api/health` | Salud de Flask y conexión SQL |
| GET | `/api/equipos?q=texto` | Listar y buscar |
| POST | `/api/equipos` | Crear |
| GET | `/api/equipos/<id>` | Consultar uno |
| PUT / PATCH | `/api/equipos/<id>` | Sustituir / modificar |
| DELETE | `/api/equipos/<id>` | Eliminar |

### 5. Conexión directa a MariaDB

El endpoint `/api/health` ya ejecuta `SELECT 1`. Para una segunda comprobación dentro del contenedor, carga la contraseña desde `.env` en la sesión y ejecuta el cliente sin imprimirla:

```powershell
$line = Get-Content .env | Where-Object { $_ -match '^DB_PASSWORD=' }
$env:DB_PASSWORD = $line.Substring('DB_PASSWORD='.Length)
docker compose exec -e MYSQL_PWD=$env:DB_PASSWORD db mariadb -u inventario_app inventario -e "SELECT 1; SELECT COUNT(*) AS equipos FROM equipos;"
Remove-Item Env:DB_PASSWORD
```

Si cambiaste `DB_USER` o `DB_NAME`, sustitúyelos en el comando. Se esperan dos resultados sin errores y una tabla `equipos` accesible.

### 6. Pruebas Python aisladas

Estas pruebas usan SQLite temporal y no requieren MariaDB; verifican rutas, validación y CRUD de la API:

```powershell
cd mv3
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -q
cd ..
```

Para incluir la prueba real de MariaDB, define una URL de prueba antes de ejecutar `pytest` (no la guardes en Git):

```powershell
$env:MARIADB_TEST_URL = "mysql+pymysql://USUARIO:CONTRASENA@127.0.0.1:3306/inventario"
python -m pytest -q
Remove-Item Env:MARIADB_TEST_URL
```

### 7. Parada y limpieza

`docker compose down` detiene el entorno y conserva los datos. `docker compose down -v` elimina también el volumen de MariaDB; úsalo solo si quieres reiniciar deliberadamente la base de datos.

## Matriz de resultados esperados

| Prueba | Resultado correcto |
|---|---|
| Contenedores | Cuatro servicios `healthy` |
| Portadas | HTTP 200, estilos distintos, datos configurados |
| Salud API | HTTP 200 y `database: connected` |
| Alta | HTTP 201 y objeto con `id` |
| Lectura/listado | HTTP 200 y datos creados |
| Edición | HTTP 200 y campos modificados |
| Búsqueda | Solo coincidencias; `total` correcto |
| Eliminación | HTTP 204; consulta posterior HTTP 404 |
| Validación | HTTP 400 para datos/IP inválidos |
| Serie duplicada | HTTP 409 |
| MariaDB directa | `SELECT 1` devuelve `1` |

