#!/usr/bin/env bash
set -Eeuo pipefail

usage() { echo "Uso: sudo $0 --student 'Nombre Apellidos' --ip 'IP_ASIGNADA'"; }
STUDENT_NAME="${STUDENT_NAME:-}"
SERVER_IP="${SERVER_IP:-}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --student) STUDENT_NAME="${2:-}"; shift 2 ;;
    --ip) SERVER_IP="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Parámetro desconocido: $1" >&2; usage; exit 2 ;;
  esac
done
[[ $EUID -eq 0 ]] || { echo "Ejecuta el script con sudo." >&2; exit 1; }
[[ -n "$STUDENT_NAME" && -n "$SERVER_IP" ]] || { usage; exit 2; }

html_escape() { local s=$1; s=${s//&/&amp;}; s=${s//</&lt;}; s=${s//>/&gt;}; s=${s//\"/&quot;}; printf '%s' "$s"; }
SRC_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y apache2
install -d -m 0755 /var/www/html
escaped_student=$(html_escape "$STUDENT_NAME")
escaped_ip=$(html_escape "$SERVER_IP")
sed -e "s|{{STUDENT_NAME}}|$escaped_student|g" -e "s|{{SERVER_IP}}|$escaped_ip|g" "$SRC_DIR/index.html" > /var/www/html/index.html
install -m 0644 "$SRC_DIR/style.css" /var/www/html/style.css
systemctl enable --now apache2
apache2ctl configtest
curl --fail --silent http://127.0.0.1/ >/dev/null
echo "MV1 instalada. Comprueba: http://$SERVER_IP/"

