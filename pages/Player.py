import streamlit as st
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn_extra.cluster import KMedoids
import pandas as pd
import plotly.graph_objects as go
import kmedoids, numpy
from sklearn.datasets import fetch_openml
from sklearn.metrics.pairwise import euclidean_distances
import plotly.figure_factory as ff
from mplsoccer import Radar, FontManager, grid
import numpy as np
import os

movil=pd.read_csv('./data/Jugador_movil.csv',encoding='utf-8-sig')
Stats_Varias=pd.read_csv('./data/Stats_Varias.csv',encoding='utf-8-sig')
Stats_Defense=pd.read_csv('./data/Stats_Defense.csv',encoding='utf-8-sig')
Stats_Disparo=pd.read_csv('./data/Stats_Disparo.csv',encoding='utf-8-sig')
Stats_Pases=pd.read_csv('./data/Stats_Pases.csv',encoding='utf-8-sig')
Stats_Posesión=pd.read_csv('./data/Stats_Posesión.csv',encoding='utf-8-sig')
Stats_GK=pd.read_csv('./data/Stats_GK.csv',encoding='utf-8-sig')
jugador = pd.read_excel('./data/Jugador.xlsx', header=0)
jugador["Born"] = pd.to_datetime(jugador["Born"], format="%d/%m/%Y").dt.date
club = pd.read_excel('./data/Club.xlsx', header=0)
jugadoresnew = pd.merge(movil,jugador, on='id_jugador',how='left')
jugadoresnew = pd.merge(jugadoresnew,club, on='id_club',how='left')
fotos = os.listdir('./Fotos_scoutech')


def show_player():
    # Titulo de la página
    st.header("Análisis Comparativo de Jugadores")
    # Para elegir la posición a analizar
    st.subheader('Elija la Posición a analizar', divider='rainbow')
    Position = st.selectbox('Seleccione la posición', options= ['Defensa','Mediocampo','Delantero','Portero'])
    df = jugadoresnew[jugadoresnew['Posicion_agrup']==Position]
    # Elige la cantidad de jugadores a comparar
    st.subheader('Selecciona la cantidad de jugadores a comparar', divider='rainbow')
    start, end = st.select_slider("Elige la cantidad de Jugadores...",
        options=["3","6"],
        value=("3", "3"),)
    # Elige los jugadores a comparar
    st.subheader('Elija los Jugadores a analizar', divider='rainbow')
    col1, col2, col3 = st.columns(3)
    if end=="3":
        Club1 = col1.selectbox('Select Club', options=df['nombre'].unique(),key="1")
        Player1 = col1.selectbox('Select Player', options=df[df['nombre']==Club1]['Nombre'],key="Jugador1")
        Club2 = col2.selectbox('Select Club', options=df['nombre'].unique(),key="2")
        Player2 = col2.selectbox('Select Player', options=df[(df['nombre']==Club2)&(df['Nombre']!=Player1)]['Nombre'],key="Jugador2")
        Club3 = col3.selectbox('Select Club', options=df['nombre'].unique(),key="3")
        Player3 = col3.selectbox('Select Player', options=df[(df['nombre']==Club3)&(df['Nombre']!=Player1)&(df['Nombre']!=Player2)]['Nombre'],key="Jugador3")
    else:
        Club1 = col1.selectbox('Select Club', options=df['nombre'].unique(),key="1")
        Player1 = col1.selectbox('Select Player', options=df[df['nombre']==Club1]['Nombre'],key="Jugador1")
        Club2 = col2.selectbox('Select Club', options=df['nombre'].unique(),key="2")
        Player2 = col2.selectbox('Select Player', options=df[df['nombre']==Club2]['Nombre'],key="Jugador2")
        Club3 = col3.selectbox('Select Club', options=df['nombre'].unique(),key="3")
        Player3 = col3.selectbox('Select Player', options=df[df['nombre']==Club3]['Nombre'],key="Jugador3")
        Club4 = col1.selectbox('Select Club', options=df['nombre'].unique(),key="4")
        Player4 = col1.selectbox('Select Player', options=df[df['nombre']==Club4]['Nombre'],key="Jugador4")
        Club5 = col2.selectbox('Select Club', options=df['nombre'].unique(),key="5")
        Player5 = col2.selectbox('Select Player', options=df[df['nombre']==Club5]['Nombre'],key="Jugador5")
        Club6 = col3.selectbox('Select Club', options=df['nombre'].unique(),key="6")
        Player6 = col3.selectbox('Select Player', options=df[df['nombre']==Club6]['Nombre'],key="Jugador6")
    # muestra datos de los jugadores seleccionados
    if end=="3":
        Jugador1 = df[df['Nombre']==Player1]
        for i in range(len(Jugador1)):    
            a=Jugador1.iloc[i]
        if pd.isna(a['Nacionalidad']):
            l1=""
        else:
            l1=a['Nacionalidad'].replace("['","").replace("']","").replace("', '"," / ")
        if f"{str(a['id_jugador'])}.jpg" in fotos:
            col1.image(f"./Fotos_scoutech/{a['id_jugador']}.jpg", width=100)
        else: 
            col1.image(f"./Fotos_scoutech/default.jpg", width=100)
        col1.markdown(f"**{a['Nombre']}**")
        col1.markdown(f"{a['Born']} - {l1}")
        col1.markdown(f"{a['Altura']} - {a['Pie']} - {a['nombre']}")   
        Jugador2 = df[df["Nombre"]==Player2]
        for i in range(len(Jugador2)):    
            b=Jugador2.iloc[i]
        l2=b['Nacionalidad'].replace("['","").replace("']","").replace("', '"," / ")
        if f"{b['id_jugador']}.jpg" in fotos:
            col2.image(f"./Fotos_scoutech/{b['id_jugador']}.jpg", width=100)
        else: 
            col2.image(f"./Fotos_scoutech/default.jpg", width=100)
        col2.markdown(f"**{b['Nombre']}**")
        col2.markdown(f"{b['Born']} - {l2}")
        col2.markdown(f"{b['Altura']} - {b['Pie']} - {b['nombre']}")
        Jugador3 = df[df["Nombre"]==Player3]
        for i in range(len(Jugador3)):    
            c=Jugador3.iloc[i]
        l3=c['Nacionalidad'].replace("['","").replace("']","").replace("', '"," / ")
        if f"{c['id_jugador']}.jpg" in fotos:
            col3.image(f"./Fotos_scoutech/{c['id_jugador']}.jpg", width=100)
        else: 
            col3.image(f"./Fotos_scoutech/default.jpg", width=100)
        col3.markdown(f"**{c['Nombre']}**")
        col3.markdown(f"{c['Born']} - {l3}")
        col3.markdown(f"{c['Altura']} - {c['Pie']} - {c['nombre']}")
    else:
        Jugador1 = df[df['Nombre']==Player1]    
        for i in range(len(Jugador1)):    
            a=Jugador1.iloc[i]
        l1=a['Nacionalidad'].replace("['","").replace("']","").replace("', '"," / ")
        if f"{str(a['id_jugador'])}.jpg" in fotos:
            col1.image(f"./Fotos_scoutech/{a['id_jugador']}.jpg", width=100)
        else: 
            col1.image(f"./Fotos_scoutech/default.jpg", width=100)
        col1.markdown(f"**{a['Nombre']}**")
        col1.markdown(f"{a['Born']} - {l1}")
        col1.markdown(f"{a['Altura']} - {a['Pie']} - {a['nombre']}")   
        Jugador2 = df[df["Nombre"]==Player2]
        for i in range(len(Jugador2)):    
            b=Jugador2.iloc[i]
        l2=b['Nacionalidad'].replace("['","").replace("']","").replace("', '"," / ")
        if f"{b['id_jugador']}.jpg" in fotos:
            col2.image(f"./Fotos_scoutech/{b['id_jugador']}.jpg", width=100)
        else: 
            col2.image(f"./Fotos_scoutech/default.jpg", width=100)
        col2.markdown(f"**{b['Nombre']}**")
        col2.markdown(f"{b['Born']} - {l2}")
        col2.markdown(f"{b['Altura']} - {b['Pie']} - {b['nombre']}")
        Jugador3 = df[df["Nombre"]==Player3]
        for i in range(len(Jugador3)):    
            c=Jugador3.iloc[i]
        l3=c['Nacionalidad'].replace("['","").replace("']","").replace("', '"," / ")
        if f"{c['id_jugador']}.jpg" in fotos:
            col3.image(f"./Fotos_scoutech/{c['id_jugador']}.jpg", width=100)
        else: 
            col3.image(f"./Fotos_scoutech/default.jpg", width=100)
        col3.markdown(f"**{c['Nombre']}**")
        col3.markdown(f"{c['Born']} - {l3}")
        col3.markdown(f"{c['Altura']} - {c['Pie']} - {c['nombre']}")
        Jugador4 = df[df['Nombre']==Player4]    
        for i in range(len(Jugador4)):    
            d=Jugador4.iloc[i]
        l4=d['Nacionalidad'].replace("['","").replace("']","").replace("', '"," / ")
        if f"{str(d['id_jugador'])}.jpg" in fotos:
            col1.image(f"./Fotos_scoutech/{d['id_jugador']}.jpg", width=100)
        else: 
            col1.image(f"./Fotos_scoutech/default.jpg", width=100)
        col1.markdown(f"**{d['Nombre']}**")
        col1.markdown(f"{d['Born']} - {l4}")
        col1.markdown(f"{d['Altura']} - {d['Pie']} - {d['nombre']}")   
        Jugador5 = df[df["Nombre"]==Player5]
        for i in range(len(Jugador5)):    
            e=Jugador5.iloc[i]
        l5=e['Nacionalidad'].replace("['","").replace("']","").replace("', '"," / ")
        if f"{e['id_jugador']}.jpg" in fotos:
            col2.image(f"./Fotos_scoutech/{e['id_jugador']}.jpg", width=100)
        else: 
            col2.image(f"./Fotos_scoutech/default.jpg", width=100)
        col2.markdown(f"**{e['Nombre']}**")
        col2.markdown(f"{e['Born']} - {l5}")
        col2.markdown(f"{e['Altura']} - {e['Pie']} - {e['nombre']}")
        Jugador6 = df[df["Nombre"]==Player6]
        for i in range(len(Jugador6)):    
            f=Jugador6.iloc[i]
        l6=f['Nacionalidad'].replace("['","").replace("']","").replace("', '"," / ")
        if f"{f['id_jugador']}.jpg" in fotos:
            col3.image(f"./Fotos_scoutech/{f['id_jugador']}.jpg", width=100)
        else: 
            col3.image(f"./Fotos_scoutech/default.jpg", width=100)
        col3.markdown(f"**{f['Nombre']}**")
        col3.markdown(f"{f['Born']} - {l6}")
        col3.markdown(f"{f['Altura']} - {f['Pie']} - {f['nombre']}") 
    # empieza la parte de Estadísticas
    # muestra si la comparación la realizamos contra todos los jugadores o solamente los de su posición    
    st.subheader('Estadísticas', divider='rainbow')
    cluster = st.radio("Comparación respecto a los ...",["***jugadores***", f"***{Position}***"],)
    if cluster=='jugadores':
        basedf = movil
    else: 
        basedf =df
    if Position =='Portero':
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([ "Varias","Defensa", "Pases","Posesión","Disparo","Portero"])
        with tab6:
            for i in Stats_GKtot1.columns.values:
                if i != 'id_jugador':
                    if i=='Minutos':
                        a=f'{i}90'
                        Stats_GKtot1[a] = round(Stats_GKtot1[i]/90,2)
                    else:
                        a=f'{i}90'
                        Stats_GKtot1[a] = round(Stats_GKtot1[i]/(Stats_GKtot1['Minutos']/90),2)
            for i in Stats_GKtot1.columns.values:
                if i in ['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']:
                    Stats_GKtot1[i]=round((Stats_GKtot1[i]-Stats_GKtot1[i].min())/(Stats_GKtot1[i].max()-Stats_GKtot1[i].min())*100)
            if end=="3":
                Jugadores1 = Stats_GKtot1[Stats_GKtot1["id_jugador"]==Jugador1["id_jugador"].iloc[0]]
                Jugadores1['Nombre'] = Player1
                Jugadores1=Jugadores1[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']]
                Jugadores1_trasp=Jugadores1[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']].T
                Jugadores1_trasp['Nombre'] = Player1
                Jugadores1_trasp = Jugadores1_trasp.reset_index()
                Jugadores1_trasp.columns = ['caracteristica','valor','Nombre']
                Jugadores2 = Stats_GKtot1[Stats_GKtot1["id_jugador"]==Jugador2["id_jugador"].iloc[0]]
                Jugadores2['Nombre'] = Player2
                Jugadores2=Jugadores2[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']]
                Jugadores2_trasp=Jugadores2[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']].T
                Jugadores2_trasp['Nombre'] = Player2
                Jugadores2_trasp = Jugadores2_trasp.reset_index()
                Jugadores2_trasp.columns = ['caracteristica','valor','Nombre']
                Jugadores3 = Stats_GKtot1[Stats_GKtot1["id_jugador"]==Jugador3["id_jugador"].iloc[0]]
                Jugadores3['Nombre'] = Player3
                Jugadores3=Jugadores3[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']]
                Jugadores3_trasp=Jugadores3[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']].T
                Jugadores3_trasp['Nombre'] = Player3
                Jugadores3_trasp = Jugadores3_trasp.reset_index()
                Jugadores3_trasp.columns = ['caracteristica','valor','Nombre']
                Jugadores_rad = pd.concat([Jugadores1,Jugadores2,Jugadores3])
                Jugadores = pd.concat([Jugadores1_trasp,Jugadores2_trasp,Jugadores3_trasp])
                Jugadores.reset_index(drop=True)
            else:
                Jugadores1 = Stats_GKtot1[Stats_GKtot1["id_jugador"]==Jugador1["id_jugador"].iloc[0]]
                Jugadores1['Nombre'] = Player1
                Jugadores1=Jugadores1[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']]
                Jugadores1_trasp=Jugadores1[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']].T
                Jugadores1_trasp['Nombre'] = Player1
                Jugadores1_trasp = Jugadores1_trasp.reset_index()
                Jugadores1_trasp.columns = ['caracteristica','valor','Nombre']
                Jugadores2 = Stats_GKtot1[Stats_GKtot1["id_jugador"]==Jugador2["id_jugador"].iloc[0]]
                Jugadores2['Nombre'] = Player2
                Jugadores2=Jugadores2[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']]
                Jugadores2_trasp=Jugadores2[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']].T
                Jugadores2_trasp['Nombre'] = Player2
                Jugadores2_trasp = Jugadores2_trasp.reset_index()
                Jugadores2_trasp.columns = ['caracteristica','valor','Nombre']
                Jugadores3 = Stats_GKtot1[Stats_GKtot1["id_jugador"]==Jugador3["id_jugador"].iloc[0]]
                Jugadores3['Nombre'] = Player3
                Jugadores3=Jugadores3[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']]
                Jugadores3_trasp=Jugadores3[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']].T
                Jugadores3_trasp['Nombre'] = Player3
                Jugadores3_trasp = Jugadores3_trasp.reset_index()
                Jugadores3_trasp.columns = ['caracteristica','valor','Nombre']
                Jugadores4 = Stats_GKtot1[Stats_GKtot1["id_jugador"]==Jugador4["id_jugador"].iloc[0]]
                Jugadores4['Nombre'] = Player4
                Jugadores4=Jugadores4[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']]
                Jugadores4_trasp=Jugadores4[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']].T
                Jugadores4_trasp['Nombre'] = Player4
                Jugadores4_trasp = Jugadores4_trasp.reset_index()
                Jugadores4_trasp.columns = ['caracteristica','valor','Nombre']
                Jugadores5 = Stats_GKtot1[Stats_GKtot1["id_jugador"]==Jugador5["id_jugador"].iloc[0]]
                Jugadores5['Nombre'] = Player5
                Jugadores5=Jugadores5[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']]
                Jugadores5_trasp=Jugadores5[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']].T
                Jugadores5_trasp['Nombre'] = Player5
                Jugadores5_trasp = Jugadores5_trasp.reset_index()
                Jugadores5_trasp.columns = ['caracteristica','valor','Nombre']
                Jugadores6 = Stats_GKtot1[Stats_GKtot1["id_jugador"]==Jugador6["id_jugador"].iloc[0]]
                Jugadores6['Nombre'] = Player6
                Jugadores6=Jugadores6[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']]
                Jugadores6_trasp=Jugadores6[['Disparos_sufridos90','Goles_recibidos90','Salvadas90','Salvadas%90','Goles_EsperadosPSXG90',
                        'Pases_Inicia_completados90','Pases_Inicia_intentados90','Pases_Inicia_completados%90','Pases_intentados_sinSA90',
                        'Tiros_intentados90','Tiros_intentados%90','Distancia_pases90','Saques_arco(SA)90','Tiros_SA%90','Distancia_SA90',
                        'Centros_recibidos90','Centros_parados90','Centros_parados%90','Acciones_fuera_penal90','Distancia_Acciones90']].T
                Jugadores6_trasp['Nombre'] = Player6
                Jugadores6_trasp = Jugadores6_trasp.reset_index()
                Jugadores6_trasp.columns = ['caracteristica','valor','Nombre']
                Jugadores_rad = pd.concat([Jugadores1,Jugadores2,Jugadores3,Jugadores4,Jugadores5,Jugadores6])
                Jugadores = pd.concat([Jugadores1_trasp,Jugadores2_trasp,Jugadores3_trasp,Jugadores4_trasp,Jugadores5_trasp,Jugadores6_trasp])
                Jugadores.reset_index(drop=True)
            st.bar_chart(Jugadores, x="caracteristica", y="valor", color="Nombre", stack=False, x_label='Características')
    else:
        tab1, tab2, tab3, tab4, tab5= st.tabs(["Varias", "Defensa", "Pases","Posesión","Disparo"])
        Jugadores_rad = pd.DataFrame([])
    Stats_Variastot = pd.merge(Stats_Varias,movil,on='id_movil',how='inner')
    Varias = Stats_Variastot.groupby('id_jugador')[['Minutos','Amarillas','Rojas','Seg_Amarillas','Faltas_cometidas','Faltas_recibidas','Offside','Penal_concedido','Goles_contra']].sum().reset_index()
    Stats_Posesióntot = pd.merge(Stats_Posesión,movil,on='id_movil',how='inner')
    Stats_Posesióntot = pd.merge(Stats_Posesióntot,Stats_Varias,on='id_movil',how='inner')
    Stats_Posesióntot1 = Stats_Posesióntot.groupby('id_jugador')[['Minutos','Toques','Toques_area_defensiva','Toques_defensa','Toques_medio','Toques_ataque','Toques_area_ataque','Toques_balon_vivo','Enfrentamientos_intentados','Enfrentamientos_exitosos','Enfrentamientos_exitosos%','Enfrentamientos_tackleados','Enfrentamientos_tackleados%','Carreras','Distancia_traslados','Distancia_progresivas','Carreras_progresivas','Traslados_ultimo_tercio','Traslados_area_penal','Errores_control','Perdidas','Pases_recibidos','Pases_progresivos_recibidos']].sum().reset_index()
    Stats_Defensetot = pd.merge(Stats_Defense,movil,on='id_movil',how='left')
    Stats_Defensetot = pd.merge(Stats_Defensetot,Stats_Varias,on='id_movil',how='inner')
    Stats_Defensetot1 = Stats_Defensetot.groupby('id_jugador')[['Minutos','Tackles','Tackles_conseguidos','Tackles_defensa','Tackles_medio','Tackles_arriba','Regateadores_Tackleados','Regateadores_desafiados','Regateadores_Tackleados%','Desafios_perdidos','Bloqueos','Tiros_bloqueados','Pases_bloqueados','Intercepciones','Despejes','Errores','Recuperaciones','Duelos_aereos_ganados','Duelos_aereos_perdidos','Duelos_aereos_ganados%']].sum().reset_index()
    Stats_Disparotot = pd.merge(Stats_Disparo,movil,on='id_movil',how='left')
    Stats_Disparotot = pd.merge(Stats_Disparotot,Stats_Varias,on='id_movil',how='inner')
    Stats_Disparotot1 = Stats_Disparotot.groupby('id_jugador')[['Minutos','Goles','Tiro_Penal','Tiro_Penal_intentado','Total_Disparo','Disparo_arco','XG','XG_NoPenal','Creacion_tiros','Creacion_goles']].sum().reset_index()
    Stats_GKtot = pd.merge(Stats_GK,movil,on='id_movil',how='left')
    Stats_GKtot = pd.merge(Stats_GKtot,Stats_Varias,on='id_movil',how='inner')
    Stats_GKtot1 = Stats_GKtot.groupby('id_jugador')[['Minutos','Disparos_sufridos','Goles_recibidos','Salvadas','Salvadas%','Goles_EsperadosPSXG','Pases_Inicia_completados','Pases_Inicia_intentados','Pases_Inicia_completados%','Pases_intentados_sinSA','Tiros_intentados','Tiros_intentados%','Distancia_pases','Saques_arco(SA)','Tiros_SA%','Distancia_SA','Centros_recibidos','Centros_parados','Centros_parados%','Acciones_fuera_penal','Distancia_Acciones']].sum().reset_index()
    Stats_Pasestot = pd.merge(Stats_Pases,movil,on='id_movil',how='left')
    Stats_Pasestot = pd.merge(Stats_Pasestot,Stats_Varias,on='id_movil',how='inner')
    Stats_Pasestot1 = Stats_Pasestot.groupby('id_jugador')[['Minutos','Pases_completos','Pases_intentados','Pases_completos%','Distancia_pase','Distancia_Pases_progresivos','Pases_Cortos_completos','Pases_Cortos_intentados','Pases_Cortos_completos%','Pases_Medios_completos','Pases_Medios_intentados','Pases_Medios_completos%','Pases_Largos_completos','Pases_Largos_intentados','Pases_Largos_completos%','Asistencia','XAG','XA','Pases_Claves','Pases_ultimo_tercio','Pases_area_penal','Centro_area_penal','Pases_progresivos','Pases_balon_vivo','Pases_balon_muerto','Pases_tiro_libre','Pases_largo','Cambios_frente','Pases_Centros','Tiros_libre','Tiros_Esquina','Tiros_Esquina_dentro','Tiros_Esquina_fuera','Tiros_Esquina_rectos','Pases_fuera_juego','Pases_bloqueados_opo']].sum().reset_index()
    """
    if cluster=="jugadores":
        None
    else:
        Varias = Stats_Variastot1[Stats_Variastot1['Posicion_agrup']==Position]
    """
    with tab1:
        for i in Varias.columns.values:
            if i != 'id_jugador':
                if i=='Minutos':
                    a=f'{i}90'
                    Varias[a] = round(Varias[i]/90,2)
                else:
                    a=f'{i}90'
                    Varias[a] = round(Varias[i]/(Varias['Minutos']/90),2)
        for i in Varias.columns.values:
            if i in ['Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']:
                Varias[i]=round((Varias[i]-Varias[i].min())/(Varias[i].max()-Varias[i].min())*100)
        if end=="3":
            Jugadores1 = Varias[Varias["id_jugador"]==Jugador1["id_jugador"].iloc[0]]
            Jugadores1['Nombre'] = Player1
            Jugadores1=Jugadores1[['Nombre','Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']]
            Jugadores1_trasp=Jugadores1[['Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']].T
            Jugadores1_trasp['Nombre'] = Player1
            Jugadores1_trasp = Jugadores1_trasp.reset_index()
            Jugadores1_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores2 = Varias[Varias["id_jugador"]==Jugador2["id_jugador"].iloc[0]]
            Jugadores2['Nombre'] = Player2
            Jugadores2=Jugadores2[['Nombre','Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']]
            Jugadores2_trasp=Jugadores2[['Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']].T
            Jugadores2_trasp['Nombre'] = Player2
            Jugadores2_trasp = Jugadores2_trasp.reset_index()
            Jugadores2_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores3 = Varias[Varias["id_jugador"]==Jugador3["id_jugador"].iloc[0]]
            Jugadores3['Nombre'] = Player3
            Jugadores3=Jugadores3[['Nombre','Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']]
            Jugadores3_trasp=Jugadores3[['Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']].T
            Jugadores3_trasp['Nombre'] = Player3
            Jugadores3_trasp = Jugadores3_trasp.reset_index()
            Jugadores3_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores_rad1 = pd.concat([Jugadores1,Jugadores2,Jugadores3])
            Jugadores = pd.concat([Jugadores1_trasp,Jugadores2_trasp,Jugadores3_trasp])
            Jugadores.reset_index(drop=True)
        else:
            Jugadores1 = Varias[Varias["id_jugador"]==Jugador1["id_jugador"].iloc[0]]
            Jugadores1['Nombre'] = Player1
            Jugadores1=Jugadores1[['Nombre','Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']]
            Jugadores1_trasp=Jugadores1[['Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']].T
            Jugadores1_trasp['Nombre'] = Player1
            Jugadores1_trasp = Jugadores1_trasp.reset_index()
            Jugadores1_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores2 = Varias[Varias["id_jugador"]==Jugador2["id_jugador"].iloc[0]]
            Jugadores2['Nombre'] = Player2
            Jugadores2=Jugadores2[['Nombre','Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']]
            Jugadores2_trasp=Jugadores2[['Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']].T
            Jugadores2_trasp['Nombre'] = Player2
            Jugadores2_trasp = Jugadores2_trasp.reset_index()
            Jugadores2_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores3 = Varias[Varias["id_jugador"]==Jugador3["id_jugador"].iloc[0]]
            Jugadores3['Nombre'] = Player3
            Jugadores3=Jugadores3[['Nombre','Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']]
            Jugadores3_trasp=Jugadores3[['Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']].T
            Jugadores3_trasp['Nombre'] = Player3
            Jugadores3_trasp = Jugadores3_trasp.reset_index()
            Jugadores3_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores4 = Varias[Varias["id_jugador"]==Jugador4["id_jugador"].iloc[0]]
            Jugadores4['Nombre'] = Player4
            Jugadores4=Jugadores4[['Nombre','Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']]
            Jugadores4_trasp=Jugadores4[['Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']].T
            Jugadores4_trasp['Nombre'] = Player4
            Jugadores4_trasp = Jugadores4_trasp.reset_index()
            Jugadores4_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores5 = Varias[Varias["id_jugador"]==Jugador5["id_jugador"].iloc[0]]
            Jugadores5['Nombre'] = Player5
            Jugadores5=Jugadores5[['Nombre','Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']]
            Jugadores5_trasp=Jugadores5[['Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']].T
            Jugadores5_trasp['Nombre'] = Player5
            Jugadores5_trasp = Jugadores5_trasp.reset_index()
            Jugadores5_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores6 = Varias[Varias["id_jugador"]==Jugador6["id_jugador"].iloc[0]]
            Jugadores6['Nombre'] = Player6
            Jugadores6=Jugadores6[['Nombre','Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']]
            Jugadores6_trasp=Jugadores6[['Amarillas90','Rojas90','Seg_Amarillas90','Faltas_cometidas90','Faltas_recibidas90','Offside90','Penal_concedido90','Goles_contra90']].T
            Jugadores6_trasp['Nombre'] = Player6
            Jugadores6_trasp = Jugadores6_trasp.reset_index()
            Jugadores6_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores_rad1 = pd.concat([Jugadores1,Jugadores2,Jugadores3,Jugadores4,Jugadores5,Jugadores6])
            Jugadores = pd.concat([Jugadores1_trasp,Jugadores2_trasp,Jugadores3_trasp,Jugadores4_trasp,Jugadores5_trasp,Jugadores6_trasp])
            Jugadores.reset_index(drop=True)
        st.bar_chart(Jugadores, x="caracteristica", y="valor", color="Nombre", stack=False, x_label='Características')
    with tab2:
        for i in Stats_Defensetot1.columns.values:
            if i != 'id_jugador':
                if i=='Minutos':
                    a=f'{i}90'
                    Stats_Defensetot1[a] = round(Stats_Defensetot1[i]/90,2)
                else:
                    a=f'{i}90'
                    Stats_Defensetot1[a] = round(Stats_Defensetot1[i]/(Stats_Defensetot1['Minutos']/90),2)
        for i in Stats_Defensetot1.columns.values:
            if i in ['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']:
                Stats_Defensetot1[i]=round((Stats_Defensetot1[i]-Stats_Defensetot1[i].min())/(Stats_Defensetot1[i].max()-Stats_Defensetot1[i].min())*100)
        if end=="3":
            Jugadores1 = Stats_Defensetot1[Stats_Defensetot1["id_jugador"]==Jugador1["id_jugador"].iloc[0]]
            Jugadores1['Nombre'] = Player1
            Jugadores1=Jugadores1[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']]
            Jugadores1_trasp=Jugadores1[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']].T
            Jugadores1_trasp['Nombre'] = Player1
            Jugadores1_trasp = Jugadores1_trasp.reset_index()
            Jugadores1_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores2 = Stats_Defensetot1[Stats_Defensetot1["id_jugador"]==Jugador2["id_jugador"].iloc[0]]
            Jugadores2['Nombre'] = Player2
            Jugadores2=Jugadores2[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']]
            Jugadores2_trasp=Jugadores2[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']].T
            Jugadores2_trasp['Nombre'] = Player2
            Jugadores2_trasp = Jugadores2_trasp.reset_index()
            Jugadores2_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores3 = Stats_Defensetot1[Stats_Defensetot1["id_jugador"]==Jugador3["id_jugador"].iloc[0]]
            Jugadores3['Nombre'] = Player3
            Jugadores3=Jugadores3[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']]
            Jugadores3_trasp=Jugadores3[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']].T
            Jugadores3_trasp['Nombre'] = Player3
            Jugadores3_trasp = Jugadores3_trasp.reset_index()
            Jugadores3_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores_rad2 = pd.concat([Jugadores1,Jugadores2,Jugadores3])
            Jugadores = pd.concat([Jugadores1_trasp,Jugadores2_trasp,Jugadores3_trasp])
            Jugadores.reset_index(drop=True)
        else:
            Jugadores1 = Stats_Defensetot1[Stats_Defensetot1["id_jugador"]==Jugador1["id_jugador"].iloc[0]]
            Jugadores1['Nombre'] = Player1
            Jugadores1=Jugadores1[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']]
            Jugadores1_trasp=Jugadores1[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']].T
            Jugadores1_trasp['Nombre'] = Player1
            Jugadores1_trasp = Jugadores1_trasp.reset_index()
            Jugadores1_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores2 = Stats_Defensetot1[Stats_Defensetot1["id_jugador"]==Jugador2["id_jugador"].iloc[0]]
            Jugadores2['Nombre'] = Player2
            Jugadores2=Jugadores2[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']]
            Jugadores2_trasp=Jugadores2[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']].T
            Jugadores2_trasp['Nombre'] = Player2
            Jugadores2_trasp = Jugadores2_trasp.reset_index()
            Jugadores2_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores3 = Stats_Defensetot1[Stats_Defensetot1["id_jugador"]==Jugador3["id_jugador"].iloc[0]]
            Jugadores3['Nombre'] = Player3
            Jugadores3=Jugadores3[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']]
            Jugadores3_trasp=Jugadores3[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']].T
            Jugadores3_trasp['Nombre'] = Player3
            Jugadores3_trasp = Jugadores3_trasp.reset_index()
            Jugadores3_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores4 = Stats_Defensetot1[Stats_Defensetot1["id_jugador"]==Jugador4["id_jugador"].iloc[0]]
            Jugadores4['Nombre'] = Player4
            Jugadores4=Jugadores4[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']]
            Jugadores4_trasp=Jugadores4[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']].T
            Jugadores4_trasp['Nombre'] = Player4
            Jugadores4_trasp = Jugadores4_trasp.reset_index()
            Jugadores4_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores5 = Stats_Defensetot1[Stats_Defensetot1["id_jugador"]==Jugador5["id_jugador"].iloc[0]]
            Jugadores5['Nombre'] = Player5
            Jugadores5=Jugadores5[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']]
            Jugadores5_trasp=Jugadores5[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']].T
            Jugadores5_trasp['Nombre'] = Player5
            Jugadores5_trasp = Jugadores5_trasp.reset_index()
            Jugadores5_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores6 = Stats_Defensetot1[Stats_Defensetot1["id_jugador"]==Jugador6["id_jugador"].iloc[0]]
            Jugadores6['Nombre'] = Player6
            Jugadores6=Jugadores6[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']]
            Jugadores6_trasp=Jugadores6[['Tackles90','Tackles_conseguidos90','Tackles_defensa90','Tackles_medio90',
                     'Tackles_arriba90','Regateadores_Tackleados90','Regateadores_desafiados90',
                     'Regateadores_Tackleados%90','Desafios_perdidos90','Bloqueos90','Tiros_bloqueados90',
                     'Pases_bloqueados90','Intercepciones90','Despejes90','Errores90','Recuperaciones90',
                     'Duelos_aereos_ganados90','Duelos_aereos_perdidos90','Duelos_aereos_ganados%90']].T
            Jugadores6_trasp['Nombre'] = Player6
            Jugadores6_trasp = Jugadores6_trasp.reset_index()
            Jugadores6_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores_rad2 = pd.concat([Jugadores1,Jugadores2,Jugadores3,Jugadores4,Jugadores5,Jugadores6])
            Jugadores = pd.concat([Jugadores1_trasp,Jugadores2_trasp,Jugadores3_trasp,Jugadores4_trasp,Jugadores5_trasp,Jugadores6_trasp])
            Jugadores.reset_index(drop=True)
        st.bar_chart(Jugadores, x="caracteristica", y="valor", color="Nombre", stack=False, x_label='Características')
    with tab3:
        for i in Stats_Pasestot1.columns.values:
            if i != 'id_jugador':
                if i=='Minutos':
                    a=f'{i}90'
                    Stats_Pasestot1[a] = round(Stats_Pasestot1[i]/90,2)
                else:
                    a=f'{i}90'
                    Stats_Pasestot1[a] = round(Stats_Pasestot1[i]/(Stats_Pasestot1['Minutos']/90),2)
        for i in Stats_Pasestot1.columns.values:
            if i in ['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']:
                Stats_Pasestot1[i]=round((Stats_Pasestot1[i]-Stats_Pasestot1[i].min())/(Stats_Pasestot1[i].max()-Stats_Pasestot1[i].min())*100)
        if end=="3":
            Jugadores1 = Stats_Pasestot1[Stats_Pasestot1["id_jugador"]==Jugador1["id_jugador"].iloc[0]]
            Jugadores1['Nombre'] = Player1
            Jugadores1=Jugadores1[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']]
            Jugadores1_trasp=Jugadores1[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']].T
            Jugadores1_trasp['Nombre'] = Player1
            Jugadores1_trasp = Jugadores1_trasp.reset_index()
            Jugadores1_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores2 = Stats_Pasestot1[Stats_Pasestot1["id_jugador"]==Jugador2["id_jugador"].iloc[0]]
            Jugadores2['Nombre'] = Player2
            Jugadores2=Jugadores2[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']]
            Jugadores2_trasp=Jugadores2[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']].T
            Jugadores2_trasp['Nombre'] = Player2
            Jugadores2_trasp = Jugadores2_trasp.reset_index()
            Jugadores2_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores3 = Stats_Pasestot1[Stats_Pasestot1["id_jugador"]==Jugador3["id_jugador"].iloc[0]]
            Jugadores3['Nombre'] = Player3
            Jugadores3=Jugadores3[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']]
            Jugadores3_trasp=Jugadores3[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']].T
            Jugadores3_trasp['Nombre'] = Player3
            Jugadores3_trasp = Jugadores3_trasp.reset_index()
            Jugadores3_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores_rad3 = pd.concat([Jugadores1,Jugadores2,Jugadores3])
            Jugadores = pd.concat([Jugadores1_trasp,Jugadores2_trasp,Jugadores3_trasp])
            Jugadores.reset_index(drop=True)
        else:
            Jugadores1 = Stats_Pasestot1[Stats_Pasestot1["id_jugador"]==Jugador1["id_jugador"].iloc[0]]
            Jugadores1['Nombre'] = Player1
            Jugadores1=Jugadores1[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']]
            Jugadores1_trasp=Jugadores1[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']].T
            Jugadores1_trasp['Nombre'] = Player1
            Jugadores1_trasp = Jugadores1_trasp.reset_index()
            Jugadores1_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores2 = Stats_Pasestot1[Stats_Pasestot1["id_jugador"]==Jugador2["id_jugador"].iloc[0]]
            Jugadores2['Nombre'] = Player2
            Jugadores2=Jugadores2[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']]
            Jugadores2_trasp=Jugadores2[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']].T
            Jugadores2_trasp['Nombre'] = Player2
            Jugadores2_trasp = Jugadores2_trasp.reset_index()
            Jugadores2_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores3 = Stats_Pasestot1[Stats_Pasestot1["id_jugador"]==Jugador3["id_jugador"].iloc[0]]
            Jugadores3['Nombre'] = Player3
            Jugadores3=Jugadores3[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']]
            Jugadores3_trasp=Jugadores3[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']].T
            Jugadores3_trasp['Nombre'] = Player3
            Jugadores3_trasp = Jugadores3_trasp.reset_index()
            Jugadores3_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores4 = Stats_Pasestot1[Stats_Pasestot1["id_jugador"]==Jugador4["id_jugador"].iloc[0]]
            Jugadores4['Nombre'] = Player4
            Jugadores4=Jugadores4[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']]
            Jugadores4_trasp=Jugadores4[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']].T
            Jugadores4_trasp['Nombre'] = Player4
            Jugadores4_trasp = Jugadores4_trasp.reset_index()
            Jugadores4_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores5 = Stats_Pasestot1[Stats_Pasestot1["id_jugador"]==Jugador5["id_jugador"].iloc[0]]
            Jugadores5['Nombre'] = Player5
            Jugadores5=Jugadores5[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']]
            Jugadores5_trasp=Jugadores5[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']].T
            Jugadores5_trasp['Nombre'] = Player5
            Jugadores5_trasp = Jugadores5_trasp.reset_index()
            Jugadores5_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores6 = Stats_Pasestot1[Stats_Pasestot1["id_jugador"]==Jugador6["id_jugador"].iloc[0]]
            Jugadores6['Nombre'] = Player6
            Jugadores6=Jugadores6[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']]
            Jugadores6_trasp=Jugadores6[['Pases_completos90','Pases_intentados90','Pases_completos%90','Distancia_pase90',
                     'Distancia_Pases_progresivos90','Pases_Cortos_completos90','Pases_Cortos_intentados90',
                     'Pases_Cortos_completos%90','Pases_Medios_completos90','Pases_Medios_intentados90',
                     'Pases_Medios_completos%90','Pases_Largos_completos90','Pases_Largos_intentados90',
                     'Pases_Largos_completos%90','Asistencia90','XAG90','XA90','Pases_Claves90','Pases_ultimo_tercio90',
                     'Pases_area_penal90','Centro_area_penal90','Pases_progresivos90','Pases_balon_vivo90','Pases_balon_muerto90',
                     'Pases_tiro_libre90','Pases_largo90','Cambios_frente90','Pases_Centros90','Tiros_libre90','Tiros_Esquina90',
                     'Tiros_Esquina_dentro90','Tiros_Esquina_fuera90','Tiros_Esquina_rectos90','Pases_fuera_juego90','Pases_bloqueados_opo90']].T
            Jugadores6_trasp['Nombre'] = Player6
            Jugadores6_trasp = Jugadores6_trasp.reset_index()
            Jugadores6_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores_rad3 = pd.concat([Jugadores1,Jugadores2,Jugadores3,Jugadores4,Jugadores5,Jugadores6])
            Jugadores = pd.concat([Jugadores1_trasp,Jugadores2_trasp,Jugadores3_trasp,Jugadores4_trasp,Jugadores5_trasp,Jugadores6_trasp])
            Jugadores.reset_index(drop=True)
        st.bar_chart(Jugadores, x="caracteristica", y="valor", color="Nombre", stack=False, x_label='Características')
    with tab4:
        for i in Stats_Posesióntot1.columns.values:
            if i != 'id_jugador':
                if i=='Minutos':
                    a=f'{i}90'
                    Stats_Posesióntot1[a] = round(Stats_Posesióntot1[i]/90,2)
                else:
                    a=f'{i}90'
                    Stats_Posesióntot1[a] = round(Stats_Posesióntot1[i]/(Stats_Posesióntot1['Minutos']/90),2)
        for i in Stats_Posesióntot1.columns.values:
            if i in ['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']:
                Stats_Posesióntot1[i]=round((Stats_Posesióntot1[i]-Stats_Posesióntot1[i].min())/(Stats_Posesióntot1[i].max()-Stats_Posesióntot1[i].min())*100)
        if end=="3":
            Jugadores1 = Stats_Posesióntot1[Stats_Posesióntot1["id_jugador"]==Jugador1["id_jugador"].iloc[0]]
            Jugadores1['Nombre'] = Player1
            Jugadores1=Jugadores1[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']]
            Jugadores1_trasp=Jugadores1[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']].T
            Jugadores1_trasp['Nombre'] = Player1
            Jugadores1_trasp = Jugadores1_trasp.reset_index()
            Jugadores1_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores2 = Stats_Posesióntot1[Stats_Posesióntot1["id_jugador"]==Jugador2["id_jugador"].iloc[0]]
            Jugadores2['Nombre'] = Player2
            Jugadores2=Jugadores2[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']]
            Jugadores2_trasp=Jugadores2[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']].T
            Jugadores2_trasp['Nombre'] = Player2
            Jugadores2_trasp = Jugadores2_trasp.reset_index()
            Jugadores2_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores3 = Stats_Posesióntot1[Stats_Posesióntot1["id_jugador"]==Jugador3["id_jugador"].iloc[0]]
            Jugadores3['Nombre'] = Player3
            Jugadores3=Jugadores3[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']]
            Jugadores3_trasp=Jugadores3[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']].T
            Jugadores3_trasp['Nombre'] = Player3
            Jugadores3_trasp = Jugadores3_trasp.reset_index()
            Jugadores3_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores_rad4 = pd.concat([Jugadores1,Jugadores2,Jugadores3])
            Jugadores = pd.concat([Jugadores1_trasp,Jugadores2_trasp,Jugadores3_trasp])
            Jugadores.reset_index(drop=True)
        else:
            Jugadores1 = Stats_Posesióntot1[Stats_Posesióntot1["id_jugador"]==Jugador1["id_jugador"].iloc[0]]
            Jugadores1['Nombre'] = Player1
            Jugadores1=Jugadores1[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']]
            Jugadores1_trasp=Jugadores1[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']].T
            Jugadores1_trasp['Nombre'] = Player1
            Jugadores1_trasp = Jugadores1_trasp.reset_index()
            Jugadores1_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores2 = Stats_Posesióntot1[Stats_Posesióntot1["id_jugador"]==Jugador2["id_jugador"].iloc[0]]
            Jugadores2['Nombre'] = Player2
            Jugadores2=Jugadores2[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']]
            Jugadores2_trasp=Jugadores2[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']].T
            Jugadores2_trasp['Nombre'] = Player2
            Jugadores2_trasp = Jugadores2_trasp.reset_index()
            Jugadores2_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores3 = Stats_Posesióntot1[Stats_Posesióntot1["id_jugador"]==Jugador3["id_jugador"].iloc[0]]
            Jugadores3['Nombre'] = Player3
            Jugadores3=Jugadores3[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']]
            Jugadores3_trasp=Jugadores3[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']].T
            Jugadores3_trasp['Nombre'] = Player3
            Jugadores3_trasp = Jugadores3_trasp.reset_index()
            Jugadores3_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores4 = Stats_Posesióntot1[Stats_Posesióntot1["id_jugador"]==Jugador4["id_jugador"].iloc[0]]
            Jugadores4['Nombre'] = Player4
            Jugadores4=Jugadores4[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']]
            Jugadores4_trasp=Jugadores4[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']].T
            Jugadores4_trasp['Nombre'] = Player4
            Jugadores4_trasp = Jugadores4_trasp.reset_index()
            Jugadores4_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores5 = Stats_Posesióntot1[Stats_Posesióntot1["id_jugador"]==Jugador5["id_jugador"].iloc[0]]
            Jugadores5['Nombre'] = Player5
            Jugadores5=Jugadores5[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']]
            Jugadores5_trasp=Jugadores5[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']].T
            Jugadores5_trasp['Nombre'] = Player5
            Jugadores5_trasp = Jugadores5_trasp.reset_index()
            Jugadores5_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores6 = Stats_Posesióntot1[Stats_Posesióntot1["id_jugador"]==Jugador6["id_jugador"].iloc[0]]
            Jugadores6['Nombre'] = Player6
            Jugadores6=Jugadores6[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']]
            Jugadores6_trasp=Jugadores6[['Toques90','Toques_area_defensiva90','Toques_defensa90','Toques_medio90','Toques_ataque90',
                     'Toques_area_ataque90','Toques_balon_vivo90','Enfrentamientos_intentados90','Enfrentamientos_exitosos90',
                     'Enfrentamientos_exitosos%90','Enfrentamientos_tackleados90','Enfrentamientos_tackleados%90','Carreras90',
                     'Distancia_traslados90','Distancia_progresivas90','Carreras_progresivas90','Traslados_ultimo_tercio90',
                     'Traslados_area_penal90','Errores_control90','Perdidas90','Pases_recibidos90','Pases_progresivos_recibidos90']].T
            Jugadores6_trasp['Nombre'] = Player6
            Jugadores6_trasp = Jugadores6_trasp.reset_index()
            Jugadores6_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores_rad4 = pd.concat([Jugadores1,Jugadores2,Jugadores3,Jugadores4,Jugadores5,Jugadores6])
            Jugadores = pd.concat([Jugadores1_trasp,Jugadores2_trasp,Jugadores3_trasp,Jugadores4_trasp,Jugadores5_trasp,Jugadores6_trasp])
            Jugadores.reset_index(drop=True)
        st.bar_chart(Jugadores, x="caracteristica", y="valor", color="Nombre", stack=False, x_label='Características')
    with tab5:
        for i in Stats_Disparotot1.columns.values:
            if i != 'id_jugador':
                if i=='Minutos':
                    a=f'{i}90'
                    Stats_Disparotot1[a] = round(Stats_Disparotot1[i]/90,2)
                else:
                    a=f'{i}90'
                    Stats_Disparotot1[a] = round(Stats_Disparotot1[i]/(Stats_Disparotot1['Minutos']/90),2)
        for i in Stats_Disparotot1.columns.values:
            if i in ['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']:
                Stats_Disparotot1[i]=round((Stats_Disparotot1[i]-Stats_Disparotot1[i].min())/(Stats_Disparotot1[i].max()-Stats_Disparotot1[i].min())*100)
        if end=="3":
            Jugadores1 = Stats_Disparotot1[Stats_Disparotot1["id_jugador"]==Jugador1["id_jugador"].iloc[0]]
            Jugadores1['Nombre'] = Player1
            Jugadores1=Jugadores1[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']]
            Jugadores1_trasp=Jugadores1[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']].T
            Jugadores1_trasp['Nombre'] = Player1
            Jugadores1_trasp = Jugadores1_trasp.reset_index()
            Jugadores1_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores2 = Stats_Disparotot1[Stats_Disparotot1["id_jugador"]==Jugador2["id_jugador"].iloc[0]]
            Jugadores2['Nombre'] = Player2
            Jugadores2=Jugadores2[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']]
            Jugadores2_trasp=Jugadores2[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']].T
            Jugadores2_trasp['Nombre'] = Player2
            Jugadores2_trasp = Jugadores2_trasp.reset_index()
            Jugadores2_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores3 = Stats_Disparotot1[Stats_Disparotot1["id_jugador"]==Jugador3["id_jugador"].iloc[0]]
            Jugadores3['Nombre'] = Player3
            Jugadores3=Jugadores3[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']]
            Jugadores3_trasp=Jugadores3[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']].T
            Jugadores3_trasp['Nombre'] = Player3
            Jugadores3_trasp = Jugadores3_trasp.reset_index()
            Jugadores3_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores_rad5 = pd.concat([Jugadores1,Jugadores2,Jugadores3])
            Jugadores = pd.concat([Jugadores1_trasp,Jugadores2_trasp,Jugadores3_trasp])
            Jugadores.reset_index(drop=True)
        else:
            Jugadores1 = Stats_Disparotot1[Stats_Disparotot1["id_jugador"]==Jugador1["id_jugador"].iloc[0]]
            Jugadores1['Nombre'] = Player1
            Jugadores1=Jugadores1[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']]
            Jugadores1_trasp=Jugadores1[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']].T
            Jugadores1_trasp['Nombre'] = Player1
            Jugadores1_trasp = Jugadores1_trasp.reset_index()
            Jugadores1_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores2 = Stats_Disparotot1[Stats_Disparotot1["id_jugador"]==Jugador2["id_jugador"].iloc[0]]
            Jugadores2['Nombre'] = Player2
            Jugadores2=Jugadores2[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']]
            Jugadores2_trasp=Jugadores2[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']].T
            Jugadores2_trasp['Nombre'] = Player2
            Jugadores2_trasp = Jugadores2_trasp.reset_index()
            Jugadores2_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores3 = Stats_Disparotot1[Stats_Disparotot1["id_jugador"]==Jugador3["id_jugador"].iloc[0]]
            Jugadores3['Nombre'] = Player3
            Jugadores3=Jugadores3[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']]
            Jugadores3_trasp=Jugadores3[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']].T
            Jugadores3_trasp['Nombre'] = Player3
            Jugadores3_trasp = Jugadores3_trasp.reset_index()
            Jugadores3_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores4 = Stats_Disparotot1[Stats_Disparotot1["id_jugador"]==Jugador4["id_jugador"].iloc[0]]
            Jugadores4['Nombre'] = Player4
            Jugadores4=Jugadores4[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']]
            Jugadores4_trasp=Jugadores4[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']].T
            Jugadores4_trasp['Nombre'] = Player4
            Jugadores4_trasp = Jugadores4_trasp.reset_index()
            Jugadores4_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores5 = Stats_Disparotot1[Stats_Disparotot1["id_jugador"]==Jugador5["id_jugador"].iloc[0]]
            Jugadores5['Nombre'] = Player5
            Jugadores5=Jugadores5[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']]
            Jugadores5_trasp=Jugadores5[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']].T
            Jugadores5_trasp['Nombre'] = Player5
            Jugadores5_trasp = Jugadores5_trasp.reset_index()
            Jugadores5_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores6 = Stats_Disparotot1[Stats_Disparotot1["id_jugador"]==Jugador6["id_jugador"].iloc[0]]
            Jugadores6['Nombre'] = Player6
            Jugadores6=Jugadores6[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']]
            Jugadores6_trasp=Jugadores6[['Goles90','Tiro_Penal90','Tiro_Penal_intentado90','Total_Disparo90','Disparo_arco90',
                     'XG90','XG_NoPenal90','Creacion_tiros90','Creacion_goles90']].T
            Jugadores6_trasp['Nombre'] = Player6
            Jugadores6_trasp = Jugadores6_trasp.reset_index()
            Jugadores6_trasp.columns = ['caracteristica','valor','Nombre']
            Jugadores_rad5 = pd.concat([Jugadores1,Jugadores2,Jugadores3,Jugadores4,Jugadores5,Jugadores6])
            Jugadores = pd.concat([Jugadores1_trasp,Jugadores2_trasp,Jugadores3_trasp,Jugadores4_trasp,Jugadores5_trasp,Jugadores6_trasp])
            Jugadores.reset_index(drop=True)
        st.bar_chart(Jugadores, x="caracteristica", y="valor", color="Nombre", stack=False, x_label='Características')
    Jugadores_rad = pd.concat([Jugadores_rad1,Jugadores_rad,Jugadores_rad2,Jugadores_rad3,Jugadores_rad4,Jugadores_rad5], axis=1)
    options = st.multiselect("What are your favorite colors",Jugadores_rad.drop(columns = ["Nombre"]).columns,['Toques90','Disparo_arco90','Pases_completos90','Tackles90']) 
    if len(Jugadores_rad) ==3:
        Jugador1=Jugadores_rad[options].iloc[0].to_numpy().tolist()
        Jugador2=Jugadores_rad[options].iloc[1].to_numpy().tolist()
        Jugador3=Jugadores_rad[options].iloc[2].to_numpy().tolist()
        maximo=max([max(Jugador1),max(Jugador2),max(Jugador3)])
        categories = options
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=Jugador1,
            theta=categories,
            fill='toself',
            fillcolor='red',
            opacity=0.5,
            line_color='red',
            name=Player1
        ))
        fig.add_trace(go.Scatterpolar(
            r=Jugador2,
            theta=categories,
            fill='toself',
            fillcolor='blue',
            opacity=0.5,
            line_color='blue',
            name=Player2
        ))
        fig.add_trace(go.Scatterpolar(
            r=Jugador3,
            theta=categories,
            fill='toself',
            fillcolor='red',
            opacity=0.5,
            line_color='red',
            name=Player3
        ))
        fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, maximo]
            )),
        showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        Jugador1=Jugadores_rad[options].iloc[0].to_numpy().tolist()
        Jugador2=Jugadores_rad[options].iloc[1].to_numpy().tolist()
        Jugador3=Jugadores_rad[options].iloc[2].to_numpy().tolist()
        Jugador4=Jugadores_rad[options].iloc[3].to_numpy().tolist()
        Jugador5=Jugadores_rad[options].iloc[4].to_numpy().tolist()
        Jugador6=Jugadores_rad[options].iloc[5].to_numpy().tolist()
        categories = options
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=Jugador1,
            theta=categories,
            fill='toself',
            fillcolor='red',
            opacity=0.5,
            line_color='red',
            name=Player1
        ))
        fig.add_trace(go.Scatterpolar(
            r=Jugador2,
            theta=categories,
            fill='toself',
            fillcolor='blue',
            opacity=0.5,
            line_color='blue',
            name=Player2
        ))
        fig.add_trace(go.Scatterpolar(
            r=Jugador3,
            theta=categories,
            fill='toself',
            fillcolor='blue',
            opacity=0.5,
            line_color='blue',
            name=Player3
        ))
        fig.add_trace(go.Scatterpolar(
            r=Jugador4,
            theta=categories,
            fill='toself',
            fillcolor='blue',
            opacity=0.5,
            line_color='blue',
            name=Player4
        ))
        fig.add_trace(go.Scatterpolar(
            r=Jugador5,
            theta=categories,
            fill='toself',
            fillcolor='blue',
            opacity=0.5,
            line_color='blue',
            name=Player5
        ))
        fig.add_trace(go.Scatterpolar(
            r=Jugador6,
            theta=categories,
            fill='toself',
            fillcolor='blue',
            opacity=0.5,
            line_color='blue',
            name=Player6
        ))
        fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 100]
            )),
        showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)