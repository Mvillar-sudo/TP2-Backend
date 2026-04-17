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

INSERT INTO partidos (Equipo_local, Equipo_visitante, Fecha, Fase)
VALUES
('Argentina', 'Croacia', '2026-03-11', 'Grupos'),
('Brasil', 'Paises Bajos', '2026-03-11', 'Grupos'),
('Senegal', 'España', '2026-03-13', 'Grupos'),
('Costa Rica', 'Uruguay', '2026-03-13', 'Grupos');

