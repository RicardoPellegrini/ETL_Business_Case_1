Creation of database and tables - Ricardo Pellegrini

DROP DATABASE IF EXISTS db_shape;
CREATE DATABASE db_shape
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;



CREATE TABLE tb_equipments
(
  	equipment_id				INT NOT NULL,
  	code					VARCHAR(16) NOT NULL,
  	group_name				VARCHAR(16) NOT NULL,
  	CONSTRAINT pk_tb_equipment PRIMARY KEY (equipment_id)
);



CREATE TABLE tb_equipment_sensors
(
	equipment_id				INT NOT NULL,
	sensor_id				INT NOT NULL,
	CONSTRAINT pk_equipment_sensors PRIMARY KEY(sensor_id),
	CONSTRAINT fk_tb_equipments_tb_equipment_sensors
		FOREIGN KEY(equipment_id) 
		REFERENCES tb_equipments(equipment_id)
);


CREATE TABLE tb_equipment_failure_sensors
(
	failure_id					SERIAL,
	datetime_utc				TIMESTAMP NOT NULL,
	sensor_id					INT NOT NULL,
	temperature					NUMERIC NOT NULL,
	vibration					NUMERIC NOT NULL,
	CONSTRAINT pk_equipment_failure_sensors PRIMARY KEY(failure_id),
	CONSTRAINT fk_tb_equipment_sensors_tb_equipment_failure_sensors
		FOREIGN KEY(sensor_id) 
		REFERENCES tb_equipment_sensors(sensor_id)
);