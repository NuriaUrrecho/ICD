#!/usr/bin/env bash
set -Eeuo pipefail

[[ $EUID -eq 0 ]] || { echo "Ejecuta: sudo bash instalar.sh NUMERO" >&2; exit 1; }
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROLE="${1:-}"
if [[ ! "$ROLE" =~ ^[123]$ ]]; then
  read -r -p "¿Qué máquina es (1, 2 o 3)? " ROLE
fi
[[ "$ROLE" =~ ^[123]$ ]] || { echo "Elige 1, 2 o 3." >&2; exit 2; }

STUDENT_NAME=""
if [[ -f "$ROOT_DIR/datos.conf" ]]; then
  STUDENT_NAME=$(sed -n 's/^NOMBRE_ESTUDIANTE=//p' "$ROOT_DIR/datos.conf" | head -n 1)
fi
if [[ -z "$STUDENT_NAME" || "$STUDENT_NAME" == "CAMBIAR_ANTES_DEL_LABORATORIO" ]]; then
  read -r -p "Nombre y apellidos: " STUDENT_NAME
fi
[[ -n "$STUDENT_NAME" ]] || { echo "Falta el nombre del estudiante." >&2; exit 2; }

DETECTED_IP=$(ip -4 route get 1.1.1.1 2>/dev/null | awk '{for(i=1;i<=NF;i++) if($i=="src"){print $(i+1); exit}}' || true)
if [[ -z "$DETECTED_IP" ]]; then
  DETECTED_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || true)
fi
read -r -p "IP que mostrará la web [$DETECTED_IP]: " SERVER_IP
SERVER_IP="${SERVER_IP:-$DETECTED_IP}"
[[ -n "$SERVER_IP" ]] || { echo "No se pudo detectar la IP. Escríbela manualmente." >&2; exit 2; }

echo "Instalando MV$ROLE para $STUDENT_NAME en $SERVER_IP..."
case "$ROLE" in
  1) bash "$ROOT_DIR/mv1/instalar_mv1.sh" --student "$STUDENT_NAME" --ip "$SERVER_IP" ;;
  2) bash "$ROOT_DIR/mv2/instalar_mv2.sh" --student "$STUDENT_NAME" --ip "$SERVER_IP" ;;
  3) bash "$ROOT_DIR/mv3/instalar_mv3.sh" --student "$STUDENT_NAME" --ip "$SERVER_IP" ;;
esac

echo
echo "LISTO: MV$ROLE instalada. Guarda una captura de esta pantalla."

