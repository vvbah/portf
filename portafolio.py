import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from proyecto1 import main as proyecto1_main
from proyecto2 import main as proyecto2_main
from proyecto3 import main as proyecto3_main


##########################################################################################################################
################################## PORTADA PORTAFOLIO ####################################################################
##########################################################################################################################


#### NOMBRE PESTAÑA:

st.set_page_config(page_title="Portafolio Virtual", page_icon=":computer:")

#### BARRA LATERAL:

with st.sidebar:
    pagina_actual = option_menu("Menu", ["Sobre Mí", 'Predicción Precio Propiedades',
                                        'Estudio Estación Central', 'Similitud de Textos'], 
        icons=['house', 'book','book','book'], default_index=0)

if pagina_actual == "Sobre Mí":

    st.title("""Portafolio Virtual""")
    st.write('---')

    st.header('Sobre mi:')
    st.write("""
        Hola! Soy Valentina Vergara, egresada de Ingeniería Comercial con Máster en Business Analytics de la Universidad 
    Adolfo Ibáñez. He desempeñado mi práctica intermedia en el área de marketing digital del emprendimiento chileno 
    Rew y, además, realicé mi práctica profesional en el área comercial/producto de Maxxa, una fintech chilena, en 
    donde pude potenciar los conocimientos adquiridos en el Máster participando en el desarrollo de un modelo de *machine learning* para predecir fuga 
    de clientes mensuales, automatización de KPIs informados vía mail y en transformación y carga de datos. Soy 
    fiel creedora de que el análisis de datos y la creación de modelos predictivos/clasificadores pueden aportar 
    gran valor a las empresas ya que ayudan a tomar mejores decisiones para la firma, además de otros grandes beneficios. 
    Por esta razón me he interesado en estudiar ente rubro, presentando un gran interés en *machine learning*, 
    representación visual de datos y procesos ETL.  

    + **Manejo los siguientes lenguajes de programación:** Python, SQL, R.  
    + **Principales Habilidades:**  
        + Modelos de predicción y clasificación con sklearn (python).  
        + Visualización de datos con matplotlib, seaborn, plotly express (python) y ggplot2 (R).  
        + Análisis de datos con pandas, numpy (python), data.table, tidyr y dplyr (R).  
        + Visualizaciones de aplicaciones, machine learning y paneles de control con streamlit (python).  
        + Visualización datos espaciales con geopandas (python), sp y rgdal (R).   

    En el menú de la izquierda podrás encontrar diferentes proyectos en los que he participado.
    """)

elif pagina_actual == "Predicción Precio Propiedades":
    proyecto1_main()
elif pagina_actual == "Estudio Estación Central":
    proyecto2_main()
elif pagina_actual == "Similitud de Textos":
    proyecto3_main()

