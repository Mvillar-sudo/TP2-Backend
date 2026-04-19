# Estructura del Proyecto

Esta estructura cumple con la "Separación de Capas" que pide el PDF y mantiene el proyecto ordenado:

```text
/proyecto-backend-mundial
│
├── app.py                      <-- El servidor principal. Aquí se registran todas las rutas.
├── database.py                 <-- La conexión única a MySQL que usan todos los módulos.
├── schema.sql                  <-- El diseño oficial de las tablas para que los profes puedan probarlo.
├── swagger.yaml                <-- El contrato intacto.
├── .gitignore                  <-- Archivos que no se suben (__pycache__, venv, etc).
├── README.md                   <-- Instrucciones de cómo correr el proyecto.
│
├── controllers/                <-- CAPA 1 (Recepcionistas): Reciben el pedido y validan los parámetros HTTP.
│   ├── ranking_controller.py
│   ├── partidos_controller.py  <-- Harán los endpoints GET /partidos, POST /partidos, etc.
│   ├── usuarios_controller.py
│   └── predicciones_controller.py
│
├── services/                   <-- CAPA 2 (Directores): Lógica de negocio y reglas del ProDe.
│   ├── ranking_service.py
│   ├── partidos_service.py
│   ├── usuarios_service.py
│   └── predicciones_service.py
│
└── repositories/               <-- CAPA 3 (Bibliotecarios): Puro SQL, los únicos que usan 'database.py'.
    ├── ranking_repository.py
    ├── partidos_repository.py
    ├── usuarios_repository.py
    └── predicciones_repository.py
```
