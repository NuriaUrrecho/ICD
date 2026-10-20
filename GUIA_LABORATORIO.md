# Guía de despliegue en el laboratorio

Si solo dispones de 45 minutos y no puedes pegar órdenes, sigue primero `TARJETA_45_MIN.md`. Esta guía larga queda como referencia y para resolver incidencias.

> Antes de desplegar, comunica al profesor las características de la aplicación de inventario y los segmentos de red previstos. El enunciado indica penalización si no se consensúan. Usa únicamente la IP, máscara, gateway, DNS, MAC, bridge/VLAN y número de puesto asignados; los marcadores de esta guía no son valores reales.

## Hoja de datos que debes completar

| Dato | MV1 | MV2 | MV3 |
|---|---|---|---|
| VMID | `<VMID_MV1>` | `<VMID_MV2>` | `<VMID_MV3>` |
| Nombre | `<HOST_MV1>` | `<HOST_MV2>` | `<HOST_MV3>` |
| IP/prefijo | `<IP_MV1>/<CIDR>` | `<IP_MV2>/<CIDR>` | `<IP_MV3>/<CIDR>` |
| MAC asignada | `<MAC_MV1>` | `<MAC_MV2>` | `<MAC_MV3>` |
| Bridge | `<BRIDGE>` | `<BRIDGE>` | `<BRIDGE>` |
| VLAN (si procede) | `<VLAN>` | `<VLAN>` | `<VLAN>` |
| Interfaz en Ubuntu | `<INTERFAZ_MV1>` | `<INTERFAZ_MV2>` | `<INTERFAZ_MV3>` |

Consulta al profesor cómo aplicar el anexo de MAC reservadas a las tres MV: el documento vincula la reserva con grupo y número de ordenador, pero no conviene deducir direcciones adicionales.

## 1. Crear las tres máquinas en Proxmox VE

Repite el proceso para MV1, MV2 y MV3:

1. Sube o selecciona la ISO de Ubuntu Server indicada por el profesor.
2. Pulsa **Create VM** y usa el VMID y nombre de tu hoja de datos.
3. Selecciona la ISO, firmware y controlador recomendados por el laboratorio. Mantén QEMU Guest Agent activado si la imagen lo admite.
4. Crea el disco y la interfaz de red con los datos siguientes.
5. Arranca la MV, instala Ubuntu Server y crea un usuario administrador con `sudo`.
6. Instala el agente si se usa en el laboratorio: `sudo apt update && sudo apt install -y qemu-guest-agent && sudo systemctl enable --now qemu-guest-agent`.

## 2. CPU, RAM y disco

Valores iniciales prudentes, sujetos a los límites del laboratorio:

| MV | vCPU | RAM | Disco | Motivo |
|---|---:|---:|---:|---|
| MV1 | 1 | 1 GiB | 10 GiB | Apache estático |
| MV2 | 1 | 1 GiB | 10 GiB | Apache estático |
| MV3 | 2 | 2 GiB | 20 GiB | Flask, Gunicorn y MariaDB |

Usa thin provisioning si el profesor lo permite. Si Ubuntu o MariaDB muestran presión de memoria, aumenta MV3 a 4 GiB; no sobredimensiones sin consultar la capacidad del nodo.

## 3. Red con parámetros asignados

### En Proxmox

En **Hardware > Network Device** de cada MV:

1. Selecciona `<BRIDGE>` y `<VLAN>` si se ha indicado.
2. Introduce exactamente su `<MAC_MVx>` reservada.
3. Usa el modelo recomendado por el laboratorio, normalmente VirtIO.

### En Ubuntu Server

Identifica el nombre real con `ip -br link`; no asumas que es `ens18`. Edita el YAML existente en `/etc/netplan/`:

```yaml
network:
  version: 2
  ethernets:
    <INTERFAZ_MVx>:
      dhcp4: false
      addresses:
        - <IP_MVx>/<CIDR>
      routes:
        - to: default
          via: <GATEWAY>
      nameservers:
        addresses: [<DNS_1>, <DNS_2>]
```

Valida primero con `sudo netplan try`; confirma solo si conserva conectividad. Después usa `sudo netplan apply`, `ip -br address`, `ip route` y `ping -c 3 <GATEWAY>`. Si el laboratorio usa DHCP con reserva por MAC, conserva `dhcp4: true` y no declares una IP estática.

## 4. Transferir el proyecto

### Opción A: GitHub

Desde cada MV (preferiblemente con repositorio privado si hay datos personales):

```bash
sudo apt update && sudo apt install -y git
git clone <URL_REPOSITORIO> practica4
cd practica4
```

No subas `.env`, contraseñas ni claves. Si el repositorio es privado, usa un token de alcance mínimo o una clave SSH temporal siguiendo las reglas del laboratorio.

### Opción B: SCP desde Windows

En PowerShell, desde la raíz del proyecto:

```powershell
scp -r .\mv1 USUARIO@IP_MV1:/home/USUARIO/practica4/
scp -r .\mv2 USUARIO@IP_MV2:/home/USUARIO/practica4/
scp -r .\mv3 USUARIO@IP_MV3:/home/USUARIO/practica4/
```

Sustituye cada marcador. Verifica luego con `find ~/practica4 -maxdepth 2 -type f`.

## 5. Ejecutar los instaladores

Haz ejecutables los scripts y pasa los valores reales entre comillas:

**MV1**

```bash
cd ~/practica4/mv1
chmod +x instalar_mv1.sh
sudo ./instalar_mv1.sh --student "NOMBRE APELLIDOS" --ip "IP_MV1"
```

**MV2**

```bash
cd ~/practica4/mv2
chmod +x instalar_mv2.sh
sudo ./instalar_mv2.sh --student "NOMBRE APELLIDOS" --ip "IP_MV2"
```

**MV3**

```bash
cd ~/practica4/mv3
chmod +x instalar_mv3.sh
sudo ./instalar_mv3.sh --student "NOMBRE APELLIDOS" --ip "IP_MV3"
```

MV3 pedirá la contraseña nueva de MariaDB sin mostrarla. No la pongas en la línea de comandos, en la memoria ni en una captura. El instalador crea `/etc/inventario-mv3.env` con acceso restringido y un servicio `systemd`.

Si se activa un firewall, abre únicamente lo necesario y de acuerdo con el laboratorio: HTTP 80 en MV1/MV2 y TCP 5000 en MV3. MariaDB queda ligada al host local y no necesita el puerto 3306 accesible desde la red.

## 6. Comprobar Apache en MV1

```bash
systemctl is-active apache2
apache2ctl configtest
curl -I http://127.0.0.1/
```

Desde otra MV o el puesto: `curl -I http://IP_MV1/`. Debe responder `HTTP/1.1 200 OK`. Abre la URL y comprueba asignatura, estudiante, IP y “MV1”.

## 7. Comprobar Apache en MV2

Ejecuta las mismas tres órdenes en MV2 y visita `http://IP_MV2/`. Debe responder 200, mostrar los datos correctos y un diseño claramente diferente al de MV1.

## 8. Comprobar Flask y MariaDB en MV3

```bash
systemctl is-active mariadb inventario-mv3
sudo systemctl status inventario-mv3 --no-pager
curl -s http://127.0.0.1:5000/api/health
```

Se espera `{"database":"connected","status":"ok"}`. Visita `http://IP_MV3:5000/`, crea, busca, edita y elimina un equipo. Si falla:

```bash
sudo journalctl -u inventario-mv3 -n 100 --no-pager
sudo mariadb -e "SHOW DATABASES;"
ss -lntp | grep -E ':5000|:3306'
```

## 9. Comunicación entre las tres MV

Desde cada MV registra:

```bash
ip -br address
ip route
ping -c 3 IP_DE_OTRA_MV
```

Además:

- Desde MV1: `curl -I http://IP_MV2/` y `curl -s http://IP_MV3:5000/api/health`.
- Desde MV2: `curl -I http://IP_MV1/` y `curl -s http://IP_MV3:5000/api/health`.
- Desde MV3: `curl -I http://IP_MV1/` y `curl -I http://IP_MV2/`.

Un ping bloqueado no demuestra por sí solo un fallo: confirma los puertos de aplicación con `curl`. Revisa bridge, VLAN, máscara, ruta y firewall si no hay comunicación.

## 10. Capturas para la memoria

Obtén capturas legibles, recortando secretos y datos no necesarios:

1. Resumen de hardware de cada MV en Proxmox.
2. Configuración de red/MAC de cada MV, solo si el profesor permite publicarla.
3. `ip -br address` y `ip route` de las tres MV.
4. Portada MV1 y portada MV2 completas.
5. Inicio de MV3 con identidad del servidor.
6. Alta, listado, búsqueda, edición y eliminación en el inventario.
7. `/api/health` y ejecución satisfactoria de pruebas CRUD.
8. Estados `active` de Apache, MariaDB y `inventario-mv3`.
9. Pruebas `curl` entre las tres máquinas.

Para la entrega, el enunciado también pide antecedentes sobre virtualización y metodología Proxmox, validación de los tres servicios, anexos con prompts/referencias, tabla de contenido, tabla de figuras, glosario y bibliografía. Confirma con el profesor el título exacto: el documento mezcla “Máquinas Virtuales” con un título de almacenamiento masivo que parece heredado de otra práctica.
