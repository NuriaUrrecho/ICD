FROM httpd:2.4-alpine
COPY index.html /opt/site/index.html
COPY style.css /usr/local/apache2/htdocs/style.css
COPY docker-configure.sh /opt/configure.sh
RUN chmod 755 /opt/configure.sh
CMD ["/opt/configure.sh"]

