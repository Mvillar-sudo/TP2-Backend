CREATE DATABASE IF NOT EXISTS mundial_fixture;
USE mundial_fixture;

CREATE TABLE partidos (
    ID               INT AUTO_INCREMENT PRIMARY KEY,
    Equipo_local     VARCHAR(100) NOT NULL,
    Equipo_visitante VARCHAR(100) NOT NULL,
    Goles_local      INT NULL,
    Goles_visitante  INT NULL,
    Estadio          VARCHAR(100),
    Ciudad           VARCHAR(100),
    Fecha            DATETIME NOT NULL,
    Fase             VARCHAR(50) NOT NULL
);

INSERT INTO partidos (Equipo_local, Equipo_visitante, Estadio, Ciudad, Fecha, Fase)
VALUES
('Argentina', 'Croacia', 'Estadio Azteca', 'Ciudad de Mexico', '2026-03-11 15:00:00', 'Grupos'),
('Brasil', 'Paises Bajos', 'Estadio Azteca', 'Ciudad de Mexico', '2026-03-11 18:00:00', 'Grupos'),
('Senegal', 'España', 'Estadio Azteca', 'Ciudad de Mexico', '2026-03-13 15:00:00', 'Grupos'),
('Costa Rica', 'Uruguay', 'Estadio Azteca', 'Ciudad de Mexico', '2026-03-13 18:00:00', 'Grupos');

