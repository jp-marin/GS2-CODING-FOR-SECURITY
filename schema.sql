CREATE DATABASE IF NOT EXISTS bealive
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE bealive;

CREATE TABLE IF NOT EXISTS ocorrencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(40) NOT NULL,
    descricao VARCHAR(500) NULL,
    local VARCHAR(120) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    data_ocorrencia DATE NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
