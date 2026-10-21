# Checklist de ejecución y evidencias

## Antes de Proxmox

- [ ] Aplicación y segmentos de red consensuados con el profesor.
- [x] Docker Desktop instalado.
- [x] `.env` creado sin subirlo a Git.
- [x] Cuatro servicios Docker en estado `healthy`.
- [x] Prueba CRUD finalizada sin errores.
- [x] Prueba directa de MariaDB correcta.

## Proxmox

- [ ] Tres contenedores LXC visibles y arrancados.
- [ ] Hardware de MV1 capturado.
- [ ] Hardware de MV2 capturado.
- [ ] Hardware de MV3 capturado.
- [ ] Red, MAC, bridge y VLAN documentados sin mostrar secretos.
- [ ] `ip -br address` e `ip route` de cada contenedor.
- [ ] Apache activo y habilitado en MV1.
- [ ] Apache activo y habilitado en MV2.
- [ ] MariaDB y `tablon-cpd` activos y habilitados en MV3.
- [ ] Comunicación cruzada demostrada.
- [ ] Servicios comprobados después de reiniciar.

## Capturas de la aplicación

- [ ] Portada completa de MV1.
- [ ] Portada completa de MV2.
- [ ] Página principal del tablón con avisos iniciales.
- [ ] Formulario antes de publicar un aviso.
- [ ] Nuevo aviso visible tras recargar.
- [ ] Filtro por categoría.
- [ ] Filtro por prioridad.
- [ ] Eliminación confirmada.
- [ ] `/health` mostrando conexión con MariaDB.
- [ ] `/api/avisos` mostrando JSON.
- [ ] Consulta SQL mostrando los avisos persistidos.

## Memoria

- [ ] Portada y autor correctos.
- [ ] Índice de contenidos.
- [ ] Índice de figuras.
- [ ] Objetivo y antecedentes.
- [ ] Arquitectura y red real utilizadas.
- [ ] Desarrollo de las tres máquinas.
- [ ] Validación con resultados reales.
- [ ] Conclusiones.
- [ ] Glosario y referencias.
- [ ] Anexo de prompts, comandos, scripts y configuraciones.
- [ ] Ninguna contraseña ni captura inventada.
