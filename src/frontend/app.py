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

def load_latest_data():
    try:
        raw_files = [f for f in os.listdir('data/raw') if f.startswith('dolares_') and f.endswith('.json')]
        if raw_files:
            latest_file = sorted(raw_files)[-1]
            with open(f'data/raw/{latest_file}', 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
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
        
        - **📈 Análisis de Mercado**: Compara diferentes tipos de dólar y analiza spreads
        
        ### 🚀 Tecnología
        
        Utilizamos modelos de última generación:
        - **ARIMA**: Análisis de series temporales
        - **LightGBM**: Gradient Boosting optimizado
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

elif page == "📊 Exploración":
    st.title("📊 Exploración del Mercado Cambiario")
    
    latest_data = load_latest_data()
    
    if latest_data:
        st.markdown("### 💰 Cotizaciones en Tiempo Real")
        
        num_dolares = len(latest_data)
        
        if num_dolares >= 5:
            cols = st.columns(5)
        elif num_dolares == 4:
            cols = st.columns(4)
        elif num_dolares == 3:
            cols = st.columns(3)
        elif num_dolares == 2:
            cols = st.columns(2)
        else:
            cols = [st.container()]
        
        for idx, dolar in enumerate(latest_data[:len(cols)]):
            with cols[idx]:
                st.metric(
                    label=f"{dolar['nombre'].title()}",
                    value=f"${dolar['venta']:.2f}",
                    delta=f"Spread: ${dolar['venta'] - dolar['compra']:.2f}"
                )
        
        st.markdown("---")
        st.markdown("### 📊 Detalle de Cotizaciones")
        
        df_cotizaciones = pd.DataFrame(latest_data)
        df_cotizaciones['spread'] = df_cotizaciones['venta'] - df_cotizaciones['compra']
        df_cotizaciones = df_cotizaciones[['nombre', 'compra', 'venta', 'spread']]
        df_cotizaciones.columns = ['Tipo', 'Compra', 'Venta', 'Spread']
        
        st.dataframe(df_cotizaciones, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("### 📈 Comparación Visual")
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_cotizaciones['Tipo'],
            y=df_cotizaciones['Compra'],
            name='Compra',
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            x=df_cotizaciones['Tipo'],
            y=df_cotizaciones['Venta'],
            name='Venta',
            marker_color='darkblue'
        ))
        
        fig.update_layout(
            title='Comparación de Cotizaciones',
            xaxis_title='Tipo de Dólar',
            yaxis_title='Precio (ARS)',
            barmode='group',
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📊 Análisis de Spread")
        
        fig_spread = go.Figure()
        
        fig_spread.add_trace(go.Bar(
            x=df_cotizaciones['Tipo'],
            y=df_cotizaciones['Spread'],
            marker_color='coral',
            text=df_cotizaciones['Spread'].round(2),
            textposition='auto'
        ))
        
        fig_spread.update_layout(
            title='Spread por Tipo de Dólar',
            xaxis_title='Tipo de Dólar',
            yaxis_title='Spread (ARS)',
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_spread, use_container_width=True)
        
    else:
        st.error("No se pudieron cargar los datos actuales.")

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
    
    except FileNotFoundError:
        st.error("⚠️ No se encontró la configuración del modelo. Por favor, ejecuta primero los notebooks de entrenamiento.")
        st.info("Ejecuta los notebooks en el siguiente orden:\n1. 04_Model_Engineering.ipynb\n2. 05_model_ensembling.ipynb")
    except Exception as e:
        st.error(f"Error al cargar la configuración del modelo: {e}")

st.markdown("---")
st.caption("BrechApp © 2025 - Desarrollado por David Soler | Datos actualizados automáticamente")
