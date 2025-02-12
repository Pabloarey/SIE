import streamlit as st
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn_extra.cluster import KMedoids
import pandas as pd
import plotly.graph_objects as go


df = pd.read_excel('Mediocampistas.xlsx', header=0, sheet_name="Sheet1")
df= df.drop(columns = ["Nation","Pos","Squad","Age","Born"], axis=1)
df = df.set_index('Player')
#if upload_file is not None:
#    df = pd.read_excel(upload_file, header=0, sheet_name="ACP Defensa")

def show_Segmentacion():
    st.header("Definiciones")
    col1, col2 = st.columns(2)
    k_clus = col1.selectbox('Select the X-axis', options=[2,3,4,5,6,7,8] )
    scaler = StandardScaler().fit(df)
    x_scaled = scaler.transform(df)
    kMedoids = KMedoids(n_clusters = k_clus, random_state = 0)
    kMedoids.fit(x_scaled)
    y_kmed = kMedoids.fit_predict(x_scaled)
    x_scaled=pd.DataFrame(x_scaled,columns=df.columns)
    y_kmed = pd.DataFrame(y_kmed, columns = ['Cluster'])
    df_new = pd.concat([x_scaled, y_kmed], axis=1,)
    table = pd.pivot_table(df_new, values=df.columns, index=['Cluster'],
                       aggfunc= "mean")
    table=pd.DataFrame(table).rank()
    table = (table.reset_index().T)*-1
    table =table.reset_index().drop(0)
    fig = go.Figure()
    for j in range(k_clus):
        fig.add_trace(go.Scatter(
        name=f"cluster {j}",
        mode="markers+lines", x=table['index'], y=table[j],
        xperiodalignment="middle"
        ))
    fig.update_xaxes(showgrid=True)
    st.plotly_chart(fig, use_container_width=True)
    players = col1.selectbox('Select cluster', options=range(k_clus))
    df_players=df_new[df_new['Cluster']==players]
    col1, col2 = st.columns(2)
    col1.metric(label="Jugadores", value=len(df_players), delta="0 %")
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
    st.header(f'Jugadores que pertenecen al grupo {players}')
    st.write(df_players)

    
