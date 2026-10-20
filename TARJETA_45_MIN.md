# Tarjeta rápida: práctica en 45 minutos

## Preparación obligatoria en casa

1. Edita `datos.conf` y escribe tu nombre después de `NOMBRE_ESTUDIANTE=`.
2. Sube todo a un repositorio con nombre corto, por ejemplo `P4`.
3. Anota en papel la URL corta del repositorio y los datos de red asignados.
4. Pregunta si hay una plantilla de Ubuntu ya instalada que pueda clonarse. Con 45 minutos, instalar tres sistemas desde ISO puede consumir casi todo el tiempo.

## Orden recomendado en el laboratorio

### Minutos 0-10: crear las tres MV

- Crea MV1 y MV2 con 1 vCPU, 1 GiB RAM y 10 GiB.
- Crea MV3 con 2 vCPU, 2 GiB RAM y 20 GiB.
- Introduce las MAC, bridge y VLAN entregadas por el profesor.
- Si existe una plantilla autorizada, haz tres clones completos y arráncalos. Si debes usar ISO, inicia las tres instalaciones en paralelo y alterna entre consolas.

### Minutos 10-20: red y proyecto

Configura la IP asignada durante la instalación o con Netplan. Comprueba `ip -br a` y el gateway.

En cada MV solo hay que teclear estas órdenes, sustituyendo la URL:

```text
sudo apt update
sudo apt install -y git
git clone URL_DEL_REPOSITORIO P4
cd P4
```

### Minutos 20-30: instalación en paralelo

En MV1:

```text
sudo bash instalar.sh 1
```

En MV2:

```text
sudo bash instalar.sh 2
```

En MV3:

```text
sudo bash instalar.sh 3
```

Pulsa Enter para aceptar la IP detectada. Solo MV3 pide inventar y repetir mentalmente una contraseña para MariaDB; no se muestra al escribir. Deja las instalaciones trabajando simultáneamente cambiando de consola.

### Minutos 30-38: comprobaciones mínimas

Teclea desde cualquier equipo que tenga acceso:

```text
curl -I http://IP_MV1
curl -I http://IP_MV2
curl http://IP_MV3:5000/api/health
```

Resultados: `200 OK`, `200 OK` y `database connected`. Abre también las tres direcciones en el navegador.

### Minutos 38-45: demostración y capturas

1. Captura las dos portadas Apache.
2. En MV3 crea un equipo, búscalo, edítalo y elimínalo.
3. Captura `/api/health` y los servicios activos.
4. Captura una prueba de comunicación entre máquinas.

## Si algo falla

En MV1/MV2:

```text
sudo systemctl restart apache2
sudo systemctl status apache2
```

En MV3:

```text
sudo systemctl restart mariadb inventario-mv3
sudo systemctl status inventario-mv3
```

No pierdas tiempo reinstalando inmediatamente: lee la última línea en rojo del estado y revisa primero IP, gateway y conexión a Internet.

