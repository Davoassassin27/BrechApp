# BrechApp 🚀

<img src="assets/images/logo.png" alt="BrechApp Logo" width="150" height="auto">

**BrechApp** es una plataforma completa para el análisis de criptomonedas con predicción de precios, análisis de volatilidad y detección de brechas.

## 📋 Descripción

Este proyecto integra modelos de series temporales (ARIMA, Prophet, GARCH) con una API REST y una interfaz web interactiva para:
- Predicción de precios de criptomonedas
- Análisis de volatilidad
- Visualización de datos históricos
- Detección de brechas y anomalías

## 🏗️ Estructura del Proyecto

```
BrechApp/
├── src/
│   ├── ingestion/      # Recolección de datos
│   ├── processing/     # Limpieza y transformación
│   ├── analysis/       # Análisis exploratorio
│   ├── models/         # Modelos de ML (ARIMA, Prophet, GARCH)
│   ├── api/            # Backend FastAPI
│   └── frontend/       # Frontend Streamlit
├── data/
│   ├── raw/            # Datos crudos
│   └── processed/      # Datos procesados
├── notebooks/          # Análisis exploratorio
├── tests/              # Tests unitarios
└── docs/               # Documentación
```

## 🔧 Requisitos

- Python 3.8+
- pip
- Git

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
# Clonar el repositorio
git clone https://github.com/Davoassassin27/BrechApp.git
cd BrechApp

# Ver todas las ramas disponibles
git branch -a
```

### 2. Elegir la Rama de Trabajo

```bash
# Para trabajar con todo (recomendado)
git checkout develop

# O elegir una feature específica:
git checkout feature/models      # Solo modelos
git checkout feature/api         # Solo API
git checkout feature/frontend    # Solo frontend
```

### 3. Configurar Entorno Virtual

**Windows (PowerShell):**
```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno
.\.venv\Scripts\Activate.ps1

# Si hay error de permisos, ejecutar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux/Mac:**
```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar entorno
source .venv/bin/activate
```

### 4. Instalar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

## 📊 Uso

### Ingesta de Datos

```bash
# Descargar datos históricos
python src/ingestion/ingest_history.py
```

### Procesamiento

```bash
# Procesar datos a formato Parquet
python src/processing/process_history.py
```

### Ejecutar Frontend (Streamlit)

```bash
# Iniciar aplicación web
streamlit run src/frontend/app.py

# La app se abrirá en: http://localhost:8501
```

### Ejecutar API (FastAPI)

```bash
# Iniciar servidor API
uvicorn src.api.main:app --reload

# Documentación disponible en:
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

### Análisis en Notebooks

```bash
# Iniciar Jupyter
jupyter notebook

# Abrir notebooks/03_final_analysis.ipynb
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=src tests/

# Test específico
pytest tests/test_models.py
```

## 🌿 Workflow Git

```bash
# Actualizar desde develop
git checkout develop
git pull origin develop

# Crear nueva feature
git checkout -b feature/mi-feature

# Hacer cambios y commit
git add .
git commit -m "feat: descripción del cambio"

# Push a GitHub
git push -u origin feature/mi-feature
```

## 📦 Ramas Disponibles

- `main` - Producción estable
- `develop` - Desarrollo principal
- `feature/models` - Modelos de ML
- `feature/api` - Backend API
- `feature/frontend` - Interfaz web

## 🛠️ Tecnologías

- **Data Processing**: Pandas, Polars, NumPy
- **ML Models**: Statsmodels, Prophet, ARCH
- **API**: FastAPI, Uvicorn, Pydantic
- **Frontend**: Streamlit, Plotly
- **Testing**: Pytest

## 📝 Notas

- Los datos se almacenan en `data/` (ignorado por git)
- Configurar variables de entorno en `.env` si es necesario
- La API corre en puerto 8000 por defecto
- Streamlit corre en puerto 8501 por defecto

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add: AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto es de código abierto.

## 👥 Autor

Desarrollado por Davoassassin27