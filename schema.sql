CREATE DATABASE IF NOT EXISTS mundial_db;
USE mundial_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS partidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipo_local VARCHAR(255) NOT NULL,
    equipo_visitante VARCHAR(255) NOT NULL,
    goles_local INT NULL,
    goles_visitante INT NULL,
    fecha DATETIME NOT NULL,
    fase VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS predicciones (
    id_usuario INT NOT NULL,
    id_partido INT NOT NULL,
    local INT NOT NULL,
    visitante INT NOT NULL,
    PRIMARY KEY (id_usuario, id_partido),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_partido) REFERENCES partidos(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
