DROP TABLE partidos;
DROP TABLE usuarios;
DROP TABLE predicciones;


CREATE DATABASE IF NOT EXISTS mundial_fixture;
USE mundial_fixture;

CREATE TABLE partidos (
    ID               INT AUTO_INCREMENT PRIMARY KEY,
    Equipo_local     VARCHAR(100) NOT NULL,
    Equipo_visitante VARCHAR(100) NOT NULL,
    Goles_local      INT NULL,
    Goles_visitante  INT NULL,
    Fecha            DATE NOT NULL,
    Fase             VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE
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
