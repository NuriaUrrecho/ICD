#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  echo "Uso: sudo $0 --student 'Nombre Apellidos' --ip 'IP_ASIGNADA' [--db-name inventario] [--db-user inventario_app]"
}
STUDENT_NAME="${STUDENT_NAME:-}"
SERVER_IP="${SERVER_IP:-}"
DB_NAME="${DB_NAME:-inventario}"
DB_USER="${DB_USER:-inventario_app}"
DB_PASSWORD="${DB_PASSWORD:-}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --student) STUDENT_NAME="${2:-}"; shift 2 ;;
    --ip) SERVER_IP="${2:-}"; shift 2 ;;
    --db-name) DB_NAME="${2:-}"; shift 2 ;;
    --db-user) DB_USER="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Parámetro desconocido: $1" >&2; usage; exit 2 ;;
  esac
done
[[ $EUID -eq 0 ]] || { echo "Ejecuta el script con sudo." >&2; exit 1; }
[[ -n "$STUDENT_NAME" && -n "$SERVER_IP" ]] || { usage; exit 2; }
[[ "$DB_NAME" =~ ^[A-Za-z0-9_]+$ && "$DB_USER" =~ ^[A-Za-z0-9_]+$ ]] || { echo "Nombre de base de datos/usuario no válido." >&2; exit 2; }
if [[ -z "$DB_PASSWORD" ]]; then
  read -r -s -p "Contraseña nueva para el usuario MariaDB '$DB_USER': " DB_PASSWORD
  echo
fi
[[ -n "$DB_PASSWORD" && "$DB_PASSWORD" != *$'\n'* ]] || { echo "La contraseña no puede estar vacía ni contener saltos de línea." >&2; exit 2; }

SRC_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR=/opt/inventario-mv3
APP_USER=inventario
ENV_FILE=/etc/inventario-mv3.env

apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-venv python3-pip mariadb-server curl
systemctl enable --now mariadb
id "$APP_USER" >/dev/null 2>&1 || useradd --system --home "$APP_DIR" --shell /usr/sbin/nologin "$APP_USER"
install -d -o "$APP_USER" -g "$APP_USER" -m 0755 "$APP_DIR"
cp -a "$SRC_DIR/." "$APP_DIR/"
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install --upgrade pip
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"

sql_password=${DB_PASSWORD//\\/\\\\}
sql_password=${sql_password//\'/\'\'}
sql_file=$(mktemp)
trap 'rm -f "$sql_file"' EXIT
chmod 600 "$sql_file"
cat > "$sql_file" <<SQL
CREATE DATABASE IF NOT EXISTS \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$sql_password';
ALTER USER '$DB_USER'@'localhost' IDENTIFIED BY '$sql_password';
GRANT ALL PRIVILEGES ON \`$DB_NAME\`.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
USE \`$DB_NAME\`;
SOURCE $APP_DIR/sql/schema.sql;
SQL
mariadb < "$sql_file"

escape_env() { local s=$1; s=${s//\\/\\\\}; s=${s//\"/\\\"}; printf '%s' "$s"; }
SECRET_KEY=$("$APP_DIR/venv/bin/python" -c 'import secrets; print(secrets.token_hex(32))')
install -o root -g "$APP_USER" -m 0640 /dev/null "$ENV_FILE"
{
  printf 'DB_HOST="127.0.0.1"\nDB_PORT="3306"\n'
  printf 'DB_NAME="%s"\nDB_USER="%s"\n' "$(escape_env "$DB_NAME")" "$(escape_env "$DB_USER")"
  printf 'DB_PASSWORD="%s"\n' "$(escape_env "$DB_PASSWORD")"
  printf 'SECRET_KEY="%s"\n' "$SECRET_KEY"
  printf 'STUDENT_NAME="%s"\nSERVER_IP="%s"\n' "$(escape_env "$STUDENT_NAME")" "$(escape_env "$SERVER_IP")"
} > "$ENV_FILE"

cat > /etc/systemd/system/inventario-mv3.service <<'UNIT'
[Unit]
Description=Inventario Flask de la práctica 4
After=network-online.target mariadb.service
Wants=network-online.target
Requires=mariadb.service

[Service]
Type=simple
User=inventario
Group=inventario
WorkingDirectory=/opt/inventario-mv3
EnvironmentFile=/etc/inventario-mv3.env
ExecStart=/opt/inventario-mv3/venv/bin/gunicorn --workers 2 --bind 0.0.0.0:5000 --access-logfile - run:app
Restart=on-failure
RestartSec=5
PrivateTmp=true
ProtectSystem=full
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
systemctl enable --now inventario-mv3
for _ in {1..20}; do curl --fail --silent http://127.0.0.1:5000/api/health >/dev/null && break; sleep 1; done
curl --fail --silent http://127.0.0.1:5000/api/health
echo
echo "MV3 instalada. Comprueba: http://$SERVER_IP:5000/"
