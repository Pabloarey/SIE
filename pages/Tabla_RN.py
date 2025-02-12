import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib
from matplotlib import colormaps

df = pd.read_excel('C:/FUTBOL/Predichos RN Defensores Goles.xlsx', header=0, sheet_name="Sheet1")

def show_Tabla_RN():
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
    st.header('Tabla Estimaciones Modelo IA')
    st.dataframe(df.style.background_gradient(axis=0, cmap='RdYlGn', subset=['Posición','Aforo']).format({'Aforo':'{:.0%}'}),hide_index=True)

    