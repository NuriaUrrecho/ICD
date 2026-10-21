# Instalación y despliegue

## A. Entorno local

Sigue `GUIA_WINDOWS.md`. Es la forma recomendada de desarrollar y validar el proyecto antes de disponer de Proxmox.

## B. Datos que deben conocerse antes de tocar la red

Completa y consensúa con el profesor:

| Dato | MV1 | MV2 | MV3 |
|---|---|---|---|
| VMID | pendiente | pendiente | pendiente |
| Hostname | `web1-cpd` propuesto | `web2-cpd` propuesto | `tablon-cpd` propuesto |
| IP/prefijo | pendiente | pendiente | pendiente |
| MAC | pendiente | pendiente | pendiente |
| Bridge/VLAN | pendiente | pendiente | pendiente |
| Gateway y DNS | pendiente | pendiente | pendiente |

No reutilices una misma MAC en varias máquinas. En el laboratorio, aplica el anexo de reservas únicamente como indique el profesor.

## C. Crear los contenedores LXC

En la interfaz de Proxmox, repite **Create CT** usando una plantilla Debian compatible:

| Contenedor | vCPU | RAM | Swap | Disco | Arranque |
|---|---:|---:|---:|---:|---|
| MV1 / `web1-cpd` | 1 | 512 MiB | 256 MiB | 8 GiB | automático |
| MV2 / `web2-cpd` | 1 | 512 MiB | 256 MiB | 8 GiB | automático |
| MV3 / `tablon-cpd` | 2 | 1 GiB | 512 MiB | 10 GiB | automático |

Usa contenedores no privilegiados. Configura la interfaz únicamente con los datos confirmados. Arranca cada contenedor y verifica `ip -br address`, `ip route` y resolución DNS.

## D. Transferir el proyecto

Con Git:

```bash
apt-get update && apt-get install -y git
git clone https://github.com/NuriaUrrecho/ICD.git practica4
cd practica4
```

O desde Windows mediante SCP:

```powershell
scp -r .\mv1 root@IP_MV1:/root/practica4/
scp -r .\mv2 root@IP_MV2:/root/practica4/
scp -r .\mv3 root@IP_MV3:/root/practica4/
```

## E. Instalar los servicios

En MV1:

```bash
cd /root/practica4/mv1
chmod +x instalar_mv1.sh
./instalar_mv1.sh --student "NURIA URRECHO TORRES" --ip "IP_MV1"
```

En MV2:

```bash
cd /root/practica4/mv2
chmod +x instalar_mv2.sh
./instalar_mv2.sh --student "NURIA URRECHO TORRES" --ip "IP_MV2"
```

En MV3:

```bash
cd /root/practica4/mv3
chmod +x instalar_mv3.sh
./instalar_mv3.sh --student "NURIA URRECHO TORRES" --ip "IP_MV3"
```

El último script solicita una contraseña nueva sin mostrarla, instala MariaDB, crea `cpd_avisos`, carga ocho avisos, instala Flask y Gunicorn y habilita `tablon-cpd.service`.

## F. Arranque automático

Los instaladores ejecutan:

- `systemctl enable --now apache2` en MV1 y MV2.
- `systemctl enable --now mariadb tablon-cpd` en MV3.

Después de reiniciar cada contenedor, valida los servicios con el procedimiento de `VALIDACION.md`.
