import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os

st.set_page_config(
    page_title="BrechApp - Análisis del Dólar Argentino",
    page_icon="💵",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_data():
    try:
        df = pd.read_parquet('data/processed/history.parquet')
        df['fecha'] = pd.to_datetime(df['fecha'])
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return None

def load_latest_data():
    try:
        raw_files = [f for f in os.listdir('data/raw') if f.startswith('dolares_') and f.endswith('.json')]
        if raw_files:
            latest_file = sorted(raw_files)[-1]
            with open(f'data/raw/{latest_file}', 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        st.error(f"Error al cargar datos actuales: {e}")
        return None

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Flag_of_Argentina.svg/200px-Flag_of_Argentina.svg.png", width=100)
    st.title("🇦🇷 BrechApp")
    st.markdown("---")

    page = st.radio(
        "Navegación",
        ["🏠 Inicio", "📊 Exploración", "🔮 Predicción"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**Desarrollado por:**")
    st.markdown("David Soler")
    st.markdown("---")
    st.caption("Datos actualizados en tiempo real")

if page == "🏠 Inicio":
    st.title("💵 BrechApp")
    st.subheader("Una app argentina para argentinos")

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        ### ¿Qué es BrechApp?

        **BrechApp** es una aplicación de análisis y predicción del mercado cambiario argentino,
        diseñada para ayudarte a entender y anticipar las fluctuaciones del dólar en sus diferentes
        modalidades.

        ### 🎯 Características principales:

        - **📊 Exploración en Tiempo Real**: Visualiza las cotizaciones actuales de todos los tipos
          de dólar con métricas clave y gráficos interactivos

        - **🔮 Predicciones Avanzadas**: Modelos de Machine Learning y Deep Learning para predecir
          tendencias futuras del dólar blue

        - **📈 Análisis Histórico**: Accede a datos históricos y analiza patrones de comportamiento

        ### 🚀 Tecnología

        Utilizamos modelos de última generación:
        - **ARIMA**: Análisis de series temporales
        - **LightGBM**: Gradient Boosting optimizado
        - **N-BEATS**: Deep Learning para forecasting
        - **Ensemble Methods**: Combinación inteligente de modelos

        ### 👨‍💻 Autor

        **David Soler**
        Desarrollador y Data Scientist
        Proyecto académico - UCASAL 2025

        ---

        ### 📌 Comienza explorando

        Usa el menú lateral para navegar entre las diferentes secciones de la aplicación.
        """)

    st.markdown("---")

    latest_data = load_latest_data()
    if latest_data:
        st.subheader("💰 Cotizaciones Actuales")

        cols = st.columns(4)
        dolares_principales = ['blue', 'oficial', 'mep', 'ccl']

        for idx, tipo in enumerate(dolares_principales):
            dolar = next((d for d in latest_data if d['nombre'].lower() == tipo), None)
            if dolar:
                with cols[idx]:
                    st.metric(
                        label=f"Dólar {dolar['nombre'].title()}",
                        value=f"${dolar['venta']:.2f}",
                        delta=f"{dolar['venta'] - dolar['compra']:.2f}"
                    )

elif page == "📊 Exploración":
    st.title("📊 Exploración del Mercado Cambiario")

    df = load_data()
    st.markdown("---")

    latest_data = load_latest_data()
    if latest_data:
        st.subheader("💰 Cotizaciones Actuales")

        dolares_principales = ['blue', 'oficial', 'mep', 'ccl']
        dolares_disponibles = [d for d in latest_data if d['nombre'].lower() in dolares_principales]

        if len(dolares_disponibles) >= 4:
            cols = st.columns(4)
        elif len(dolares_disponibles) == 3:
            cols = st.columns(3)
        elif len(dolares_disponibles) == 2:
            cols = st.columns(2)
        else:
            cols = [st.container()]

        for idx, dolar in enumerate(dolares_disponibles[:len(cols)]):
            with cols[idx]:
                st.metric(
                    label=f"Dólar {dolar['nombre'].title()}",
                    value=f"${dolar['venta']:.2f}",
                    delta=f"{dolar['venta'] - dolar['compra']:.2f}"
                )

    if df is not None:
        st.markdown("---")
        st.markdown("### 📈 Análisis Histórico")

        tipos_dolar = df['tipo'].unique().tolist()
        tipo_seleccionado = st.selectbox(
            "Selecciona el tipo de dólar:",
            options=['Todos'] + tipos_dolar,
            index=0
        )

        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            fecha_min = df['fecha'].min().date()
            fecha_max = df['fecha'].max().date()

            fecha_inicio, fecha_fin = st.date_input(
                "Rango de fechas:",
                value=(fecha_max - timedelta(days=90), fecha_max),
                min_value=fecha_min,
                max_value=fecha_max
            )

        with col2:
            metrica_viz = st.selectbox(
                "Métrica a visualizar:",
                options=['Venta', 'Compra', 'Promedio', 'Spread']
            )

        with col3:
            metrica_viz = st.selectbox(
                "Métrica a visualizar:",
                options=['Venta', 'Compra', 'Promedio', 'Spread']
            )

        df_filtrado = df[
            (df['fecha'].dt.date >= fecha_inicio) &
            (df['fecha'].dt.date <= fecha_fin)
        ].copy()

        if tipo_seleccionado != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['tipo'] == tipo_seleccionado]

        if len(df_filtrado) == 0:
            st.warning("No hay datos disponibles para el rango de fechas seleccionado.")
        else:
            if metrica_viz == 'Promedio':
                df_filtrado['valor'] = (df_filtrado['venta'] + df_filtrado['compra']) / 2
            elif metrica_viz == 'Spread':
                df_filtrado['valor'] = df_filtrado['venta'] - df_filtrado['compra']
            else:
                df_filtrado['valor'] = df_filtrado[metrica_viz.lower()]

            fig = go.Figure()

            if tipo_seleccionado == 'Todos':
                for tipo in df_filtrado['tipo'].unique():
                    df_tipo = df_filtrado[df_filtrado['tipo'] == tipo]
                    fig.add_trace(go.Scatter(
                        x=df_tipo['fecha'],
                        y=df_tipo['valor'],
                        mode='lines',
                        name=tipo.title(),
                        line=dict(width=2)
                    ))
            else:
                fig.add_trace(go.Scatter(
                    x=df_filtrado['fecha'],
                    y=df_filtrado['valor'],
                    mode='lines',
                    name=tipo_seleccionado.title(),
                    line=dict(width=3, color='#1f77b4'),
                    fill='tozeroy',
                    fillcolor='rgba(31, 119, 180, 0.1)'
                ))

            fig.update_layout(
                title=f'Evolución del Dólar - {metrica_viz}',
                xaxis_title='Fecha',
                yaxis_title=f'{metrica_viz} (ARS)',
                hovermode='x unified',
                height=500,
                template='plotly_white'
            )

            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            st.markdown("### 📊 Métricas Estadísticas")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Valor Actual",
                    f"${df_filtrado['valor'].iloc[-1]:.2f}"
                )

            with col2:
                st.metric(
                    "Promedio",
                    f"${df_filtrado['valor'].mean():.2f}"
                )

            with col3:
                st.metric(
                    "Máximo",
                    f"${df_filtrado['valor'].max():.2f}"
                )

            with col4:
                st.metric(
                    "Mínimo",
                    f"${df_filtrado['valor'].min():.2f}"
                )

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📉 Distribución de Valores")
                fig_hist = px.histogram(
                    df_filtrado,
                    x='valor',
                    nbins=30,
                    title=f'Distribución de {metrica_viz}',
                    labels={'valor': f'{metrica_viz} (ARS)', 'count': 'Frecuencia'}
                )
                fig_hist.update_layout(height=400, template='plotly_white')
                st.plotly_chart(fig_hist, use_container_width=True)

            with col2:
                st.markdown("#### 📊 Volatilidad (Desviación Estándar)")

                if len(df_filtrado) >= 7:
                    df_filtrado_sorted = df_filtrado.sort_values('fecha')
                    df_filtrado_sorted['volatilidad'] = df_filtrado_sorted.groupby('tipo')['valor'].transform(
                        lambda x: x.rolling(window=7, min_periods=1).std()
                    )

                    fig_vol = go.Figure()

                    if tipo_seleccionado == 'Todos':
                        for tipo in df_filtrado_sorted['tipo'].unique():
                            df_tipo = df_filtrado_sorted[df_filtrado_sorted['tipo'] == tipo]
                            fig_vol.add_trace(go.Scatter(
                                x=df_tipo['fecha'],
                                y=df_tipo['volatilidad'],
                                mode='lines',
                                name=tipo.title()
                            ))
                    else:
                        fig_vol.add_trace(go.Scatter(
                            x=df_filtrado_sorted['fecha'],
                            y=df_filtrado_sorted['volatilidad'],
                    mode='lines',
                    name='Volatilidad',
                    line=dict(color='red', width=2)
                ))

            fig_vol.update_layout(
                title='Volatilidad en el Tiempo',
                xaxis_title='Fecha',
                yaxis_title='Desviación Estándar',
                height=400,
                template='plotly_white'
            )
            st.plotly_chart(fig_vol, use_container_width=True)

elif page == "🔮 Predicción":
    st.title("🔮 Predicción del Dólar Blue")

    st.warning("⚠️ **FASE DE DESARROLLO** - Esta funcionalidad está en construcción y los resultados son experimentales.")

    st.markdown("---")

    try:
        with open('src/models/models/final_model_config.json', 'r') as f:
            model_config = json.load(f)

        st.markdown("### 🤖 Modelo Seleccionado")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Modelo", model_config['best_model'])

        with col2:
            st.metric("MAE", f"{model_config['metrics']['mae']:.2f}")

        with col3:
            st.metric("MAPE", f"{model_config['metrics']['mape']:.2f}%")

        st.markdown("---")
        st.markdown("### 📊 Métricas del Modelo")

        metrics_df = pd.DataFrame({
            'Métrica': ['MAE', 'RMSE', 'MAPE'],
            'Valor': [
                f"{model_config['metrics']['mae']:.2f}",
                f"{model_config['metrics']['rmse']:.2f}",
                f"{model_config['metrics']['mape']:.2f}%"
            ],
            'Descripción': [
                'Error Absoluto Medio',
                'Raíz del Error Cuadrático Medio',
                'Error Porcentual Absoluto Medio'
            ]
        })

        st.dataframe(metrics_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### 🔧 Configuración del Modelo")

        if model_config['ensemble_type']:
            st.info(f"**Tipo de Ensemble:** {model_config['ensemble_type'].replace('_', ' ').title()}")

            if model_config['weights']:
                st.markdown("**Pesos del Ensemble:**")
                weights_df = pd.DataFrame({
                    'Modelo': ['ARIMA', 'LightGBM', 'N-BEATS'][:len(model_config['weights'])],
                    'Peso': model_config['weights']
                })
                st.dataframe(weights_df, use_container_width=True, hide_index=True)

            if model_config['meta_model']:
                st.markdown(f"**Meta-modelo:** {model_config['meta_model']}")

        st.markdown("---")
        st.markdown("### 🎯 Predicciones Futuras")

        st.info("🚧 Las predicciones futuras estarán disponibles próximamente. Actualmente el modelo está en fase de validación.")

        horizonte = st.slider("Horizonte de predicción (días)", 7, 30, 14)

        if st.button("Generar Predicción", type="primary", disabled=True):
            st.warning("Esta funcionalidad estará disponible en la próxima versión.")

        st.markdown("---")
        st.markdown("### 📈 Visualización de Resultados Históricos")

        st.info("🚧 **EN DESARROLLO** - Visualización de predicciones en construcción")

        try:
            img_path = 'src/models/models/best_model_predictions.png'
            if os.path.exists(img_path):
                col1, col2, col3 = st.columns([1, 3, 1])
                with col2:
                    st.image(img_path, caption='Predicciones del Mejor Modelo (Datos Históricos)', use_container_width=True)

                st.caption("⚠️ Nota: Este gráfico muestra el rendimiento del modelo en datos históricos. Las predicciones futuras estarán disponibles próximamente.")
            else:
                st.warning("No hay gráficos de predicción disponibles aún. Ejecuta los notebooks de entrenamiento primero.")
        except Exception as e:
            st.error(f"Error al cargar visualización: {e}")

        st.markdown("---")
        st.markdown("### ℹ️ Información del Desarrollo")

        with st.expander("📋 Estado del Proyecto"):
            st.markdown("""
            **Funcionalidades Completadas:**
            - ✅ Carga y procesamiento de datos históricos
            - ✅ Entrenamiento de modelos base (ARIMA, LightGBM)
            - ✅ Ensemble de modelos
            - ✅ Evaluación de métricas

            **En Desarrollo:**
            - 🚧 Predicciones en tiempo real
            - 🚧 API de predicción
            - 🚧 Actualización automática de modelos
            - 🚧 Intervalos de confianza

            **Próximamente:**
            - 📅 Alertas personalizadas
            - 📅 Análisis de sentimiento de noticias
            - 📅 Comparación con indicadores económicos
            """)

        try:
            import matplotlib.pyplot as plt
            from PIL import Image

            img_path = 'src/models/models/best_model_predictions.png'
            if os.path.exists(img_path):
                st.image(img_path, caption='Predicciones del Mejor Modelo', use_container_width=True)
            else:
                st.info("No hay gráficos de predicción disponibles aún.")
        except Exception as e:
            st.error(f"Error al cargar visualización: {e}")

    except FileNotFoundError:
        st.error("⚠️ No se encontró la configuración del modelo. Por favor, ejecuta primero los notebooks de entrenamiento.")
        st.info("Ejecuta los notebooks en el siguiente orden:\n1. 04_Model_Engineering.ipynb\n2. 05_model_ensembling.ipynb")
    except Exception as e:
        st.error(f"Error al cargar la configuración del modelo: {e}")

st.markdown("---")
st.caption("BrechApp © 2024 - Desarrollado por David Soler | Datos actualizados automáticamente")
