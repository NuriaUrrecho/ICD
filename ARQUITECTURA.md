# Arquitectura propuesta

## Componentes

| Rol | Hostname propuesto | Servicio | Puerto | Recursos |
|---|---|---|---:|---|
| MV1 | `web1-cpd` | Apache 2.4 | 80 | 1 vCPU, 512 MiB RAM, 8 GiB |
| MV2 | `web2-cpd` | Apache 2.4 | 80 | 1 vCPU, 512 MiB RAM, 8 GiB |
| MV3 | `tablon-cpd` | Flask/Gunicorn + MariaDB | 5000; 3306 solo local | 2 vCPU, 1 GiB RAM, 10 GiB |

## Laboratorio local con Docker

```text
Navegador Windows
  |-- localhost:8081 --> Apache MV1
  |-- localhost:8082 --> Apache MV2
  `-- localhost:5000 --> Flask MV3 --> MariaDB:3306
```

Docker proporciona una red privada interna por nombre de servicio. MariaDB no publica el puerto 3306 al anfitrión.

## Proxmox

```text
Equipo cliente
      |
bridge/VLAN autorizados
      |
Proxmox VE
  |-- CT MV1 / Apache
  |-- CT MV2 / Apache
  `-- CT MV3 / Gunicorn + Flask + MariaDB local
```

Las IP, MAC, máscara, gateway, DNS, bridge y VLAN quedan como datos pendientes hasta conocer el entorno. La guía oficial reserva MAC según horario y número de puesto en el laboratorio, pero no define tres reservas por estudiante; por ello debe confirmarse con el profesor cómo aplicarlas.

## Decisiones

- LXC reduce consumo y es suficiente para servicios Linux.
- MariaDB y Flask comparten MV3 porque el enunciado exige tres máquinas y no una cuarta para la base de datos.
- MariaDB escucha localmente; la aplicación se conecta mediante `127.0.0.1` en Proxmox y mediante el nombre `db` en Docker.
- Gunicorn ejecuta Flask como servicio `systemd`; no se usa el servidor de desarrollo en despliegue.
- Las credenciales se proporcionan mediante variables de entorno y no se guardan en Git.

## Datos pendientes

- Plataforma Proxmox definitiva y versión.
- Plantilla Debian autorizada.
- Segmento de red, bridge/VLAN, IP, MAC, gateway y DNS.
- Límites de recursos del nodo.
