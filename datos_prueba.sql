-- Limpiamos por si la ejecutamos múltiples veces (el orden de delete es importante por las relaciones)
DELETE FROM predicciones;
DELETE FROM partidos;
DELETE FROM usuarios;

-- 1. Insertamos Usuarios
INSERT INTO usuarios (id, nombre, email) VALUES 
(1, 'Leo Messi', 'leo@ejemplo.com'),
(2, 'Elias', 'elias@ejemplo.com'),
(3, 'Merentiel', 'merentiel@ejemplo.com');

-- 2. Insertamos Partidos (Algunos terminados y otros no)
-- Partido 1: Argentina 2 - 1 Brasil
-- Partido 2: Francia vs Inglaterra (No jugado, en NULL)
-- Partido 3: España 1 - 1 Italia
INSERT INTO partidos (id, equipo_local, equipo_visitante, fecha, fase, goles_local, goles_visitante) VALUES 
(1, 'Argentina', 'Brasil', '2026-06-15 15:00:00', 'grupos', 2, 1),
(2, 'Francia', 'Inglaterra', '2026-06-16 18:00:00', 'grupos', NULL, NULL),
(3, 'España', 'Italia', '2026-06-18 15:00:00', 'grupos', 1, 1);

-- 3. Insertamos Predicciones para calcular puntos
-- Respecto al Partido 1 (ARG 2 - 1 BRA):
-- Leo predice ARG 2 - 1 BRA (Acierto Exacto -> 3 pts)
-- Elias predice ARG 1 - 0 BRA (Acierto de Ganador -> 1 pt)
-- Merentiel predice ARG 0 - 2 BRA (Incorrecto -> 0 pts)
INSERT INTO predicciones (id_usuario, id_partido, local, visitante) VALUES 
(1, 1, 2, 1),
(2, 1, 1, 0),
(3, 1, 0, 2);

-- Respecto al Partido 3 (ESP 1 - 1 ITA):
-- Leo predice ESP 2 - 2 ITA (Acierto Empate, pero no exacto -> 1 pt)
-- Elias predice ESP 1 - 1 ITA (Acierto Exacto -> 3 pts)
-- Merentiel predice ESP 0 - 0 ITA (Acierto Empate, pero no exacto -> 1 pt)
INSERT INTO predicciones (id_usuario, id_partido, local, visitante) VALUES 
(1, 3, 2, 2),
(2, 3, 1, 1),
(3, 3, 0, 0);

-- RESULTADOS ESPERADOS EN EL RANKING:
-- Leo: 3 + 1 = 4 puntos
-- Elias: 1 + 3 = 4 puntos
-- Merentiel: 0 + 1 = 1 punto
