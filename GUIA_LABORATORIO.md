# Guía de laboratorio con Proxmox VE

Esta guía debe usarse solo cuando se conozcan los datos reales de red. No reutiliza las direcciones de otros estudiantes.

## 1. Consenso previo con el profesor

Comunica exactamente:

1. **SGBD:** MariaDB, instalado en MV3 y accesible únicamente desde la propia MV3.
2. **Aplicación:** Tablón de Avisos del CPD en Flask; lista, publica, filtra y elimina avisos guardados en MariaDB, expone `/health` y `/api/avisos`.
3. **Servidor:** contenedor LXC Debian MV3, servido con Gunicorn en el puerto 5000.
4. **Red:** tres contenedores en el segmento que autorice el profesor, conectados al bridge y VLAN que indique.

El enunciado advierte de una penalización si no se consensúan la aplicación y los segmentos de red.

## 2. Crear los tres contenedores

Usa **Create CT**, plantilla Debian, contenedores no privilegiados y los recursos de `ARQUITECTURA.md`. Activa `Start at boot`.

En la pestaña Network introduce únicamente:

- interfaz `eth0`;
- MAC reservada para esa máquina, si el profesor la ha asignado;
- bridge y VLAN autorizados;
- IP/prefijo y gateway confirmados, o DHCP si la reserva funciona mediante DHCP;
- DNS indicado por el laboratorio.

No asignes la misma MAC a dos contenedores.

## 3. Verificar la red antes de instalar

En cada contenedor:

```bash
ip -br address
ip route
getent hosts deb.debian.org
ping -c 3 IP_DE_OTRO_CONTENEDOR
```

Si falla, revisa bridge, VLAN, máscara, gateway y DNS antes de ejecutar `apt`.

## 4. Transferir e instalar

Sigue `INSTALACION.md`. En resumen:

```bash
git clone https://github.com/NuriaUrrecho/ICD.git practica4
cd practica4
sudo bash instalar.sh 1   # solo en MV1
sudo bash instalar.sh 2   # solo en MV2
sudo bash instalar.sh 3   # solo en MV3
```

El lanzador solicita o detecta los valores necesarios. La contraseña de MariaDB se introduce sin mostrarse.

## 5. Validación rápida

En MV1 y MV2:

```bash
systemctl is-enabled apache2
systemctl is-active apache2
apache2ctl configtest
curl -I http://127.0.0.1/
```

En MV3:

```bash
systemctl is-enabled mariadb tablon-cpd
systemctl is-active mariadb tablon-cpd
curl -s http://127.0.0.1:5000/health
curl -s http://127.0.0.1:5000/api/avisos
```

Desde el puesto abre `http://IP_MV1/`, `http://IP_MV2/` y `http://IP_MV3:5000/`. Publica un aviso y recarga la página para demostrar persistencia.

## 6. Comunicación entre contenedores

- MV1: `curl -I http://IP_MV2/` y `curl -s http://IP_MV3:5000/health`.
- MV2: `curl -I http://IP_MV1/` y `curl -s http://IP_MV3:5000/health`.
- MV3: `curl -I http://IP_MV1/` y `curl -I http://IP_MV2/`.

## 7. Reinicio

Reinicia los tres contenedores y repite `systemctl is-active` y las peticiones HTTP. Este paso demuestra el arranque automático.

## 8. Evidencias

Usa `CHECKLIST.md`. Oculta contraseñas, tokens y cualquier dato sensible que no sea necesario para evaluar la práctica.
