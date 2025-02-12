import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_excel('C:/FUTBOL/Simulación Copa America 24/FUENTE_JUGADORES.xlsx', header=0, sheet_name="ACP Defensa")

def show_Grafico_AM():
    col1, col2 = st.columns(2)
    
    x_axis_val = col1.selectbox('Select the X-axis', options=df.columns, )
    y_axis_val = col2.selectbox('Select the Y-axis', options=df.columns)

    plot = px.scatter(df, x=x_axis_val, y=y_axis_val, hover_name=df['Jugador'])
    st.plotly_chart(plot, use_container_width=True)
