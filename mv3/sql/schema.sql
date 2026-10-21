CREATE TABLE IF NOT EXISTS avisos (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  titulo VARCHAR(120) NOT NULL,
  descripcion TEXT NOT NULL,
  categoria VARCHAR(30) NOT NULL,
  prioridad VARCHAR(20) NOT NULL,
  fecha_publicacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY ix_avisos_titulo (titulo),
  KEY ix_avisos_categoria (categoria),
  KEY ix_avisos_prioridad (prioridad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO avisos (titulo, descripcion, categoria, prioridad)
SELECT * FROM (
  SELECT 'Mantenimiento de climatización', 'Revisión preventiva de las unidades de climatización de la sala técnica.', 'Mantenimiento', 'Media' UNION ALL
  SELECT 'Actualización del cortafuegos', 'Ventana de actualización prevista para el viernes a las 22:00.', 'Seguridad', 'Alta' UNION ALL
  SELECT 'Incidencia en almacenamiento', 'Latencia elevada detectada en el sistema de copias de seguridad.', 'Incidencia', 'Crítica' UNION ALL
  SELECT 'Prueba mensual del SAI', 'La prueba de autonomía se realizará sin interrupción de servicio.', 'Mantenimiento', 'Baja' UNION ALL
  SELECT 'Cambio de política de contraseñas', 'La nueva política será efectiva a partir del próximo lunes.', 'Seguridad', 'Media' UNION ALL
  SELECT 'Intervención de red', 'Puede producirse una pérdida breve de conectividad durante la madrugada.', 'Incidencia', 'Alta' UNION ALL
  SELECT 'Acceso de personal externo', 'Visita técnica autorizada para revisar el sistema antiincendios.', 'General', 'Baja' UNION ALL
  SELECT 'Reunión de coordinación', 'Revisión semanal de incidencias y tareas pendientes del CPD.', 'General', 'Media'
) AS datos
WHERE NOT EXISTS (SELECT 1 FROM avisos);

