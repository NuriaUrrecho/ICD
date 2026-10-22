# Resultados de las pruebas locales

**Fechas:** 21-22/10/2026
**Sistemas:** Windows 11 con Docker Desktop 4.96.0 / motor Docker 29.9.1, y Proxmox VE 9.2.2 anidado en VirtualBox.

## Resultado global

El laboratorio local quedó operativo con los cuatro servicios en estado `healthy`:

- `mv1`: Apache, publicado en <http://localhost:8081>;
- `mv2`: Apache, publicado en <http://localhost:8082>;
- `mv3`: Flask/Gunicorn, publicado en <http://localhost:5000>;
- `db`: MariaDB 11.4.13, accesible únicamente desde la red interna de Compose.

## Comprobaciones superadas

| Comprobación | Resultado observado |
|---|---|
| Página MV1 | HTTP 200; asignatura, estudiante, IP configurable e identificación MV1 |
| Página MV2 | HTTP 200; información obligatoria y diseño diferente de MV1 |
| Página Flask | carga correcta y muestra ocho avisos iniciales |
| Estado de la base de datos | `/health` devuelve estado correcto y conexión real |
| Datos iniciales | consulta SQL devuelve exactamente ocho avisos |
| Alta por API | aviso creado y devuelto con identificador |
| Lectura por API | aviso recuperado correctamente |
| Modificación por API | cambios guardados en MariaDB |
| Filtros | categoría y prioridad devuelven las coincidencias esperadas |
| Eliminación por API | aviso eliminado y deja de estar disponible |
| Persistencia | un aviso sobrevivió a `docker compose down` y al nuevo arranque |
| Pruebas Python | `4 passed, 1 skipped` |
| Revisión visual | las tres interfaces se visualizaron correctamente |

La prueba Python omitida es una variante opcional que requiere indicar manualmente una URL MariaDB externa. La misma integración se verificó directamente contra el MariaDB real del laboratorio Docker mediante el script CRUD, `/health` y una consulta SQL.

## Ejecución completada en Proxmox local

Además, se creó y comprobó un entorno Proxmox VE local anidado en VirtualBox, sin utilizar red ni valores de un laboratorio universitario:

- Proxmox VE 9.2.2 disponible en `https://localhost:8006`.
- Contenedores LXC Debian 13 reales: `101` (`web1-cpd`), `102` (`web2-cpd`) y `103` (`tablon-cpd`).
- Red privada `10.10.10.0/24`: `10.10.10.11`, `10.10.10.12` y `10.10.10.13` respectivamente.
- Apache activo en CT101 y CT102; `tablon-cpd` y MariaDB activos en CT103.
- Publicación local verificada: MV1 en el puerto `8081`, MV2 en el `8082` y Flask/MariaDB en el `5000`.
- El script `probar_api.ps1` superó CREATE, READ, UPDATE, filtro y DELETE contra la MariaDB de CT103.
- Comunicación interna comprobada: CT101→CT102, CT102→CT103 y CT103→CT101.
- Tras un reinicio normal de Proxmox, los tres CT y sus servicios arrancaron de nuevo; las tres URLs devolvieron HTTP 200.

La configuración real de MAC, bridge, VLAN, IP, gateway y DNS que asigne un profesor, si fuera necesaria en otro entorno, sigue estando documentada en `GUIA_LABORATORIO.md`.
