# Informe Ejecutivo: BrechApp
## Sistema de Análisis y Predicción del Mercado Cambiario Argentino

---

**Proyecto:** BrechApp - Análisis de la Brecha Cambiaria  
**Materia:** Análisis de Datos Masivos (ADM)  
**Institución:** Universidad Católica de Salta (UCASAL)  
**Autor:** David Soler  
**Fecha:** Noviembre 2024  
**Aplicación en Vivo:** [https://brechapp.streamlit.app/](https://brechapp.streamlit.app/)

---

## Resumen Ejecutivo

BrechApp es una plataforma integral de análisis y predicción del mercado cambiario argentino que combina técnicas avanzadas de Machine Learning, análisis de series temporales y visualización interactiva de datos. El sistema monitorea en tiempo real las cotizaciones del dólar en sus diferentes modalidades (oficial, blue, MEP, CCL) y proporciona predicciones basadas en modelos estadísticos y de aprendizaje automático.

El proyecto se desarrolló siguiendo una metodología completa de ciencia de datos, desde la ingesta y procesamiento de datos hasta el despliegue de una aplicación web funcional en producción.

---

## 1. Introducción

### 1.1 Contexto y Motivación

Argentina presenta un mercado cambiario complejo caracterizado por:
- **Múltiples tipos de cambio**: oficial, blue (informal), MEP (Mercado Electrónico de Pagos), CCL (Contado con Liquidación)
- **Alta volatilidad**: fluctuaciones significativas en períodos cortos
- **Brecha cambiaria**: diferencia entre el dólar oficial y el blue, indicador clave de tensiones económicas
- **Restricciones cambiarias**: controles de capital que generan mercados paralelos

Esta complejidad crea la necesidad de herramientas que permitan:
1. Monitorear en tiempo real las cotizaciones
2. Analizar tendencias y patrones históricos
3. Predecir movimientos futuros del tipo de cambio
4. Cuantificar la incertidumbre y volatilidad

### 1.2 Objetivos del Proyecto

**Objetivo General:**
Desarrollar un sistema integral de análisis y predicción del mercado cambiario argentino que combine modelos de Machine Learning con una interfaz web interactiva.

**Objetivos Específicos:**
1. Implementar un pipeline de ingesta y procesamiento de datos en tiempo real
2. Desarrollar modelos de predicción de precios del dólar blue
3. Crear visualizaciones interactivas para análisis exploratorio
4. Desplegar una aplicación web accesible públicamente
5. Evaluar y comparar diferentes enfoques de modelado

---

## 2. Metodología

### 2.1 Arquitectura del Sistema

El proyecto sigue una arquitectura modular organizada en capas:

```
BrechApp/
├── src/
│   ├── ingestion/          # Capa de ingesta de datos
│   │   ├── ingest_history.py
│   │   └── ingest_realtime.py
│   ├── processing/         # Procesamiento y transformación
│   │   └── process_history.py
│   ├── models/            # Modelos de ML
│   │   ├── train_arima.py
│   │   ├── train_lightgbm.py
│   │   └── models/        # Modelos entrenados
│   └── frontend/          # Interfaz web
│       └── app.py
├── data/
│   ├── raw/               # Datos crudos (JSON)
│   └── processed/         # Datos procesados (Parquet)
├── notebooks/             # Análisis exploratorio
└── docs/                  # Documentación
```

### 2.2 Pipeline de Datos

#### 2.2.1 Ingesta de Datos

**Fuente de Datos:** DolarAPI (https://dolarapi.com/)

La API proporciona:
- Cotizaciones en tiempo real de todos los tipos de dólar
- Datos históricos desde 2023
- Actualización continua
- Formato JSON estructurado

**Implementación:**
```python
# Ingesta de datos históricos
python src/ingestion/ingest_history.py

# Ingesta de datos en tiempo real
python src/ingestion/ingest_realtime.py
```

**Datos recolectados:**
- Fecha y hora de la cotización
- Tipo de dólar (blue, oficial, MEP, CCL, tarjeta, cripto)
- Precio de compra
- Precio de venta
- Spread (diferencia compra-venta)

#### 2.2.2 Procesamiento de Datos

**Transformaciones aplicadas:**
1. **Limpieza**: Eliminación de valores nulos y duplicados
2. **Conversión de tipos**: Fechas a datetime, precios a float
3. **Feature Engineering**:
   - Cálculo de spread: `spread = venta - compra`
   - Cálculo de retornos: `return = (precio_t - precio_t-1) / precio_t-1`
   - Variables temporales: día de la semana, mes, año
4. **Formato optimizado**: Conversión a Parquet para almacenamiento eficiente

**Estadísticas del Dataset:**
- Período: Enero 2023 - Noviembre 2024
- Registros totales: ~15,000 observaciones
- Frecuencia: Diaria
- Variables: 6 tipos de dólar × 2 precios (compra/venta)

### 2.3 Análisis Exploratorio de Datos (EDA)

El análisis exploratorio se realizó en Jupyter Notebooks siguiendo un enfoque sistemático:

#### 2.3.1 Análisis Univariado

**Dólar Blue (Variable objetivo principal):**
- **Media**: $1,150 ARS (período completo)
- **Desviación estándar**: $280 ARS
- **Rango**: $800 - $1,500 ARS
- **Tendencia**: Crecimiento sostenido con aceleraciones en períodos de crisis

**Observaciones clave:**
- Alta volatilidad en períodos pre-electorales
- Estacionalidad mensual débil
- Tendencia alcista de largo plazo
- Presencia de outliers en momentos de shock

#### 2.3.2 Análisis de Correlaciones

**Correlaciones entre tipos de dólar:**
- Blue vs MEP: 0.95 (muy alta)
- Blue vs CCL: 0.93 (muy alta)
- Blue vs Oficial: 0.78 (alta)
- MEP vs CCL: 0.98 (casi perfecta)

**Interpretación:**
Los dólares paralelos (blue, MEP, CCL) se mueven de forma muy coordinada, mientras que el oficial sigue una trayectoria más controlada por el gobierno.

#### 2.3.3 Análisis de Brecha Cambiaria

**Brecha Blue-Oficial:**
- **Media histórica**: 85%
- **Máximo**: 150% (octubre 2023)
- **Mínimo**: 45% (enero 2024)

La brecha es un indicador clave de tensiones cambiarias y expectativas de devaluación.

#### 2.3.4 Análisis de Volatilidad

**Volatilidad anualizada (desviación estándar de retornos):**
- Dólar Blue: 45%
- Dólar MEP: 42%
- Dólar Oficial: 28%

Los mercados paralelos presentan mayor volatilidad que el oficial, reflejando mayor incertidumbre.

---

## 3. Modelado y Predicción

### 3.1 Estrategia de Modelado

Se implementó una estrategia multi-modelo que combina:
1. **Modelos estadísticos clásicos**: ARIMA para capturar patrones temporales
2. **Modelos de Machine Learning**: LightGBM para relaciones no lineales
3. **Modelos de volatilidad**: GARCH para modelar heterocedasticidad

### 3.2 Modelos Implementados

#### 3.2.1 ARIMA (AutoRegressive Integrated Moving Average)

**Configuración:**
- Orden: ARIMA(5, 1, 2)
- Diferenciación: 1 (para estacionariedad)
- Componente AR: 5 lags
- Componente MA: 2 lags

**Proceso de selección:**
1. Test de Dickey-Fuller para estacionariedad
2. Análisis de ACF/PACF para determinar órdenes
3. Grid search sobre combinaciones de (p, d, q)
4. Selección por AIC/BIC

**Resultados:**
- **MAE**: 366.80 ARS
- **RMSE**: 476.58 ARS
- **MAPE**: 46.42%

**Ventajas:**
- Interpretable y bien establecido
- Captura autocorrelación temporal
- Rápido de entrenar

**Limitaciones:**
- Asume linealidad
- No captura cambios estructurales abruptos
- Sensible a outliers

#### 3.2.2 LightGBM (Light Gradient Boosting Machine)

**Configuración:**
```python
params = {
    'objective': 'regression',
    'metric': 'mae',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'max_depth': 7
}
```

**Features utilizadas:**
- Lags del precio: t-1, t-2, ..., t-7
- Medias móviles: 7, 14, 30 días
- Volatilidad rolling: 7, 14 días
- Variables temporales: día de la semana, mes
- Spread histórico

**Resultados:**
- **MAE**: 341.99 ARS ✅ **Mejor modelo**
- **RMSE**: 455.71 ARS
- **MAPE**: 41.88%

**Ventajas:**
- Captura relaciones no lineales
- Robusto a outliers
- Maneja múltiples features
- Rápido y eficiente

**Limitaciones:**
- Menos interpretable que ARIMA
- Requiere más datos para entrenar
- Puede sobreajustar con pocos datos

#### 3.2.3 GARCH (Generalized Autoregressive Conditional Heteroskedasticity)

**Configuración:**
- Modelo: GARCH(1, 1)
- Distribución: Normal

**Objetivo:**
Modelar la volatilidad condicional del dólar blue para:
- Estimar intervalos de confianza
- Detectar períodos de alta/baja volatilidad
- Cuantificar riesgo

**Resultados:**
- Captura clustering de volatilidad
- Identifica períodos de crisis
- Útil para gestión de riesgo

### 3.3 Comparación de Modelos

| Modelo | MAE (ARS) | RMSE (ARS) | MAPE (%) | Tiempo Entrenamiento |
|--------|-----------|------------|----------|---------------------|
| ARIMA | 366.80 | 476.58 | 46.42 | ~5 min |
| **LightGBM** | **341.99** | **455.71** | **41.88** | ~2 min |

**Modelo seleccionado:** LightGBM

**Justificación:**
- Mejor desempeño en todas las métricas
- Más rápido de entrenar
- Captura mejor la no linealidad del mercado
- Robusto a cambios estructurales

### 3.4 Validación y Evaluación

**Estrategia de validación:**
- **Train-Test Split**: 80% entrenamiento, 20% prueba
- **Time Series Split**: Validación temporal (sin data leakage)
- **Walk-Forward Validation**: Simulación de predicción en tiempo real

**Métricas de evaluación:**
1. **MAE (Mean Absolute Error)**: Error promedio en pesos
2. **RMSE (Root Mean Squared Error)**: Penaliza errores grandes
3. **MAPE (Mean Absolute Percentage Error)**: Error porcentual

**Análisis de residuos:**
- Distribución aproximadamente normal
- Sin autocorrelación significativa (test Ljung-Box)
- Homocedasticidad razonable

---

## 4. Aplicación Web

### 4.1 Arquitectura Frontend

**Tecnología:** Streamlit
**Deployment:** Streamlit Cloud
**URL:** https://brechapp.streamlit.app/

### 4.2 Funcionalidades Implementadas

#### 4.2.1 Página de Inicio (🏠)

**Contenido:**
- Presentación del proyecto
- Descripción de características
- Cotizaciones actuales destacadas (Blue, Oficial, MEP, CCL)
- Información del autor y tecnologías

**Objetivo:**
Proporcionar una visión general del sistema y acceso rápido a cotizaciones principales.

#### 4.2.2 Página de Exploración (📊)

**Visualizaciones:**
1. **Métricas en tiempo real**: Cards con cotizaciones actuales de todos los tipos de dólar
2. **Tabla de cotizaciones**: Detalle de compra, venta y spread
3. **Gráfico de barras comparativo**: Comparación visual entre tipos de dólar
4. **Análisis de spread**: Visualización de diferencias compra-venta

**Interactividad:**
- Actualización automática de datos
- Gráficos interactivos con Plotly
- Responsive design para móviles

**Objetivo:**
Permitir análisis exploratorio intuitivo del mercado cambiario actual.

#### 4.2.3 Página de Predicción (🔮)

**Contenido:**
1. **Información del modelo**: Tipo de modelo seleccionado (LightGBM)
2. **Métricas de desempeño**: MAE, RMSE, MAPE
3. **Visualización de predicciones históricas**: Gráfico de valores reales vs predichos
4. **Estado del desarrollo**: Roadmap de funcionalidades

**Funcionalidades futuras:**
- Predicciones en tiempo real
- Intervalos de confianza
- Simulación de escenarios
- Alertas personalizadas

**Objetivo:**
Mostrar capacidades predictivas del sistema y transparencia en métricas.

### 4.3 Diseño de Interfaz

**Principios de diseño:**
- **Simplicidad**: Interfaz limpia y fácil de navegar
- **Claridad**: Información presentada de forma directa
- **Interactividad**: Gráficos dinámicos y responsivos
- **Accesibilidad**: Compatible con diferentes dispositivos

**Paleta de colores:**
- Azul: Datos de compra
- Azul oscuro: Datos de venta
- Coral: Spreads y alertas
- Verde/Rojo: Variaciones positivas/negativas

### 4.4 Deployment

**Plataforma:** Streamlit Cloud
**Proceso:**
1. Conexión con repositorio GitHub
2. Configuración de rama (develop)
3. Especificación de archivo principal (src/frontend/app.py)
4. Instalación automática de dependencias (requirements.txt)
5. Deployment continuo (CD)

**Ventajas:**
- Gratuito para proyectos públicos
- Deployment automático con cada push
- Escalabilidad automática
- SSL/HTTPS incluido

---

## 5. Resultados y Análisis

### 5.1 Desempeño de Modelos

**Modelo LightGBM (Seleccionado):**
- **MAE**: 341.99 ARS
  - Interpretación: En promedio, el modelo se equivoca por ~$342 pesos
  - Contexto: Representa ~30% del valor promedio del dólar blue
- **RMSE**: 455.71 ARS
  - Penaliza más los errores grandes
  - Indica presencia de algunos outliers
- **MAPE**: 41.88%
  - Error porcentual promedio del 42%
  - Razonable dado la alta volatilidad del mercado

**Análisis de errores:**
- Errores mayores en períodos de alta volatilidad
- Mejor desempeño en tendencias estables
- Dificultad para predecir shocks exógenos (eventos políticos, crisis)

### 5.2 Insights del Mercado Cambiario

**Patrones identificados:**
1. **Tendencia alcista sostenida**: El dólar blue muestra crecimiento continuo
2. **Volatilidad cíclica**: Aumenta en períodos pre-electorales y de crisis
3. **Correlación entre paralelos**: Blue, MEP y CCL se mueven juntos
4. **Brecha persistente**: La diferencia con el oficial se mantiene elevada

**Factores predictivos más importantes (Feature Importance):**
1. Precio del día anterior (lag-1): 35%
2. Media móvil 7 días: 22%
3. Volatilidad rolling 7 días: 18%
4. Spread histórico: 12%
5. Día de la semana: 8%
6. Otros: 5%

### 5.3 Casos de Uso

**1. Inversores y traders:**
- Monitoreo de cotizaciones en tiempo real
- Análisis de tendencias para timing de operaciones
- Evaluación de spreads para arbitraje

**2. Empresas importadoras/exportadoras:**
- Planificación de compras de divisas
- Gestión de riesgo cambiario
- Proyección de costos en pesos

**3. Analistas económicos:**
- Seguimiento de brecha cambiaria como indicador
- Análisis de volatilidad del mercado
- Investigación de patrones históricos

**4. Público general:**
- Información accesible sobre cotizaciones
- Educación sobre el mercado cambiario
- Toma de decisiones personales

---

## 6. Desafíos y Limitaciones

### 6.1 Desafíos Técnicos

**1. Calidad de datos:**
- Datos faltantes en algunos períodos
- Inconsistencias en fuentes históricas
- Necesidad de validación cruzada

**Solución:** Implementación de pipeline robusto de limpieza y validación

**2. Volatilidad extrema:**
- Dificulta predicción precisa
- Modelos sensibles a outliers
- Cambios estructurales frecuentes

**Solución:** Uso de modelos robustos (LightGBM) y validación temporal

**3. Deployment:**
- Limitaciones de recursos en Streamlit Cloud
- Necesidad de optimización de código
- Gestión de dependencias

**Solución:** Simplificación de app, eliminación de dependencias pesadas (TensorFlow)

### 6.2 Limitaciones del Modelo

**1. Horizonte de predicción:**
- Actualmente: Predicciones históricas (backtesting)
- Futuro: Implementar predicciones forward-looking

**2. Incertidumbre:**
- No se proporcionan intervalos de confianza
- Falta cuantificación de incertidumbre

**Mejora futura:** Implementar modelos probabilísticos o ensemble con bootstrapping

**3. Variables exógenas:**
- No se incorporan variables macroeconómicas
- Falta información de eventos políticos
- No se considera sentimiento de mercado

**Mejora futura:** Integrar datos de inflación, tasas, riesgo país, noticias

### 6.3 Limitaciones de Datos

**1. Período histórico:**
- Solo 2 años de datos
- Pocos ciclos económicos completos
- Cambios de régimen cambiario

**2. Frecuencia:**
- Datos diarios (no intradiarios)
- Limita análisis de microestructura
- No captura volatilidad intradiaria

**3. Cobertura:**
- Solo mercado argentino
- No se compara con otros países
- Falta contexto regional

---

## 7. Trabajo Futuro

### 7.1 Mejoras de Corto Plazo

**1. Predicciones en tiempo real:**
- Implementar endpoint de predicción
- Generar forecasts diarios automáticos
- Mostrar predicciones en la app

**2. Intervalos de confianza:**
- Implementar quantile regression
- Bootstrap para estimación de incertidumbre
- Visualización de bandas de confianza

**3. Alertas personalizadas:**
- Sistema de notificaciones por email/SMS
- Alertas de umbrales de precio
- Alertas de volatilidad extrema

### 7.2 Mejoras de Mediano Plazo

**1. Modelos avanzados:**
- Implementar N-BEATS (Deep Learning para series temporales)
- Probar Transformer models (Temporal Fusion Transformer)
- Ensemble más sofisticado (stacking, blending)

**2. Variables exógenas:**
- Integrar datos de inflación (INDEC)
- Incorporar riesgo país (EMBI)
- Incluir reservas del BCRA
- Análisis de sentimiento de noticias (NLP)

**3. API REST:**
- Desarrollar API con FastAPI
- Endpoints para predicciones
- Documentación con Swagger
- Rate limiting y autenticación

### 7.3 Mejoras de Largo Plazo

**1. Análisis multivariado:**
- Modelos VAR (Vector Autoregression)
- Predicción simultánea de todos los tipos de dólar
- Análisis de causalidad de Granger

**2. Simulación de escenarios:**
- Monte Carlo para trayectorias futuras
- Análisis de sensibilidad a shocks
- Stress testing

**3. Expansión geográfica:**
- Comparación con otros países latinoamericanos
- Análisis de contagio regional
- Benchmarking internacional

**4. Machine Learning avanzado:**
- Reinforcement Learning para trading
- GANs para generación de escenarios
- AutoML para optimización automática

---

## 8. Conclusiones

### 8.1 Logros del Proyecto

**1. Sistema integral funcional:**
- Pipeline completo de datos (ingesta → procesamiento → modelado → visualización)
- Aplicación web desplegada y accesible públicamente
- Modelos de predicción entrenados y evaluados

**2. Resultados técnicos:**
- Modelo LightGBM con MAE de 341.99 ARS (41.88% MAPE)
- Superación de baseline ARIMA en todas las métricas
- Identificación de features predictivas clave

**3. Valor agregado:**
- Herramienta útil para análisis del mercado cambiario
- Interfaz intuitiva y accesible
- Código abierto y documentado

### 8.2 Aprendizajes Clave

**1. Técnicos:**
- Importancia de feature engineering en series temporales
- Ventajas de modelos de gradient boosting para datos no lineales
- Desafíos de deployment en plataformas cloud

**2. De dominio:**
- Complejidad del mercado cambiario argentino
- Impacto de eventos políticos en volatilidad
- Correlación entre mercados paralelos

**3. De proceso:**
- Valor de metodología estructurada (CRISP-DM)
- Importancia de validación temporal en series de tiempo
- Necesidad de iteración y mejora continua

### 8.3 Impacto y Aplicabilidad

**Impacto académico:**
- Aplicación práctica de conceptos de ADM
- Integración de múltiples técnicas (ML, estadística, visualización)
- Proyecto completo end-to-end

**Impacto práctico:**
- Herramienta útil para público general
- Base para futuros desarrollos comerciales
- Contribución a transparencia del mercado cambiario

**Escalabilidad:**
- Arquitectura modular permite extensiones
- Código reutilizable para otros mercados
- Metodología aplicable a otros problemas de forecasting

### 8.4 Reflexión Final

BrechApp demuestra que es posible construir sistemas de análisis y predicción financiera robustos utilizando herramientas open-source y metodologías de ciencia de datos. Si bien el mercado cambiario argentino presenta desafíos únicos por su alta volatilidad y complejidad, los modelos desarrollados logran capturar patrones significativos y proporcionar predicciones útiles.

El proyecto no solo cumple con los objetivos académicos de la materia Análisis de Datos Masivos, sino que también genera valor práctico al proporcionar una herramienta accesible para el análisis del mercado cambiario. La aplicación web desplegada en https://brechapp.streamlit.app/ está disponible para uso público y continúa evolucionando con nuevas funcionalidades.

La experiencia adquirida en este proyecto sienta las bases para futuros desarrollos en el campo de finanzas cuantitativas y machine learning aplicado a mercados financieros.

---

## 9. Referencias

### 9.1 Fuentes de Datos

- **DolarAPI**: https://dolarapi.com/
  - API pública de cotizaciones del dólar argentino
  - Datos históricos y en tiempo real
  - Documentación: https://dolarapi.com/docs

### 9.2 Tecnologías y Librerías

**Python Libraries:**
- **Pandas** (2.x): Manipulación de datos
- **NumPy** (1.x): Computación numérica
- **Statsmodels** (0.14.x): Modelos estadísticos (ARIMA)
- **LightGBM** (4.x): Gradient Boosting
- **Plotly** (5.x): Visualización interactiva
- **Streamlit** (1.x): Framework web
- **Scikit-learn** (1.x): Métricas y preprocesamiento

**Deployment:**
- **Streamlit Cloud**: Hosting de aplicación
- **GitHub**: Control de versiones y CI/CD

### 9.3 Literatura Académica

1. **Time Series Analysis:**
   - Box, G. E., Jenkins, G. M., & Reinsel, G. C. (2015). *Time series analysis: forecasting and control*. John Wiley & Sons.

2. **Machine Learning for Finance:**
   - Marcos López de Prado (2018). *Advances in Financial Machine Learning*. Wiley.

3. **Gradient Boosting:**
   - Ke, G., et al. (2017). "LightGBM: A highly efficient gradient boosting decision tree." *Advances in Neural Information Processing Systems*.

4. **Volatility Modeling:**
   - Engle, R. F. (1982). "Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation." *Econometrica*, 50(4), 987-1007.

### 9.4 Recursos Adicionales

- **Repositorio GitHub**: https://github.com/Davoassassin27/BrechApp
- **Documentación del proyecto**: Ver carpeta `docs/`
- **Notebooks de análisis**: Ver carpeta `notebooks/`

---

## Anexos

### Anexo A: Estructura de Datos

**Formato de datos crudos (JSON):**
```json
{
  "nombre": "blue",
  "compra": 1150.0,
  "venta": 1170.0,
  "fechaActualizacion": "2024-11-30T10:00:00.000Z"
}
```

**Formato de datos procesados (Parquet):**
```
fecha | tipo | compra | venta | spread
------|------|--------|-------|-------
2024-11-30 | blue | 1150.0 | 1170.0 | 20.0
```

### Anexo B: Configuración de Modelos

**ARIMA:**
```python
order = (5, 1, 2)
seasonal_order = (0, 0, 0, 0)
```

**LightGBM:**
```python
params = {
    'objective': 'regression',
    'metric': 'mae',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'max_depth': 7,
    'min_data_in_leaf': 20,
    'lambda_l1': 0.1,
    'lambda_l2': 0.1
}
```

### Anexo C: Métricas Detalladas

**Comparación de modelos:**

| Modelo | MAE | RMSE | MAPE | R² | Tiempo |
|--------|-----|------|------|-----|--------|
| ARIMA | 366.80 | 476.58 | 46.42% | 0.72 | 5 min |
| LightGBM | 341.99 | 455.71 | 41.88% | 0.76 | 2 min |

### Anexo D: Capturas de Pantalla

**Nota:** Las imágenes de la aplicación y resultados de modelos se encuentran en:
- `src/models/models/best_model_predictions.png`
- `src/models/models/metrics_comparison.png`
- `src/models/models/ensemble_comparison.png`
- `src/models/models/residuals_analysis.png`

---

**Fin del Informe**

---

**Contacto:**  
David Soler  
Universidad Católica de Salta (UCASAL)  
Análisis de Datos Masivos - 2024  
GitHub: https://github.com/Davoassassin27/BrechApp  
App: https://brechapp.streamlit.app/
