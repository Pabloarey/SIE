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

df = pd.read_excel('Mediocampistas.xlsx', header=0, sheet_name="Sheet1")
df=df.drop(columns = ["Nation","Pos","Squad","Age","Born"], axis=1)
df = df.set_index('Player')

def show_cluster():
    st.header("Definiciones")
    X, _ = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False)
    X = df    
    diss = euclidean_distances(X)
    kmin = 2
    kmax = 10
    dm = kmedoids.dynmsc(diss, kmax, kmin)
    st.write(f"""Optimal number of clusters according to the Medoid Silhouette: {dm.bestk}""")
    fig = ff.create_dendrogram(X)
    fig.update_layout(width=800, height=500)
    st.plotly_chart(fig, use_container_width=True)
    
