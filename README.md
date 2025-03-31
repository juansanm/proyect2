# Forest Cover Type Prediction - MLOps Pipeline

Este proyecto implementa un pipeline de Machine Learning utilizando tecnologías como Apache Airflow, MLflow, FastAPI y Streamlit. Se emplea un modelo de Random Forest para predecir el tipo de cobertura forestal basado en datos de sensores ambientales.

## Proyecto corriendo en Azure Microsoft
Se crea el proyecto

![Se crea el proyecto](https://github.com/juansanm/proyect2/blob/main/p/1.png)

Verificacion de estados

![-](https://github.com/juansanm/proyect2/blob/main/p/2.png)


Verificamos que los puertos estén activos, en este caso de ejemplo el 8503 de Streamlit


![-](https://github.com/juansanm/proyect2/blob/main/p/3.png)


![-](https://github.com/juansanm/proyect2/blob/main/p/4.png)

Funcionamiento ejemplos:


![-](https://github.com/juansanm/proyect2/blob/main/p/5.png)


![-](https://github.com/juansanm/proyect2/blob/main/p/6.png)


Costos referentes a este proceso por 4 dias de VM para un servicio de Azure

![-](https://github.com/juansanm/proyect2/blob/main/p/7.png)


## Arquitectura del Proyecto

El proyecto se compone de los siguientes servicios:

- **Airflow**: Orquestación del pipeline de entrenamiento del modelo.
- **MLflow**: Seguimiento y gestión de experimentos y modelos.
- **FastAPI**: API de inferencia para realizar predicciones en tiempo real.
- **Streamlit**: Interfaz gráfica para la visualización de resultados.
- **MySQL**: Base de datos para almacenar metadatos de MLflow.
- **MinIO**: Almacenamiento de artefactos del modelo.

## Estructura del Proyecto

```
├── airflow/
│   ├── dags/
│   │   ├── forest_cover_dag.py
│   ├── Dockerfile
│   ├── requirements.txt
├── inference/
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
├── mlflow/
│   ├── Dockerfile
│   ├── requirements.txt
├── streamlit/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
├── docker-compose.yml
```

## Configuración y Despliegue

### Requisitos Previos

- Docker y Docker Compose instalados en tu máquina.
- Puerto 8080 disponible para Airflow.
- Puerto 5000 disponible para MLflow.
- Puerto 8000 disponible para la API de inferencia.
- Puerto 8503 disponible para Streamlit.

### Pasos para el Despliegue

1. Clonar este repositorio.
2. Construir y levantar los servicios con Docker Compose:
   ```bash
   docker-compose up --build -d
   ```
3. Acceder a los servicios:
   - **Airflow**: [http://localhost:8080](http://localhost:8080)
   - **MLflow UI**: [http://localhost:5000](http://localhost:5000)
   - **API de Inferencia**: [http://localhost:8000](http://localhost:8000)
   - **Streamlit GUI**: [http://localhost:8503](http://localhost:8503)

## Detalles de Implementación

### Airflow DAG (Entrenamiento del Modelo)

El DAG de Airflow `forest_cover_dag.py` ejecuta las siguientes tareas:

1. **fetch\_data**: Obtiene los datos desde una API externa.
2. **prepare\_data**: Prepara los datos para el entrenamiento.
3. **train\_model**: Entrena un modelo de Random Forest y registra métricas en MLflow.

### API de Inferencia (FastAPI)

La API de inferencia permite hacer predicciones enviando datos en formato JSON. Ejemplo de petición:

```bash
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"feature1": 10, "feature2": 20, "feature3": 30}'
```

### Streamlit (Interfaz Visual)

La aplicación en Streamlit permite visualizar predicciones de manera interactiva.

## Cierre

Este proyecto proporciona una infraestructura completa para el entrenamiento, almacenamiento, despliegue e inferencia de modelos de Machine Learning en un entorno de producción utilizando MLOps

## Realizado y sufrido por:
Juan Felipe Gonzalez Sanmiguel


