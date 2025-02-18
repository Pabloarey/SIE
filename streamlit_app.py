import os
import pandas as pd
import streamlit as st
from streamlit_navigation_bar import st_navbar
import pages as pg
import login as login
 
st.set_page_config(initial_sidebar_state="collapsed",    page_title="SIE",
                   page_icon="./logos/SIE.jpeg",layout="wide")

login.generarLogin()
if 'usuario' in st.session_state:
  pages = ["Tablero","Mapa"]
  parent_dir = os.path.dirname(os.path.abspath(__file__))
  logo_path = os.path.join(parent_dir, "./logos/home.svg")
  styles = {
      "nav": {
          "background-color": "royalblue",
          "justify-content": "left",
      },
      "img": {
          "padding-right": "14px",
      },
      "span": {
          "color": "white",
          "padding": "16px",
      },
      "active": {
          "background-color": "white",
          "color": "var(--text-color)",
          "font-weight": "normal",
          "padding": "14px",
      }
  }
  options = {
      "show_menu": False,
      "show_sidebar": False,
  }
  
  page = st_navbar(
      pages,
      logo_path=logo_path,
      styles=styles,
      options=options,
  )
  
  functions = {
      "Home": pg.show_home,
      "Tablero": pg.show_tablero,
      "Mapa": pg.show_map,
  }
  go_to = functions.get(page)
  if go_to:
      go_to()
