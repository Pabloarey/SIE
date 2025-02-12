import streamlit as st
import pandas as pd

df = pd.read_excel('C:/FUTBOL/Simulación Copa America 24/FUENTE_JUGADORES.xlsx', header=0, sheet_name="ACP Defensa")


def show_Tabla_AM():
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Jugadores", value=len(df), delta="0 %")
    st.markdown("""
    <style>
        [data-testid="stMetric"] {
        background-color: #fefbdd;
        border: 2px solid #000000;
        text-align: center;
        padding: 15px 0;
        }
        [data-testid="stMetricLabel"] {
        display: flex;
        justify-content: center;
        align-items: center;
        }
    </style>
    """
    , unsafe_allow_html=True)
    st.header('Tabla Análisis Multivariado')
    st.write(df)
    
