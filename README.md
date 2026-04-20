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

### Partidos y Predicciones

- **GET /partidos:** Lista partidos
- **POST /partidos:** Crea partidos
- **GET /partidos/{id}:** Obtiene el detalle de un partido específico
- **PUT /partidos/{id}/resultado:** Actualiza el resultado de un partido
- **DELETE /partidos/{id}:** Elimina un partido de la base de datos
- **POST /partidos/{id}/prediccion:** Registra la predicción de un usuario para un partido

### Usuarios

- **GET /usuarios:** Lista todos los usuarios registrados.
- **POST /usuarios:** Crea un nuevo usuario.
- **GET /usuarios/{id}:** Obtiene el detalle de un usuario específico.
- **PUT /usuarios/{id}:** Actualiza los datos de un usuario.
- **DELETE /usuarios/{id}:** Elimina un usuario del sistema.

### Ranking (ProDe)

- **GET /ranking:** Obtiene la tabla de posiciones calculando los puntos de los usuarios según los resultados.

## Dependencias

Es necesario instalar el microframework Flask y el conector para MySQL:

```bash
pip install Flask mysql-connector-python
```
