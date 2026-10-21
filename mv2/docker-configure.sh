#!/bin/sh
set -eu
escape_html() { printf '%s' "$1" | sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g' -e 's/"/\&quot;/g'; }
escape_sed() { printf '%s' "$1" | sed -e 's/[\\&|]/\\&/g'; }
student=$(escape_sed "$(escape_html "${STUDENT_NAME:-Nombre configurable}")")
server_ip=$(escape_sed "$(escape_html "${SERVER_IP:-IP configurable}")")
sed -e "s|{{STUDENT_NAME}}|$student|g" -e "s|{{SERVER_IP}}|$server_ip|g" /opt/site/index.html > /usr/local/apache2/htdocs/index.html
exec httpd-foreground

