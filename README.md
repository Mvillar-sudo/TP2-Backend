# TP2-Backend
# Proyecto Backend: Fixture y ProDe Mundial 2026 
### Introducción al Desarrollo de Software  - Curso Lanzillota 

Este repositorio contiene la API REST desarrollada para la gestión del fixture del Mundial 2026 y el sistema de pronósticos deportivos (ProDe) solicitado en el **Enunciado Sorpresa**.

##  Estructura del Proyecto

* `app.py`: Punto de entrada del servidor Flask y definición de rutas.
* `models.py`: Definición de los modelos de datos (SQLAlchemy) y conexión a la base de datos.
* `logic.py`: Lógica de negocio para el cálculo de puntajes y reglas del ProDe.
* `swagger.yaml`: Contrato de la API que define los estándares de entrada y salida.

##  Tecnologías Utilizadas
* **Lenguaje:** Python 3.10+
* **Framework:** Flask
* **Base de Datos:** MySQL
* **ORM:** Flask-SQLAlchemy
* 
## Endpoints Principales
* **POST /partidos:** Crea partidos.
*  **GET /partidos:** Lista partidos.
* **PUT /partidos/{id}/resultado:** Actualiza resultados.

##  Dependencias
Es necesario instalar el microframework Flask y el conector para MySQL:
```bash
pip install Flask mysql-connector-python
