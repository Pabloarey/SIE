import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import n_colors

df = pd.read_excel('./data/Resultados 21.xlsx', header=0)
#creo la función de los gráficos para mostrarlos fácilmente en columnas
#función para gráfico de torta
def make_pie(input_df):
  fig = px.pie(input_df, values='total_votos', names='Agrupacion')
  fig.update_layout(
  title_text='% Votos Agrupaciones', title_x=0.35,
  annotations=[dict(text='', showarrow=False,
  x=0.2, y=-0.15, xref='paper', yref='paper')])
  fig.update_layout(legend=dict( orientation="h", ))
  return fig
#función para gráfico de líneas
def make_time_line(data):
  fig = px.line(data, x='Mesa', y='votos', color ='Agrupacion',labels={'votos': 'Cant. Votos'})
  fig.update_layout(
  title_text="Gráfico de cantidad votos por mesa de cada Agrupación", title_x=0.2,
  annotations=[dict(text="", showarrow=False,
  x=0.5, y=-0.15, xref='paper', yref='paper')])
  #cambio ubicación leyenda y fuente de labels de ejes
  fig.update_layout(legend=dict( orientation="h",x=0, y=-0.30),
    xaxis=dict(tickfont=dict(family='Arial', size=9)),
    yaxis=dict(tickfont=dict(family='Arial', size=11))
    )   
  return fig
def make_time_line2(data):
  fig = px.line(data, x='Establecimiento', y='total_votos', color ='Agrupacion',labels={'total_votos': 'Cant. Votos', 'Agrupacion':'Agrupación'})
  fig.update_layout(
  title_text="Gráfico de cantidad votos por mesa de cada Agrupación", title_x=0.2,
  annotations=[dict(text="", showarrow=False,
  x=0.5, y=-0.15, xref='paper', yref='paper')])
  fig.update_layout(legend=dict( orientation="h",x=0, y=-0.40 ),
    xaxis=dict(tickfont=dict(family='Arial', size=7)),
    yaxis=dict(tickfont=dict(family='Arial', size=11)))
  return fig
def make_table(df):
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.Establecimiento, df.Agrupacion, df.total_votos],
                fill_color='lavender',
                align='left'))
    ])
    fig.update_layout(legend=dict( orientation="h",))
    return fig



def show_tablero():  
    # Titulo de la página
    st.header("Resultados electorales")
    # Para elegir la posición a analizar
    st.subheader('Elija la Elección a analizar', divider='rainbow')
    #Calculo los valores únicos de una columna
    opc_ele=df["Eleccion"].unique().tolist()
    opc_circ=df["IdCircuito"].unique().tolist()
    opc_esc=df["Establecimiento"].unique().tolist()
    opc_agrup=df["Agrupacion"].unique().tolist()
    # pongo un caja de selección con los valores únicos
    col1, col2, col3 = st.columns(3)
    Opc_Eleccion = col1.selectbox('Elección', options= opc_ele, index=None, placeholder="Elija la elección...")
    Opc_Circuito = col2.selectbox('Circuito', options= opc_circ, index=None, placeholder="Elija el Circuito Electoral...")
    Opc_Escuela = col3.selectbox('Establecimiento', options= opc_esc, index=None, placeholder="Elija el establecimiento...")
    # costruyo nuevo dataframe con el filtro creado de las elecciones realizadas
    if Opc_Eleccion==None:
        dfnew = df
    else:    
        dfnew = df[df['Eleccion']==Opc_Eleccion]
    if Opc_Circuito==None:
        dfnew = dfnew
    else:    
        dfnew = dfnew[dfnew['IdCircuito']==Opc_Circuito]
    if Opc_Escuela==None:
        dfnew = dfnew
    else:    
        dfnew = dfnew[dfnew['Establecimiento']==Opc_Escuela]
    dfnew=pd.DataFrame(dfnew)
    # construyo los indicadores
    Total = dfnew["votos"].sum()
    Total_pos = dfnew[dfnew['idAgrupacionInt']>0]["votos"].sum()
    Total_est = len(dfnew["Establecimiento"].unique())
    Total_mesa = len(dfnew["Mesa"].unique())
    a, b, c, d = st.columns(4)
    a.metric("Total Votantes", Total, border=True)
    b.metric("Total Votos Positivos", Total_pos, border=True)
    c.metric("Cant. Establecimientos", Total_est, border=True)
    d.metric("Cant. Mesas", Total_mesa, border=True)
    dfpie = dfnew[dfnew['idAgrupacionInt']>0].groupby(['Agrupacion']).agg(total_votos=('votos', 'sum')).reset_index()   
    df_x = dfnew[dfnew['idAgrupacionInt']>0].groupby(['Establecimiento','Agrupacion']).agg(total_votos=('votos', 'sum')).reset_index() 
    pie = make_pie(dfpie)
    time_line = make_time_line(dfnew)
    time_line2 = make_time_line2(df_x)
    time_line3 = make_table(df_x)
    a, b, = st.columns(2)
    a.plotly_chart(pie, use_container_width=True)
    b.plotly_chart(time_line, use_container_width=True)
    a.plotly_chart(time_line2, use_container_width=True)
    b.plotly_chart(time_line3, use_container_width=True)
