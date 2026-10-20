# Práctica 4 - Máquinas virtuales

Proyecto preparado para la asignatura **Infraestructura Informática para Centros de Procesamiento de Datos (UPV, código 14541)**.

Incluye:

- `mv1/`: portada Apache de la primera máquina y su instalador.
- `mv2/`: portada Apache de la segunda máquina y su instalador.
- `mv3/`: inventario Flask + MariaDB, API REST, instalador y pruebas.
- `docker-compose.yml`: laboratorio local con los tres servicios y MariaDB.
- `GUIA_WINDOWS.md`: ejecución y validación en Windows 11.
- `GUIA_LABORATORIO.md`: despliegue posterior en Proxmox VE sin asumir datos de red.
- `TARJETA_45_MIN.md`: versión mínima para trabajar sin copiar y pegar.
- `instalar.sh`: lanzador único para las tres máquinas.

## Prueba rápida con Docker

1. Instala Docker Desktop y activa contenedores Linux.
2. Copia `.env.compose.example` como `.env` y cambia todos los valores marcados.
3. Ejecuta `docker compose up --build -d`.
4. Abre MV1 en <http://localhost:8081>, MV2 en <http://localhost:8082> y MV3 en <http://localhost:5000>.
5. Ejecuta `powershell -ExecutionPolicy Bypass -File .\pruebas\probar_api.ps1`.

Los detalles, resultados esperados y resolución de problemas están en `GUIA_WINDOWS.md`.

## Instalación rápida en el laboratorio

Después de clonar el repositorio, ejecuta en cada MV únicamente:

```bash
sudo bash instalar.sh 1  # MV1
sudo bash instalar.sh 2  # MV2
sudo bash instalar.sh 3  # MV3
```

El lanzador detecta la IP y lee el nombre desde `datos.conf`.

## Seguridad

No hay contraseñas reales en el repositorio. No confirmes en Git `.env`, claves privadas, volcados de la base de datos ni capturas que revelen credenciales. Los instaladores solicitan los secretos sin mostrarlos y los guardan con permisos restringidos.

