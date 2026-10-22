# Proxmox local

Este directorio contiene los artefactos reproducibles del laboratorio Proxmox anidado.

- Proxmox VE se ejecuta en VirtualBox con NAT.
- La interfaz web se publica en `https://localhost:8006`.
- Los contenedores LXC son 101 (MV1), 102 (MV2) y 103 (MV3).
- Las aplicaciones se publican en `http://localhost:8081`, `http://localhost:8082` y `http://localhost:5000`.
- La red interna de los contenedores es `10.10.10.0/24`, aislada del entorno universitario.

Las ISO, los discos virtuales y los archivos con credenciales locales están ignorados por Git.

## Estado comprobado

El 22/10/2026 el entorno se ejecutó de extremo a extremo: Apache respondió en CT101 y CT102, Flask y MariaDB respondieron en CT103, la API CRUD pasó sus pruebas y los servicios volvieron a quedar disponibles después de reiniciar Proxmox.
