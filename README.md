# TP2-Backend

# Proyecto Backend: Fixture y ProDe Mundial 2026

### Introducción al Desarrollo de Software - Curso Lanzillota

Este repositorio contiene la API REST desarrollada para la gestión del fixture del Mundial 2026 y el sistema de pronósticos deportivos (ProDe) solicitado en el **Enunciado Sorpresa**.

## Estructura del Proyecto

- `main.py`: Archivo principal que arranca la aplicación.
- `controllers/`: Contiene las URLs o rutas a las que uno puede acceder (como `/partidos` y `/usuarios`).
- `services/`: Contiene el funcionamiento interno y las reglas del sistema.
- `repositories/`: Se encarga de guardar, buscar o borrar datos en la base de datos usando SQL.
- `database.py`: Archivo encargado de la conexión con MySQL.
- `schema.sql`: Código necesario para crear la base de datos vacía y sus tablas.

## Tecnologías Utilizadas

- **Lenguaje:** Python 3.10+
- **Framework:** Flask
- **Base de Datos:** MySQL
- **Conector BD:** mysql-connector-python
-

## Endpoints Principales

- **POST /partidos:** Crea partidos.
- **GET /partidos:** Lista partidos.
- **PUT /partidos/{id}/resultado:** Actualiza resultados.
- **DELETE /elimina partido:** Elimina un partido.

## Dependencias

Es necesario instalar el microframework Flask y el conector para MySQL:

```bash
pip install Flask mysql-connector-python
```
