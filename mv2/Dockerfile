FROM nginx:1.27-alpine
COPY index.html /opt/site/index.html
COPY style.css /usr/share/nginx/html/style.css
COPY docker-configure.sh /docker-entrypoint.d/40-configure.sh
RUN chmod 755 /docker-entrypoint.d/40-configure.sh

