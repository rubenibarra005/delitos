LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/INM_estatal_nov25.csv'
INTO TABLE delitos
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(anio, clave_ent, entidad, bien_juridico_afectado, tipo_delito, subtipo_delito, modalidad, mes, @fecha, incidencia_delictiva, entidad_federativa)
SET fecha = STR_TO_DATE(@fecha, '%Y-%m-%d');


CREATE DATABASE IF NOT EXISTS proyectosbd;
USE proyectosbd;
DROP TABLE IF EXISTS delitos;

CREATE TABLE delitos (
  anio SMALLINT NOT NULL,
  clave_ent TINYINT NOT NULL,
  entidad VARCHAR(60) NOT NULL,
  bien_juridico_afectado VARCHAR(120) NOT NULL,
  tipo_delito VARCHAR(160) NOT NULL,
  subtipo_delito VARCHAR(160) NOT NULL,
  modalidad VARCHAR(160) NOT NULL,
  mes TINYINT NOT NULL,
  fecha DATE NOT NULL,
  incidencia_delictiva INT NOT NULL,
  entidad_federativa VARCHAR(60) NOT NULL,

  INDEX idx_fecha (fecha),
  INDEX idx_entidad (entidad),
  INDEX idx_tipo (tipo_delito),
  INDEX idx_anio_mes (anio, mes)
);

ALTER TABLE delitos
MODIFY mes VARCHAR(15);