# Práctica 4 - Máquinas virtuales

**Asignatura:** Infraestructura Informática para Centros de Procesamiento de Datos (14541)  
**Titulación:** Grado en Informática Industrial y Robótica  
**Estudiante:** Nuria Urrecho Torres  
**Profesor:** Dr. Lenin Guillermo Lemus Zúñiga  
**Curso:** 2025-2026

> Borrador técnico. Los marcadores `[CAPTURA PENDIENTE]` y `[DATO PENDIENTE]` deben sustituirse exclusivamente con evidencias reales.

## Índice de contenidos

Generar automáticamente al exportar el documento final.

## Índice de figuras

Generar automáticamente después de insertar y numerar las capturas reales.

## 1. Objetivo

El objetivo es crear y configurar mediante Proxmox VE una infraestructura básica formada por tres contenedores LXC interconectados. Los dos primeros ejecutan servidores web Apache independientes. El tercero aloja una aplicación web desarrollada con Flask que se comunica con MariaDB.

La aplicación desarrollada específicamente para esta práctica se denomina **Tablón de Avisos del CPD**. Permite publicar, listar, filtrar y eliminar comunicaciones operativas almacenadas de forma persistente en una base de datos relacional.

## 2. Antecedentes

### 2.1. Virtualización en Proxmox VE

Proxmox VE es una plataforma de virtualización basada en Debian que integra máquinas virtuales KVM/QEMU y contenedores LXC. Proporciona gestión web, almacenamiento, redes virtuales, copias de seguridad y control del ciclo de vida de las máquinas.

### 2.2. Diferencias entre KVM y LXC

| Característica | KVM/QEMU | LXC |
|---|---|---|
| Virtualización | hardware completo | sistema operativo |
| Núcleo | propio | compartido con el anfitrión |
| Sistemas invitados | Linux, Windows y otros | Linux |
| Consumo | mayor | reducido |
| Aislamiento | muy alto | alto |
| Uso en esta práctica | posible | elegido por eficiencia |

### 2.3. Interconexión

Proxmox conecta interfaces virtuales mediante bridges Linux. Un bridge actúa como un conmutador virtual. La configuración concreta de IP, máscara, gateway, DNS, bridge, VLAN y MAC depende del entorno y debe verificarse antes de modificar la red.

### 2.4. Metodología

1. Analizar los requisitos.
2. Definir roles, recursos y red.
3. Crear los tres contenedores.
4. Verificar conectividad antes de instalar.
5. Desplegar Apache y Flask/MariaDB mediante scripts reproducibles.
6. Validar servicios, datos, comunicación y arranque automático.
7. Recoger capturas reales y documentar los resultados.

## 3. Entorno de trabajo y diseño

### 3.1. Preparación local

Antes del despliegue se preparó un laboratorio Docker en Windows 11. Este entorno contiene Apache MV1, Apache MV2, Flask MV3 y MariaDB, y permite ejecutar pruebas funcionales sin afirmar que se ha validado Proxmox.

**Estado:** Docker Desktop quedó instalado y el laboratorio se ejecutó con sus cuatro servicios en estado saludable. Las dos páginas Apache respondieron con HTTP 200, Flask se conectó a MariaDB 11.4.13, se verificó el CRUD completo y los datos persistieron tras detener y volver a levantar el entorno.

### 3.2. Recursos propuestos

| Máquina | Rol | vCPU | RAM | Swap | Disco |
|---|---|---:|---:|---:|---:|
| MV1 | Apache 1 | 1 | 512 MiB | 256 MiB | 8 GiB |
| MV2 | Apache 2 | 1 | 512 MiB | 256 MiB | 8 GiB |
| MV3 | Flask + MariaDB | 2 | 1 GiB | 512 MiB | 10 GiB |

### 3.3. Red definitiva

| Parámetro | MV1 | MV2 | MV3 |
|---|---|---|---|
| VMID | [DATO PENDIENTE] | [DATO PENDIENTE] | [DATO PENDIENTE] |
| Hostname | web1-cpd | web2-cpd | tablon-cpd |
| IP/prefijo | [DATO PENDIENTE] | [DATO PENDIENTE] | [DATO PENDIENTE] |
| MAC | [DATO PENDIENTE] | [DATO PENDIENTE] | [DATO PENDIENTE] |
| Bridge/VLAN | [DATO PENDIENTE] | [DATO PENDIENTE] | [DATO PENDIENTE] |

La aplicación y el segmento se comunicarán al profesor antes del despliegue, como exige el enunciado.

**Figura 1.** Arquitectura general. `[CAPTURA/DIAGRAMA PENDIENTE]`

## 4. Desarrollo

### 4.1. MV1 - Primer servidor Apache

El instalador `mv1/instalar_mv1.sh` instala Apache, sustituye de forma segura el nombre y la IP configurables, publica HTML/CSS, valida la configuración y habilita el arranque automático.

La portada muestra el nombre de la asignatura, la estudiante, la dirección IP y la identificación MV1.

**Figura 2.** Resumen del contenedor MV1. `[CAPTURA PENDIENTE]`  
**Figura 3.** Página Apache de MV1. `[CAPTURA PENDIENTE]`

### 4.2. MV2 - Segundo servidor Apache

MV2 usa el mismo procedimiento reproducible, pero presenta una composición visual diferenciada. De este modo se demuestra que son dos servicios independientes y no una única página duplicada.

**Figura 4.** Resumen del contenedor MV2. `[CAPTURA PENDIENTE]`  
**Figura 5.** Página Apache de MV2. `[CAPTURA PENDIENTE]`

### 4.3. MV3 - Tablón de Avisos del CPD

La aplicación utiliza Flask y Jinja2 para la interfaz, SQLAlchemy/PyMySQL para consultas parametrizadas y MariaDB para la persistencia. Gunicorn actúa como servidor WSGI y `systemd` controla su arranque.

La tabla `avisos` contiene:

- `id`, clave primaria autoincremental;
- `titulo` y `descripcion`;
- `categoria`: Mantenimiento, Incidencia, Seguridad o General;
- `prioridad`: Baja, Media, Alta o Crítica;
- `fecha_publicacion`.

El proyecto incorpora ocho registros de ejemplo. Las credenciales se obtienen de variables de entorno y el repositorio no contiene contraseñas reales.

Rutas principales:

| Método | Ruta | Función |
|---|---|---|
| GET | `/` | listado y filtros |
| POST | `/avisos` | publicación desde formulario |
| POST | `/avisos/<id>/eliminar` | eliminación web |
| GET | `/health` | consulta real a MariaDB |
| GET/POST | `/api/avisos` | listado y creación JSON |
| GET/PUT/PATCH/DELETE | `/api/avisos/<id>` | CRUD por API |

**Figura 6.** Aplicación con avisos. `[CAPTURA PENDIENTE]`  
**Figura 7.** Publicación de un aviso. `[CAPTURA PENDIENTE]`  
**Figura 8.** Filtros. `[CAPTURA PENDIENTE]`  
**Figura 9.** `/health`. `[CAPTURA PENDIENTE]`  
**Figura 10.** `/api/avisos`. `[CAPTURA PENDIENTE]`

## 5. Validación

Las pruebas se detallan en `VALIDACION.md`. Deben registrarse los resultados reales de:

- estado de los tres contenedores;
- Apache activo en MV1 y MV2;
- Flask y MariaDB activos en MV3;
- publicación, persistencia, filtros y eliminación;
- JSON de la API;
- conexión SQL demostrada por `/health`;
- comunicación entre contenedores;
- arranque automático tras reinicio.

| Prueba | Resultado | Evidencia |
|---|---|---|
| Apache MV1 local | Superada | HTTP 200 y revisión visual |
| Apache MV2 local | Superada | HTTP 200 y revisión visual |
| Flask local | Superada | página principal con ocho avisos |
| Flask-MariaDB local | Superada | `/health` y consulta SQL real |
| CRUD, filtros y persistencia local | Superada | script automatizado y reinicio de Compose |
| Comunicación en Proxmox | Pendiente | [CAPTURA REAL] |
| Reinicio de contenedores Proxmox | Pendiente | [CAPTURA REAL] |

## 6. Conclusiones

El proyecto deja preparado y validado localmente el código, los instaladores y las pruebas para construir una infraestructura corporativa mínima. El laboratorio Docker confirmó el funcionamiento conjunto de Apache, Flask y MariaDB, incluido el CRUD y la persistencia. El despliegue Proxmox deberá completarse con resultados observados en ese entorno real; esta separación evita presentar como ejecutadas pruebas que todavía están pendientes.

## 7. Glosario

| Término | Definición |
|---|---|
| API REST | interfaz HTTP para operar con recursos |
| Bridge | conmutador virtual que conecta interfaces |
| CPD | Centro de Procesamiento de Datos |
| Flask | framework web ligero para Python |
| Gunicorn | servidor WSGI para aplicaciones Python |
| KVM | virtualización completa del núcleo Linux |
| LXC | contenedores de sistema Linux |
| MariaDB | sistema gestor de bases de datos relacional |
| Proxmox VE | plataforma de virtualización |
| SGBD | Sistema Gestor de Bases de Datos |

## 8. Referencias

1. Proxmox Server Solutions GmbH. *Proxmox VE Administration Guide*. https://pve.proxmox.com/pve-docs/
2. Apache Software Foundation. *Apache HTTP Server Documentation*. https://httpd.apache.org/docs/
3. Pallets. *Flask Documentation*. https://flask.palletsprojects.com/
4. MariaDB Foundation. *MariaDB Server Documentation*. https://mariadb.com/docs/
5. Gunicorn. *Gunicorn Documentation*. https://docs.gunicorn.org/
6. Linux Containers. *LXC Documentation*. https://linuxcontainers.org/lxc/

Indicar la fecha real de consulta al cerrar la memoria.

## Anexo A. Uso de inteligencia artificial

Prompt principal: solicitud de análisis del enunciado, diseño de una infraestructura de tres contenedores y desarrollo original del Tablón de Avisos del CPD con Flask y MariaDB.

Acciones realizadas: análisis de requisitos, diseño de arquitectura, generación de código, scripts, entorno Docker, pruebas y borrador documental. No se han inventado capturas ni resultados de Proxmox.

## Anexo B. Comandos, scripts y configuración

Adjuntar o referenciar los archivos del repositorio y las configuraciones reales exportadas de Proxmox. Eliminar contraseñas y secretos antes de incluirlos.

## Observación sobre el enunciado

El apartado de entregables propone el título «Evaluación de prestaciones de medios de almacenamiento masivos», que no coincide con el contenido de la Práctica 4 sobre máquinas virtuales. Debe confirmarse el título definitivo con el profesor en lugar de adoptar silenciosamente el texto aparentemente heredado.
