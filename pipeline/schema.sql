-- This file contains all SQL commands to create the tables and relationships for the Plants database.

DROP TABLE IF EXISTS sensor_reading;
DROP TABLE IF EXISTS botanist_assignment;
DROP TABLE IF EXISTS plant;
DROP TABLE IF EXISTS origin;
DROP TABLE IF EXISTS botanist;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS alert;
DROP TABLE IF EXISTS alert_type;

-- Longest official country name in English is 56 characters.
CREATE TABLE country (
    country_id TINYINT IDENTITY(1,1),
    country_name VARCHAR(60) NOT NULL,
    PRIMARY KEY (country_id)
);

CREATE TABLE origin (
    origin_id SMALLINT IDENTITY(1,1),
    latitude DECIMAL(6, 4) NOT NULL,
    longitude DECIMAL(7, 4) NOT NULL,
    city_name VARCHAR(50) NOT NULL,
    country_id TINYINT NOT NULL,
    PRIMARY KEY (origin_id),
    FOREIGN KEY (country_id)
        REFERENCES country(country_id),
);

CREATE TABLE plant (
    plant_id SMALLINT IDENTITY(1,1),
    plant_name VARCHAR(40) NOT NULL,
    origin_id SMALLINT NOT NULL,
    scientific_name VARCHAR(40),
    image_link VARCHAR(255),
    PRIMARY KEY (plant_id),
    FOREIGN KEY (origin_id)
        REFERENCES origin(origin_id)
);

CREATE TABLE sensor_reading (
    sensor_reading_id BIGINT IDENTITY(1,1),
    taken_at DATETIME2(0) NOT NULL,
    temperature DECIMAL(5, 2) NOT NULL,
    last_watered DATETIME2(0) NOT NULL,
    soil_moisture DECIMAL(5, 2) NOT NULL,
    plant_id SMALLINT NOT NULL,
    PRIMARY KEY (sensor_reading_id),
    FOREIGN KEY (plant_id) 
        REFERENCES plant(plant_id),
    CHECK (
        soil_moisture >= 0
        AND soil_moisture <= 100
    ) 
);

CREATE TABLE botanist (
    botanist_id SMALLINT IDENTITY(1,1),
    botanist_name VARCHAR(40) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    phone VARCHAR(21) NOT NULL UNIQUE,
    PRIMARY KEY (botanist_id)
);

CREATE TABLE botanist_assignment (
    botanist_assignment_id SMALLINT IDENTITY(1,1),
    botanist_id SMALLINT NOT NULL,
    plant_id SMALLINT NOT NULL,
    PRIMARY KEY (botanist_assignment_id),
    FOREIGN KEY (plant_id)
        REFERENCES plant(plant_id),
    FOREIGN KEY (botanist_id)
        REFERENCES botanist(botanist_id)
);

CREATE TABLE alert_type (
    alert_type_id SMALLINT IDENTITY(1,1),
    alert_type_name VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY (alert_type_id)
);

CREATE TABLE alert (
    alert_id BIGINT IDENTITY(1,1),
    plant_id SMALLINT NOT NULL,
    alert_type_id SMALLINT NOT NULL,
    alert_value DECIMAL(5, 2) NOT NULL,
    sent_at DATETIME2(0) NOT NULL,
    PRIMARY KEY (alert_id),
    FOREIGN KEY (plant_id)
        REFERENCES plant(plant_id),
    FOREIGN KEY (alert_type_id)
        REFERENCES alert_type(alert_type_id)
);

INSERT INTO alert_type
VALUES 
('temperature'),
('soil moisture');