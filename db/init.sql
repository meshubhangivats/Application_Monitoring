CREATE DATABASE IF NOT EXISTS logs;

USE logs;

CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    endpoint VARCHAR(255),
    response_time FLOAT,
    status_code INT,
    error_message TEXT
);
