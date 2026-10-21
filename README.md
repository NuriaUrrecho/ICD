# Práctica 4 - Máquinas virtuales con Proxmox VE

Proyecto original para la asignatura **Infraestructura Informática para Centros de Procesamiento de Datos (14541)** de la UPV.

La infraestructura está formada por:

- **MV1:** servidor Apache con una portada identificativa.
- **MV2:** segundo servidor Apache con diseño diferente.
- **MV3:** aplicación Flask **Tablón de Avisos del CPD**, conectada realmente a MariaDB.

## Prueba local en Windows

Requiere Docker Desktop con contenedores Linux. En PowerShell:

```powershell
Copy-Item .env.compose.example .env
notepad .env
docker compose up --build -d
docker compose ps
```

Servicios:

| Componente | URL local |
|---|---|
| MV1 - Apache | <http://localhost:8081> |
| MV2 - Apache | <http://localhost:8082> |
| MV3 - Flask | <http://localhost:5000> |
| Salud Flask/MariaDB | <http://localhost:5000/health> |
| API de avisos | <http://localhost:5000/api/avisos> |

Prueba automatizada de la API:

```powershell
powershell -ExecutionPolicy Bypass -File .\pruebas\probar_api.ps1
```

Consulta [GUIA_WINDOWS.md](GUIA_WINDOWS.md) para la preparación completa.

## Estado comprobado

El 21/10/2026 se verificó en Windows 11 el laboratorio completo: cuatro contenedores saludables, Apache MV1 y MV2 con HTTP 200, Flask conectado a MariaDB 11.4.13, CRUD completo y persistencia después de reiniciar Compose. El detalle reproducible está en [RESULTADOS_PRUEBAS.md](RESULTADOS_PRUEBAS.md).

## Estructura

```text
mv1/                 Apache 1, portada e instalador
mv2/                 Apache 2, portada e instalador
mv3/                 Flask, MariaDB, SQL, Gunicorn, pruebas e instalador
pruebas/              validación automatizada desde Windows
docker-compose.yml    laboratorio local reproducible
INSTALACION.md        despliegue paso a paso
VALIDACION.md         pruebas y resultados esperados
ARQUITECTURA.md       recursos y diseño de red
MEMORIA_PRACTICA.md   borrador original de la memoria
CHECKLIST.md          comprobaciones y capturas pendientes
RESULTADOS_PRUEBAS.md resultados reales del laboratorio local
```

## Despliegue posterior

En cada contenedor Debian/Ubuntu se clona o copia el repositorio y se ejecuta:

```bash
sudo bash instalar.sh 1
sudo bash instalar.sh 2
sudo bash instalar.sh 3
```

Los valores reales de red deben consensuarse con el profesor antes de configurar Proxmox. Los scripts no fijan IP, gateway, DNS ni MAC universitarias.

## Seguridad

El repositorio no contiene contraseñas reales. `.env` está ignorado. El instalador de MV3 solicita la contraseña de MariaDB sin mostrarla y guarda las variables con permisos restringidos.
