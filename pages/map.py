import streamlit as st
import pandas as pd
import plotly.express as px
import os
import geopandas as gpd
import pandas as pd
import folium
import webbrowser
from folium.plugins import MiniMap, HeatMap
import numpy as np
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium
from branca.element import Template, MacroElement

# Create the legend template as an HTML element
legend_template = """
{% macro html(this, kwargs) %}
<div id='maplegend' class='maplegend' 
    style='position: fixed; bottom: 50px; left: 50px; width: 200px; height: 150px; z-index: 9999; background-color: rgba(255, 255, 255, 0.5);
     border-radius: 6px; padding: 10px; font-size: 10.5px; right: 20px; top: 20px;'>     
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background: purple; opacity: 0.75;'></span>ABC</li>
    <li><span style='background: green; opacity: 0.75;'></span>Nivel C1</li>
    <li><span style='background: #DAF7A6; opacity: 0.75;'></span>Nivel C2</li>
    <li><span style='background: yellow; opacity: 0.75;'></span>Nivel C3</li>
    <li><span style='background: orange; opacity: 0.75;'></span>Nivel D</li>   
    <li><span style='background: red; opacity: 0.75;'></span>Rural</li>
  </ul>
</div>
</div> 
<style type='text/css'>
  .maplegend .legend-scale ul {margin: 0; padding: 0; color: #0f0f0f;}
  .maplegend .legend-scale ul li {list-style: none; line-height: 18px; margin-bottom: 1.5px;}
  .maplegend ul.legend-labels li span {float: left; height: 16px; width: 16px; margin-right: 4.5px;}
</style>
{% endmacro %}
"""


df = pd.read_excel('./data/Resultados 21.xlsx', header=0)
contenido = os.listdir('./mapas/')
shapes=[]
geojsons=[]
for j in contenido:
    if j.endswith('.shp'):
        shapes.append(j)
    elif j.endswith('.geojson'):
        geojsons.append(j)
urlESCUELAS = './mapas/ESCUELAS_SFVC2.shp'
# paso a string variable circuito y le agrego 0 por delante para contener 5 dígitos
b=[]
for i, row in df.iterrows():
    if row["IdCircuito"] < 10:
        a= '0000' + str(row["IdCircuito"])
    elif row["IdCircuito"] < 100:
        a= '000' + str(row["IdCircuito"])
    elif row["IdCircuito"] < 1000:
        a= '00' + str(row["IdCircuito"])
    elif row["IdCircuito"] < 10000:
        a= '0' + str(row["IdCircuito"])
    else:
        a= str(row["IdCircuito"])
    b.append(a)
b=pd.DataFrame(b,columns=['circuito'])
df = pd.concat([df,b], axis=1)

df_x = df[df['idAgrupacionInt']>0].groupby(['circuito']).agg(total_votos=('votos', 'sum')).reset_index() 
df_x1 = df[df['idAgrupacionInt']>0].groupby(['circuito','Agrupacion']).agg(total_votos=('votos', 'sum')).reset_index() 
df_finalf = df_x1.merge(df_x, left_on="circuito", right_on="circuito", how="left")
df_finalf['Porcentaje'] = round(df_finalf['total_votos_x']/df_finalf['total_votos_y']*100,2)
gdf = gpd.read_file('./mapas/Catamarca.geojson')
df_final = df_x.merge(gdf, left_on="circuito", right_on="circuito", how="left")
df_final1 = gdf.merge(df_x, left_on="circuito", right_on="circuito", how="right")
df_final2 = gdf.merge(df_x1, left_on="circuito", right_on="circuito", how="right")

# TENGO QIE HACER MERGE entre ambas bases
#https://folium.streamlit.app/simple_popup
def display_map(df):
    # ubicar el punto centro del mapa
    mapa = gpd.read_file('./mapas/Radios.geojson')
    col1, col2 = st.columns(2)
    #Calculo los valores únicos de una columna
    dfnew = df[df['tipoVoto']=='positivo']
    opc_ele=dfnew["Eleccion"].unique().tolist()
    Opc_Eleccion = col1.selectbox('Elección', options= opc_ele, index=len(opc_ele)-1, placeholder="Elija la elección...")
    if Opc_Eleccion==None:
        dfnew = dfnew
    else:    
        dfnew = dfnew[dfnew['Eleccion']==Opc_Eleccion]
    opc_agrup=dfnew["Agrupacion"].unique().tolist()
    Opc_Agrupación = col2.selectbox('Agrupación', options= opc_agrup, index=0, placeholder="Elija el Circuito Electoral...")
    df_x2=df_finalf[df_finalf["Agrupacion"]==Opc_Agrupación]
    df_final3 = df_final2.merge(df_x2, left_on=["circuito",'Agrupacion'], right_on=["circuito",'Agrupacion'], how="right")
    map = mapa.explore(column="clus",  # make choropleth based on "BoroName" column
                    tooltip="clus",  # show "BoroName" value in tooltip (on hover)
                    popup=['link','clus', 'FdT','JxC', 'Otros'],  # show all values in popup (on click)
                    tiles="OpenStreetMap",  # use "CartoDB positron" tiles
                    cmap="Spectral_r",  # use "Set1" matplotlib colormap
                    style_kwds=dict(color="black",weight=2, opacity=0.4,fillOpacity=0.5),
                    name="Nivel socioeconómico")

    # Add the legend to the map
    macro = MacroElement()
    macro._template = Template(legend_template)
    map.get_root().add_child(macro)
    
    SALUD=gpd.read_file('./mapas/CENTROS_SALUD_CAPTAL2.shp')
    polig=folium.GeoJson(SALUD,name="Centros de Salud",show=False,marker = folium.Marker(icon=folium.Icon(icon="glyphicon-header")),tooltip=folium.GeoJsonTooltip(fields=['nam','niv_comple'],
                                                                                                                                                aliases=["Nombre Centro de Salud: ",
                                                                                                                                                         "Nivel complejidad: "], 
                                                                                                                                                localize=True,
                                                                                                                                                sticky=False,
                                                                                                                                                labels=True,
                                                                                                                                                style="""
                                                                                                                                                    background-color: #F0EFEF;
                                                                                                                                                    border: 2px solid black;
                                                                                                                                                    border-radius: 3px;
                                                                                                                                                    box-shadow: 3px;
                                                                                                                                                    """,
                                                                                                                                                max_width=800,),
                                                                                                                                                style_function=lambda x: {'markerColor': 'blue' if x['properties']['nam']=='AAA' else 'green',},)
    map.add_child(polig)
    
    Escuelas=gpd.read_file(urlESCUELAS)
    polig=folium.GeoJson(Escuelas,name="Establecimientos Educativos",show=False,marker = folium.Marker(icon=folium.Icon(color='red',icon="glyphicon-book")),tooltip=folium.GeoJsonTooltip(fields=['fna', 'BARRIO'
                                                                                                                                                    ],
                                                                                                                                                aliases=["Establecimiento: ",
                                                                                                                                                         "Barrio: "
                                                                                                                                                        ], 
                                                                                                                                                localize=True,
                                                                                                                                                sticky=False,
                                                                                                                                                labels=True,
                                                                                                                                                style="""
                                                                                                                                                    background-color: #F0EFEF;
                                                                                                                                                    border: 2px solid black;
                                                                                                                                                    border-radius: 3px;
                                                                                                                                                    box-shadow: 3px;
                                                                                                                                                """,
                                                                                                                                                max_width=800,))
    map.add_child(polig)
    
    choropleth = folium.Choropleth(
            geo_data=df_final1,
            name="Cantidad Votos por Circuitos",
            data=df_final,
            columns=('circuito', 'total_votos'),
            key_on='feature.properties.circuito',
            fill_color="YlOrRd",
            fill_opacity=0.5,
            line_opacity=0.5,
            legend_name="Cantidad Votos por Circuito",
            highlight=True,
            show=False,
        )
    choropleth.add_to(map)
    choropleth2 = folium.Choropleth(
            geo_data=df_final3,
            name=f"Votos {Opc_Agrupación} por Circuitos",
            data=df_x2,
            columns=('circuito', 'Porcentaje'),
            key_on='feature.properties.circuito',
            fill_color="YlOrRd",
            fill_opacity=0.5,
            line_opacity=0.5,
            legend_name=f"% Votos de {Opc_Agrupación}",
            highlight=True,
            show=False,)
    choropleth2.add_to(map)
    df_indexed = df_x.set_index('circuito')
    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['circuito']
        feature['properties']['total_votos'] = 'Cantidad de votos: ' + str(df_indexed.loc[state_name, 'total_votos']) if state_name in list(df_indexed.index) else ''

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['circuito', 'total_votos'], labels=False)
    )
    df_indexed = df_final3.set_index('circuito')
    for feature in choropleth2.geojson.data['features']:
        state_name = feature['properties']['circuito']
        feature['properties']['Porcentaje'] = 'Porcentaje de votos: ' + str(df_indexed.loc[state_name, 'Porcentaje']) if state_name in list(df_indexed.index) else ''
    choropleth2.geojson.add_child(
        folium.features.GeoJsonTooltip(['circuito', 'Porcentaje'], labels=False)
    )
    folium.LayerControl().add_to(map)
    st_map = st_folium(map, use_container_width=True)
    state_name = ''
    if st_map['last_active_drawing']:
        state_name = st_map['last_active_drawing']['properties']['circuito']                 
    return state_name

def show_map():  
    # Titulo de la página
    state_name = display_map(df)
    print(state_name)
