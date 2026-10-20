# Guía mínima para hacer la práctica a mano

## Antes del laboratorio

Lleva apuntados tu nombre y los datos de red entregados por el profesor: IP, máscara, gateway, DNS, MAC y bridge.

Pregunta si puedes clonar una plantilla Ubuntu. Instalar tres Ubuntu desde cero puede ocupar los 45 minutos completos.

## MV1

Configura primero la red. Después escribe:

```bash
sudo apt update
sudo apt install -y apache2
N="NOMBRE APELLIDOS"
IP=$(hostname -I | awk '{print $1}')
echo "<h1>Infraestructura Informatica para CPD</h1><p>$N</p><p>IP: $IP</p><p>MV1</p>" | sudo tee /var/www/html/index.html
```

Comprueba:

```bash
curl localhost
```

## MV2

Configura primero la red. Después escribe:

```bash
sudo apt update
sudo apt install -y apache2
N="NOMBRE APELLIDOS"
IP=$(hostname -I | awk '{print $1}')
echo "<h1>Infraestructura Informatica para CPD</h1><p>$N</p><p>IP: $IP</p><p>MV2</p>" | sudo tee /var/www/html/index.html
```

Comprueba:

```bash
curl localhost
```

## MV3

### 1. Instalar Flask y MariaDB

```bash
sudo apt update
sudo apt install -y mariadb-server python3-flask python3-pymysql
```

### 2. Crear la base de datos

```bash
U=$(whoami)
sudo mariadb -e "CREATE DATABASE avisos; CREATE USER '$U'@'localhost' IDENTIFIED VIA unix_socket; GRANT ALL ON avisos.* TO '$U'@'localhost'; CREATE TABLE avisos.avisos(texto VARCHAR(100)); INSERT INTO avisos.avisos VALUES('Mantenimiento programado');"
```

Comprueba:

```bash
mariadb avisos -e "SELECT * FROM avisos;"
```

### 3. Crear Flask

Abre el editor:

```bash
nano app.py
```

Escribe exactamente:

```python
from flask import Flask
import pymysql,getpass,os
app=Flask(__name__)

@app.route('/')
def inicio():
    db=pymysql.connect(unix_socket='/run/mysqld/mysqld.sock',user=getpass.getuser(),database='avisos')
    c=db.cursor()
    c.execute('SELECT texto FROM avisos')
    avisos=', '.join(x[0] for x in c.fetchall())
    return '<h1>Tablon de avisos del CPD</h1><p>'+os.getenv('NOMBRE')+'</p><p>IP: '+os.getenv('IP')+'</p><p>MV3 - Flask y MariaDB</p><p>Avisos: '+avisos+'</p>'

app.run(host='0.0.0.0',port=5000)
```

Guarda con `Ctrl+O`, pulsa `Enter` y sal con `Ctrl+X`.

### 4. Arrancar Flask

```bash
NOMBRE="NOMBRE APELLIDOS" IP=$(hostname -I | awk '{print $1}') nohup python3 app.py >/tmp/flask.log 2>&1 &
curl localhost:5000
```

Si no funciona:

```bash
cat /tmp/flask.log
```

## Comprobación final

Desde un equipo que pueda comunicarse con las tres MV:

```bash
curl http://IP_MV1
curl http://IP_MV2
curl http://IP_MV3:5000
```

Debes ver:

- MV1: asignatura, nombre, IP y MV1.
- MV2: asignatura, nombre, IP y MV2.
- MV3: nombre, IP, MV3 y `Mantenimiento programado` leído desde MariaDB.

Haz una captura de cada página y otra del comando `SELECT * FROM avisos;`.
