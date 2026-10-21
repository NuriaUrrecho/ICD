# Validación

No marques una prueba como superada sin ejecutarla en el entorno correspondiente.

## Pruebas locales

| ID | Comprobación | Orden o URL | Resultado esperado |
|---|---|---|---|
| L01 | Servicios | `docker compose ps` | cuatro servicios `healthy` |
| L02 | Apache 1 | <http://localhost:8081> | HTTP 200, asignatura, estudiante, IP y MV1 |
| L03 | Apache 2 | <http://localhost:8082> | HTTP 200, contenido obligatorio y diseño distinto |
| L04 | Flask | <http://localhost:5000> | tablón y ocho avisos iniciales |
| L05 | MariaDB real | <http://localhost:5000/health> | `status=ok`, `database=connected` y versión MariaDB |
| L06 | API | <http://localhost:5000/api/avisos> | JSON válido con `items` y `total` |
| L07 | CRUD API | `pruebas/probar_api.ps1` | todas las comprobaciones `OK` |
| L08 | Persistencia | publicar, recargar y reiniciar | el aviso continúa presente |
| L09 | Filtros | categoría y prioridad | solo aparecen coincidencias |
| L10 | Validación | formulario incompleto | mensaje de error, sin inserción |

## Pruebas en cada contenedor Proxmox

```bash
hostname
ip -br address
ip route
systemctl --failed
```

MV1 y MV2:

```bash
systemctl is-enabled apache2
systemctl is-active apache2
apache2ctl configtest
curl -I http://127.0.0.1/
```

MV3:

```bash
systemctl is-enabled mariadb tablon-cpd
systemctl is-active mariadb tablon-cpd
curl -s http://127.0.0.1:5000/health
curl -s http://127.0.0.1:5000/api/avisos
sudo mariadb cpd_avisos -e "SELECT id,titulo,categoria,prioridad FROM avisos;"
```

## Conectividad cruzada

Desde cada contenedor ejecuta `ping -c 3 IP_OTRA_MV`. Además, comprueba los puertos de aplicación con `curl`, porque una red puede bloquear ICMP sin bloquear HTTP.

## Reinicio

```bash
reboot
```

Tras el arranque, repite las pruebas de estado y HTTP. El resultado correcto es que no sea necesario ejecutar manualmente Apache, MariaDB ni Gunicorn.

## Matriz de cumplimiento del baremo

| Criterio oficial | Implementación | Evidencia |
|---|---|---|
| Primer servidor web, 10 % | `mv1/`, Apache | L02 y servicio activo |
| Dos servidores web, 10 % | `mv1/` y `mv2/` | L02, L03 y diseños diferentes |
| Flask, 30 % | `mv3/tablon/`, Gunicorn | L04, alta/filtro/eliminación |
| Servicios y Flask correctos, 50 % | Compose, MariaDB, scripts y systemd | L01, L05-L10, conectividad y reinicio |

## Estado actual de validación

- Docker Desktop 4.96.0 instalado y motor Docker 29.9.1 operativo.
- Los cuatro servicios del laboratorio local están en estado `healthy`.
- MV1 y MV2 responden con HTTP 200 desde Apache y muestran los datos obligatorios.
- Flask consulta una instancia real de MariaDB 11.4.13 y carga los ocho avisos iniciales.
- CRUD completo de la API superado: crear, leer, actualizar, filtrar y eliminar.
- Persistencia superada: un aviso creado continuó disponible después de `docker compose down` y un nuevo arranque.
- Pruebas Python: `4 passed, 1 skipped`. La prueba omitida es la variante opcional que requiere proporcionar manualmente una URL externa; la integración equivalente se comprobó contra el MariaDB de Docker.
- Inspección visual local de las tres páginas: superada.
- Proxmox y LXC validados: pendiente de disponer del entorno.
- Capturas del entorno Proxmox: pendientes; no se sustituyen por evidencias inventadas.
