# Plan de Modelado: Predicción de Precio y Volatilidad del Dólar en Argentina

## Contexto del Proyecto

BrechApp es un sistema de análisis y predicción de la brecha cambiaria del dólar en Argentina, que integra datos de múltiples tipos de cambio (oficial, blue, MEP, CCL) para modelar y simular la dinámica cambiaria en un contexto de alta volatilidad e incertidumbre.

---

## Objetivos del Modelado

### Objetivo Principal
Desarrollar un conjunto de modelos de Machine Learning y Deep Learning para:
1. **Predicción de Precio Exacto**: Forecasting de valores futuros de tipos de cambio (oficial, blue, MEP, CCL)
2. **Predicción de Volatilidad**: Estimación de la variabilidad y riesgo asociado a cada tipo de cambio
3. **Simulación de Escenarios**: Generación de trayectorias sintéticas bajo diferentes condiciones macroeconómicas

### Objetivos Específicos
- Capturar patrones no lineales y dependencias temporales complejas
- Modelar la heterocedasticidad condicional (volatilidad variable en el tiempo)
- Incorporar variables exógenas (inflación, tasas, riesgo país, reservas)
- Generar intervalos de confianza y cuantificación de incertidumbre
- Permitir simulación de shocks regulatorios y cambios de política

---

## Arquitectura de Modelado Propuesta

### Fase 1: Modelos Estadísticos Clásicos (Baseline)

#### 1.1 ARIMA/SARIMA
**Propósito**: Predicción de precio a corto plazo

**Características**:
- Modelo autorregresivo integrado de medias móviles
- Captura tendencias, estacionalidad y autocorrelación
- Interpretable y rápido de entrenar

**Implementación**:
```python
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

# ARIMA(p,d,q) - orden a determinar por ACF/PACF
model = ARIMA(data, order=(5,1,2))
# SARIMA con componente estacional
model = SARIMAX(data, order=(5,1,2), seasonal_order=(1,1,1,7))
```

**Ventajas**: Simple, interpretable, buen baseline
**Limitaciones**: Asume linealidad, no captura cambios estructurales abruptos

---

#### 1.2 Prophet (Facebook)
**Propósito**: Predicción con componentes de tendencia y estacionalidad

**Características**:
- Descomposición aditiva: y(t) = g(t) + s(t) + h(t) + ε(t)
- Robusto a datos faltantes y outliers
- Permite incorporar holidays y eventos especiales

**Implementación**:
```python
from prophet import Prophet

model = Prophet(
    changepoint_prior_scale=0.05,
    seasonality_mode='multiplicative',
    yearly_seasonality=True,
    weekly_seasonality=True
)
# Agregar regresores externos
model.add_regressor('inflacion')
model.add_regressor('riesgo_pais')
```

**Ventajas**: Maneja bien tendencias cambiantes, fácil de usar
**Limitaciones**: No captura dependencias complejas entre variables

---

#### 1.3 GARCH (Generalized Autoregressive Conditional Heteroskedasticity)
**Propósito**: Predicción de volatilidad

**Características**:
- Modela la varianza condicional como función del tiempo
- Captura clustering de volatilidad (períodos de alta/baja volatilidad)
- Variantes: GARCH, EGARCH, GJR-GARCH

**Implementación**:
```python
from arch import arch_model

# GARCH(1,1) - configuración estándar
model = arch_model(returns, vol='Garch', p=1, q=1)
# EGARCH para asimetría (leverage effect)
model = arch_model(returns, vol='EGARCH', p=1, q=1)
```

**Ventajas**: Especializado en volatilidad, bien establecido en finanzas
**Limitaciones**: Solo modela volatilidad, no precio directamente

---

### Fase 2: Modelos de Machine Learning

#### 2.1 XGBoost / LightGBM
**Propósito**: Predicción de precio con features engineered

**Características**:
- Gradient boosting de árboles de decisión
- Maneja no linealidades y interacciones complejas
- Permite feature importance

**Features Propuestas**:
```python
features = [
    # Lags de precio
    'precio_t-1', 'precio_t-7', 'precio_t-30',
    # Medias móviles
    'ma_7', 'ma_30', 'ma_90',
    # Volatilidad histórica
    'std_7', 'std_30',
    # Retornos
    'return_1d', 'return_7d',
    # Indicadores técnicos
    'rsi', 'macd', 'bollinger_bands',
    # Variables exógenas
    'inflacion', 'tasa_interes', 'riesgo_pais', 'reservas_bcra',
    # Brecha cambiaria
    'brecha_blue_oficial', 'brecha_mep_oficial',
    # Features temporales
    'dia_semana', 'dia_mes', 'mes', 'trimestre'
]
```

**Implementación**:
```python
import xgboost as xgb
import lightgbm as lgb

# XGBoost
model = xgb.XGBRegressor(
    n_estimators=1000,
    learning_rate=0.01,
    max_depth=7,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='reg:squarederror'
)

# LightGBM (más rápido)
model = lgb.LGBMRegressor(
    n_estimators=1000,
    learning_rate=0.01,
    num_leaves=31,
    feature_fraction=0.8
)
```

**Ventajas**: Alta precisión, maneja features heterogéneas, interpretable
**Limitaciones**: Requiere feature engineering manual, no captura dependencias temporales largas

---

#### 2.2 Random Forest con Quantile Regression
**Propósito**: Predicción con intervalos de confianza

**Características**:
- Ensemble de árboles de decisión
- Quantile Regression Forest para estimar percentiles
- Cuantificación de incertidumbre

**Implementación**:
```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

# Random Forest estándar
rf = RandomForestRegressor(n_estimators=500, max_depth=10)

# Quantile Regression para intervalos
qrf_lower = GradientBoostingRegressor(loss='quantile', alpha=0.05)
qrf_upper = GradientBoostingRegressor(loss='quantile', alpha=0.95)
```

**Ventajas**: Robusto, estima incertidumbre
**Limitaciones**: Menos preciso que XGBoost en series temporales

---

### Fase 3: Modelos de Deep Learning

#### 3.1 LSTM (Long Short-Term Memory)
**Propósito**: Predicción de precio capturando dependencias temporales largas

**Características**:
- Red neuronal recurrente con memoria a largo plazo
- Captura patrones secuenciales complejos
- Maneja múltiples variables (multivariado)

**Arquitectura Propuesta**:
```python
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional

model = Sequential([
    # Capa LSTM bidireccional
    Bidirectional(LSTM(128, return_sequences=True, input_shape=(lookback, n_features))),
    Dropout(0.2),
    
    # Segunda capa LSTM
    LSTM(64, return_sequences=False),
    Dropout(0.2),
    
    # Capas densas
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(1)  # Predicción de precio
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])
```

**Configuración**:
- Lookback window: 30-60 días
- Features: precio, volumen, variables exógenas
- Batch size: 32-64
- Epochs: 100-200 con early stopping

**Ventajas**: Captura dependencias temporales complejas, multivariado
**Limitaciones**: Requiere muchos datos, difícil de interpretar, propenso a overfitting

---

#### 3.2 GRU (Gated Recurrent Unit)
**Propósito**: Alternativa más eficiente a LSTM

**Características**:
- Similar a LSTM pero con menos parámetros
- Más rápido de entrenar
- Buen rendimiento en series temporales

**Arquitectura**:
```python
from tensorflow.keras.layers import GRU

model = Sequential([
    GRU(128, return_sequences=True, input_shape=(lookback, n_features)),
    Dropout(0.2),
    GRU(64),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dense(1)
])
```

**Ventajas**: Más eficiente que LSTM, buen rendimiento
**Limitaciones**: Similares a LSTM

---

#### 3.3 Transformer / Temporal Fusion Transformer (TFT)
**Propósito**: Predicción con atención temporal y variables exógenas

**Características**:
- Mecanismo de atención para capturar relaciones temporales
- Maneja variables estáticas, conocidas y desconocidas
- Interpretabilidad mediante attention weights

**Implementación** (usando PyTorch Forecasting):
```python
from pytorch_forecasting import TemporalFusionTransformer, TimeSeriesDataSet

# Definir dataset
training = TimeSeriesDataSet(
    data,
    time_idx="time_idx",
    target="precio",
    group_ids=["tipo_cambio"],
    max_encoder_length=60,
    max_prediction_length=30,
    static_categoricals=["tipo_cambio"],
    time_varying_known_reals=["inflacion", "tasa_interes"],
    time_varying_unknown_reals=["precio", "volumen"],
)

# Modelo TFT
tft = TemporalFusionTransformer.from_dataset(
    training,
    learning_rate=0.03,
    hidden_size=64,
    attention_head_size=4,
    dropout=0.1,
    hidden_continuous_size=32,
)
```

**Ventajas**: Estado del arte en forecasting, interpretable, maneja múltiples horizontes
**Limitaciones**: Complejo, requiere muchos datos, costoso computacionalmente

---

#### 3.4 N-BEATS (Neural Basis Expansion Analysis for Time Series)
**Propósito**: Forecasting puro sin features exógenas

**Características**:
- Arquitectura específica para series temporales
- Descomposición en tendencia y estacionalidad
- No requiere feature engineering

**Implementación**:
```python
from darts.models import NBEATSModel

model = NBEATSModel(
    input_chunk_length=60,
    output_chunk_length=30,
    num_stacks=30,
    num_blocks=1,
    num_layers=4,
    layer_widths=256,
    expansion_coefficient_dim=5,
    trend_polynomial_degree=2
)
```

**Ventajas**: Excelente para forecasting puro, interpretable
**Limitaciones**: No incorpora variables exógenas fácilmente

---

#### 3.5 WaveNet
**Propósito**: Captura patrones de alta frecuencia

**Características**:
- Convoluciones dilatadas causales
- Receptive field muy grande
- Originalmente para audio, adaptado a series temporales

**Arquitectura**:
```python
from tensorflow.keras.layers import Conv1D, Add

def wavenet_block(x, filters, kernel_size, dilation_rate):
    tanh_out = Conv1D(filters, kernel_size, dilation_rate=dilation_rate, 
                      padding='causal', activation='tanh')(x)
    sigm_out = Conv1D(filters, kernel_size, dilation_rate=dilation_rate, 
                      padding='causal', activation='sigmoid')(x)
    z = tf.multiply(tanh_out, sigm_out)
    skip = Conv1D(filters, 1)(z)
    res = Add()([x, skip])
    return res, skip
```

**Ventajas**: Captura patrones de alta frecuencia, receptive field grande
**Limitaciones**: Complejo, requiere ajuste fino

---

### Fase 4: Modelos Híbridos y Ensemble

#### 4.1 LSTM + GARCH
**Propósito**: Predicción de precio y volatilidad conjunta

**Estrategia**:
1. LSTM predice el precio medio
2. GARCH modela la volatilidad de los residuos del LSTM
3. Combinar para generar intervalos de predicción

```python
# Paso 1: LSTM para precio
lstm_pred = lstm_model.predict(X)

# Paso 2: Calcular residuos
residuals = y_true - lstm_pred

# Paso 3: GARCH para volatilidad de residuos
garch_model = arch_model(residuals, vol='Garch', p=1, q=1)
garch_fit = garch_model.fit()
volatility_forecast = garch_fit.forecast(horizon=30)

# Paso 4: Intervalos de predicción
lower_bound = lstm_pred - 1.96 * volatility_forecast
upper_bound = lstm_pred + 1.96 * volatility_forecast
```

---

#### 4.2 Ensemble Multi-Modelo
**Propósito**: Combinar fortalezas de múltiples modelos

**Estrategia**:
```python
# Modelos base
models = {
    'arima': arima_model,
    'prophet': prophet_model,
    'xgboost': xgb_model,
    'lstm': lstm_model,
    'tft': tft_model
}

# Predicciones individuales
predictions = {name: model.predict(X) for name, model in models.items()}

# Ensemble por promedio ponderado
weights = {'arima': 0.15, 'prophet': 0.15, 'xgboost': 0.25, 'lstm': 0.25, 'tft': 0.20}
ensemble_pred = sum(weights[name] * pred for name, pred in predictions.items())

# Ensemble por stacking (meta-modelo)
from sklearn.linear_model import Ridge
meta_model = Ridge()
meta_features = np.column_stack(list(predictions.values()))
meta_model.fit(meta_features, y_true)
stacked_pred = meta_model.predict(meta_features)
```

---

#### 4.3 Bayesian Deep Learning
**Propósito**: Cuantificación de incertidumbre epistémica

**Implementación** (usando TensorFlow Probability):
```python
import tensorflow_probability as tfp

# LSTM Bayesiano
model = Sequential([
    tfp.layers.DenseVariational(128, activation='relu'),
    LSTM(64),
    tfp.layers.DenseVariational(1)
])

# Predicción con incertidumbre
predictions = [model(X) for _ in range(100)]  # Monte Carlo sampling
mean_pred = np.mean(predictions, axis=0)
std_pred = np.std(predictions, axis=0)
```

**Ventajas**: Cuantifica incertidumbre del modelo, no solo de los datos
**Limitaciones**: Costoso computacionalmente

---

## Estrategia de Implementación

### Fase 1: Baseline (Semanas 1-2)
1. Implementar ARIMA/SARIMA
2. Implementar Prophet
3. Implementar GARCH para volatilidad
4. Establecer métricas de evaluación

### Fase 2: Machine Learning (Semanas 3-4)
1. Feature engineering extensivo
2. Implementar XGBoost/LightGBM
3. Implementar Random Forest con quantile regression
4. Comparar con baseline

### Fase 3: Deep Learning (Semanas 5-7)
1. Implementar LSTM/GRU
2. Implementar Temporal Fusion Transformer
3. Implementar N-BEATS
4. Optimización de hiperparámetros

### Fase 4: Modelos Avanzados (Semanas 8-10)
1. Implementar modelos híbridos (LSTM+GARCH)
2. Crear ensemble multi-modelo
3. Implementar Bayesian DL para incertidumbre
4. Validación exhaustiva

---

## Métricas de Evaluación

### Para Predicción de Precio
```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# MAE: Error absoluto medio
mae = mean_absolute_error(y_true, y_pred)

# RMSE: Raíz del error cuadrático medio
rmse = np.sqrt(mean_squared_error(y_true, y_pred))

# MAPE: Error porcentual absoluto medio
mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# R²: Coeficiente de determinación
r2 = r2_score(y_true, y_pred)

# Directional Accuracy: % de veces que predice correctamente la dirección
da = np.mean(np.sign(y_true[1:] - y_true[:-1]) == np.sign(y_pred[1:] - y_pred[:-1]))
```

### Para Predicción de Volatilidad
```python
# MSE de volatilidad realizada vs predicha
vol_mse = mean_squared_error(realized_vol, predicted_vol)

# QLIKE: Quasi-likelihood
qlike = np.mean(realized_vol / predicted_vol - np.log(realized_vol / predicted_vol) - 1)
```

### Para Intervalos de Predicción
```python
# Coverage: % de observaciones dentro del intervalo
coverage = np.mean((y_true >= lower_bound) & (y_true <= upper_bound))

# Interval Width: Ancho promedio del intervalo
interval_width = np.mean(upper_bound - lower_bound)
```

---

## Validación y Testing

### Estrategia de Validación
1. **Time Series Split**: División temporal estricta (no shuffle)
   ```python
   from sklearn.model_selection import TimeSeriesSplit
   
   tscv = TimeSeriesSplit(n_splits=5)
   for train_idx, val_idx in tscv.split(X):
       X_train, X_val = X[train_idx], X[val_idx]
       y_train, y_val = y[train_idx], y[val_idx]
   ```

2. **Walk-Forward Validation**: Reentrenamiento periódico
   ```python
   # Entrenar con datos hasta t, predecir t+1, agregar t+1 a training, repetir
   ```

3. **Backtesting**: Simulación de trading real
   ```python
   # Evaluar performance en condiciones realistas de mercado
   ```

---

## Consideraciones Especiales para Argentina

### 1. Cambios Estructurales
- Detectar y manejar cambios de régimen (controles cambiarios, devaluaciones)
- Usar modelos con changepoint detection (Prophet, Bayesian changepoint)

### 2. Datos Faltantes
- Fines de semana y feriados
- Períodos de mercado cerrado
- Imputación inteligente vs. forward fill

### 3. Outliers y Shocks
- Eventos políticos (elecciones, cambios de gobierno)
- Anuncios de política económica
- Crisis externas
- Usar modelos robustos o detección de anomalías

### 4. Variables Exógenas Clave
- Inflación (IPC, IPM)
- Tasa de interés (BADLAR, LELIQ)
- Riesgo país (EMBI+)
- Reservas del BCRA
- Base monetaria
- Resultado fiscal
- Balanza comercial

---

## Infraestructura y Herramientas

### Librerías Principales
```python
# Estadística clásica
statsmodels
prophet
arch

# Machine Learning
scikit-learn
xgboost
lightgbm

# Deep Learning
tensorflow / keras
pytorch
pytorch-forecasting
darts

# Utilidades
pandas
numpy
matplotlib
seaborn
plotly
```

### Pipeline de Entrenamiento
```python
# 1. Carga de datos
data = load_data()

# 2. Preprocesamiento
data_clean = preprocess(data)

# 3. Feature engineering
features = engineer_features(data_clean)

# 4. Split temporal
train, val, test = time_split(features)

# 5. Entrenamiento
model = train_model(train, val)

# 6. Evaluación
metrics = evaluate(model, test)

# 7. Guardado
save_model(model, metrics)
```

---

## Roadmap de Implementación

### Mes 1: Fundamentos
- ✅ Setup del proyecto
- ✅ Recolección y limpieza de datos
- ✅ EDA exhaustivo
- 🔄 Implementación de modelos baseline (ARIMA, Prophet, GARCH)

### Mes 2: Machine Learning
- Feature engineering avanzado
- Implementación de XGBoost/LightGBM
- Optimización de hiperparámetros
- Validación cruzada temporal

### Mes 3: Deep Learning
- Implementación de LSTM/GRU
- Implementación de Transformer/TFT
- Experimentación con arquitecturas
- Comparación exhaustiva

### Mes 4: Modelos Avanzados y Producción
- Modelos híbridos y ensemble
- Cuantificación de incertidumbre
- Integración con API
- Dashboard interactivo
- Documentación final

---

## Conclusión

Este plan propone una estrategia integral que combina:
1. **Modelos estadísticos clásicos** para baseline e interpretabilidad
2. **Machine Learning** para capturar no linealidades con features engineered
3. **Deep Learning** para dependencias temporales complejas
4. **Modelos híbridos** para combinar fortalezas

La implementación será iterativa, comenzando con modelos simples y avanzando hacia arquitecturas más complejas, siempre validando con métricas rigurosas y considerando las particularidades del mercado cambiario argentino.
