# Práctica completa a mano en 45 minutos

Esta versión prioriza el mínimo solicitado por el enunciado oficial: dos servidores Apache y una aplicación Flask comunicada con un SGBD. No intenta reproducir manualmente el inventario avanzado del repositorio.

## Antes de empezar

Lleva escritos en papel:

- Tu nombre y apellidos.
- IP, prefijo/máscara, gateway y DNS de cada MV.
- MAC de cada MV.
- Bridge y VLAN, si existen.

Pregunta si puedes clonar una plantilla Ubuntu. Sin plantilla, crear e instalar tres Ubuntu desde ISO en 45 minutos puede ser imposible.

## Reparto de tiempo

- 0-12 min: crear/arrancar las tres MV y configurar la red.
- 12-20 min: instalar Apache en MV1 y MV2 simultáneamente.
- 20-35 min: instalar MariaDB y Flask en MV3 y escribir `app.py`.
- 35-40 min: comprobar comunicación.
- 40-45 min: capturas.

## MV1 - Apache

Después de configurar la IP, escribe:

```bash
sudo apt update
sudo apt install -y apache2
NOMBRE="NOMBRE APELLIDOS"
IP=$(hostname -I | cut -d' ' -f1)
echo "<body style='font-family:sans-serif;background:#123;color:white;padding:10%'><h1>Infraestructura Informatica para CPD</h1><h2>MV1 - Apache</h2><p>Estudiante: $NOMBRE</p><p>IP: $IP</p></body>" | sudo tee /var/www/html/index.html
sudo systemctl enable --now apache2
curl http://localhost
```

## MV2 - Apache

Escribe las mismas órdenes, cambiando únicamente la página:

```bash
sudo apt update
sudo apt install -y apache2
NOMBRE="NOMBRE APELLIDOS"
IP=$(hostname -I | cut -d' ' -f1)
echo "<body style='font-family:serif;background:#eee;color:#222;padding:10%;border-top:20px solid orange'><h1>Infraestructura Informatica para CPD</h1><h2>MV2 - Apache</h2><p>Estudiante: $NOMBRE</p><p>IP: $IP</p></body>" | sudo tee /var/www/html/index.html
sudo systemctl enable --now apache2
curl http://localhost
```

## MV3 - Flask y MariaDB

### 1. Instalar paquetes

```bash
sudo apt update
sudo apt install -y mariadb-server python3-flask python3-pymysql
sudo systemctl enable --now mariadb
```

### 2. Crear la base de datos sin contraseña fija

La autenticación se hace mediante el usuario local de Ubuntu y el socket de MariaDB:

```bash
U=$(whoami)
sudo mariadb -e "CREATE DATABASE inventario; CREATE USER '$U'@'localhost' IDENTIFIED VIA unix_socket; GRANT ALL ON inventario.* TO '$U'@'localhost'; USE inventario; CREATE TABLE equipos(id INT AUTO_INCREMENT PRIMARY KEY,nombre VARCHAR(80)); INSERT INTO equipos(nombre) VALUES('Equipo inicial');"
```

Comprueba:

```bash
mariadb inventario -e "SELECT * FROM equipos;"
```

### 3. Escribir la aplicación

Ejecuta:

```bash
nano app.py
```

Teclea exactamente este contenido. Respeta los cuatro espacios de las líneas interiores:

```python
from flask import Flask,request,redirect
import pymysql,getpass,os

app=Flask(__name__)

def con():
    return pymysql.connect(unix_socket='/run/mysqld/mysqld.sock',user=getpass.getuser(),database='inventario',autocommit=True)

def lista():
    with con().cursor() as c:
        c.execute('SELECT * FROM equipos')
        return c.fetchall()

@app.route('/')
def inicio():
    filas=''.join(f'<li>{x[1]}</li>' for x in lista())
    return f"<body style='font-family:sans-serif;background:#eef;padding:8%'><h1>Inventario informatico</h1><p>Infraestructura Informatica para CPD</p><p>Estudiante: {os.getenv('NOMBRE')}</p><p>IP: {os.getenv('IP')} - MV3</p><form action='/alta' method='post'><input name='n' required><button>Anadir equipo</button></form><h2>Equipos</h2><ul>{filas}</ul><p><a href='/api/equipos'>API</a></p></body>"

@app.post('/alta')
def alta():
    with con().cursor() as c:
        c.execute('INSERT INTO equipos(nombre) VALUES(%s)',(request.form['n'],))
    return redirect('/')

@app.get('/api/equipos')
def api():
    with con().cursor(pymysql.cursors.DictCursor) as c:
        c.execute('SELECT * FROM equipos')
        return {'equipos':c.fetchall()}

app.run(host='0.0.0.0',port=5000)
```

Guarda con `Ctrl+O`, pulsa `Enter` y sal con `Ctrl+X`.

### 4. Arrancar Flask

```bash
export NOMBRE="NOMBRE APELLIDOS"
export IP=$(hostname -I | cut -d' ' -f1)
nohup python3 app.py >/tmp/flask.log 2>&1 &
curl http://localhost:5000
curl http://localhost:5000/api/equipos
```

Si falla:

```bash
cat /tmp/flask.log
```

## Comprobación final

Desde una máquina que pueda acceder a las tres IP:

```bash
curl -I http://IP_MV1
curl -I http://IP_MV2
curl http://IP_MV3:5000
curl http://IP_MV3:5000/api/equipos
```

Resultados esperados:

- MV1 y MV2: `HTTP/1.1 200 OK`.
- MV3: página del inventario con “Equipo inicial”.
- API: JSON con el equipo inicial.
- El formulario permite añadir otro equipo y demuestra escritura en MariaDB.

## Capturas imprescindibles

1. Página de MV1.
2. Página de MV2.
3. Página Flask con al menos dos equipos.
4. Resultado JSON de `/api/equipos`.
5. `systemctl status apache2` en MV1/MV2.
6. `systemctl status mariadb` y `SELECT * FROM equipos` en MV3.
7. Una comprobación `curl` entre máquinas.

