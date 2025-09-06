CREATE DATABASE project;
USE project;

CREATE TABLE ProductionData (
    id INT AUTO_INCREMENT PRIMARY KEY,
    machine_id INT,
    production_rate FLOAT,
    defect_rate FLOAT,
    timestamp DATETIME
);

CREATE TABLE Predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    machine_id INT,
    alert_label VARCHAR(50),
    timestamp DATETIME
);
