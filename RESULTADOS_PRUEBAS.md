# Resultados de las pruebas locales

**Fecha:** 21/10/2026  
**Sistema:** Windows 11 con Docker Desktop 4.96.0 y motor Docker 29.9.1

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

## Pendiente exclusivamente del laboratorio Proxmox

No se afirma haber probado fuera de casa lo siguiente:

- creación y recursos reales de los tres contenedores LXC;
- MAC, bridge, VLAN, IP, gateway y DNS asignados por el profesor;
- servicios `systemd` en los contenedores Debian/Ubuntu;
- comunicación cruzada y reinicio dentro de Proxmox;
- capturas de pantalla del entorno Proxmox.

Estas comprobaciones dependen del acceso al laboratorio y están detalladas en `GUIA_LABORATORIO.md` y `CHECKLIST.md`.
