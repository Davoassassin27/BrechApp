# BrechApp

<img src="assets/images/logo.png" alt="BrechApp Logo" width="150" height="auto">

**BrechApp** es una plataforma para la integración y análisis de la brecha cambiaria del dólar en Argentina.

## Descripción
Este proyecto busca centralizar, normalizar y analizar datos de múltiples fuentes sobre las cotizaciones del dólar (Oficial, Blue, MEP, CCL, etc.) para monitorear la evolución de la brecha cambiaria.

## Estructura del Proyecto
- `data/`: Almacenamiento de datos crudos y procesados.
- `src/`: Código fuente de la aplicación.
    - `ingestion/`: Scripts para la recolección de datos.
    - `processing/`: Limpieza y transformación de datos.
    - `analysis/`: Cálculo de indicadores y visualización.
- `notebooks/`: Análisis exploratorio.
    - `01_exploration_dolarapi.ipynb`: Test de conexión API.
    - `02_analysis_brecha_polars.ipynb`: Análisis básico con Polars.
    - `03_final_analysis.ipynb`: **Análisis Final** (Brechas, Medias Móviles, Volatilidad).
- `tests/`: Tests unitarios.

## Requisitos
- Python 3.8+
- Ver `requirements.txt` para las dependencias.

## Instrucciones de Uso

1.  **Configurar Entorno**:
    ```bash
    # Crear y activar entorno
    python -m venv .env
    .\.env\Scripts\Activate.ps1
    
    # Instalar dependencias
    pip install -r requirements.txt
    ```

2.  **Ingesta de Datos**:
    ```bash
    # Descargar historia completa
    python src/ingestion/ingest_history.py
    ```

3.  **Procesamiento**:
    ```bash
    # Procesar JSONs a Parquet
    python src/processing/process_history.py
    ```

4.  **Análisis**:
    - Abrir `notebooks/03_final_analysis.ipynb` en Jupyter o VS Code.
    - Seleccionar el kernel `Python (BrechApp)`.
    - Ejecutar todas las celdas.

> Todavia no hay testing porque la app esta solo en etapa de Ingestión y Procesamiento.