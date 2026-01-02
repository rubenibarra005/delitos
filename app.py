import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import plotly.express as px

load_dotenv()

def crearSitio(bienesAfectados, incidenciasPorAnio, historicoDelitosPorMes, incidenciasPorEstado):
    st.set_page_config(
        page_title="Delitos México",
        page_icon=":bar_chart:",
        layout="wide"
    )
   
    st.header("Dataset Delitos México 2015 - 2025")
    st.write("Base de datos pública del Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública (SESNSP) " \
    "Se muestran los hechos delictivos ocurridos entre 2015 y noviembre 2025. ")
   
    with st.container(border=True):
        fig = px.pie(incidenciasPorAnio, names="anio",values="numero_de_delitos",
                    labels={
                        "anio" : "Año",
                        "numero_de_delitos" : "Delitos registrados"
                    }, title="Incidencias por año", hole=0.4)
        st.plotly_chart(fig, theme=None)
        
        col1, col2 = st.columns(2)
        with col1:
            st.header("Bienes afectados",text_alignment="center")
            st.bar_chart(bienesAfectados, x="bien_juridico_afectado", y="conteo_bienes",x_label="Bien Afectado", y_label="Conteo",
                        color="#ffaa00", )
        with col2:
            st.header("Historico delitos ocurridos por mes", text_alignment="center")
            st.bar_chart(historicoDelitosPorMes, x="mes", y="total_delitos", x_label="Mes", y_label="Delitos ocurridos",
                        color="#3c6acd",)
            
        st.header("Número de incidencias por estado", text_alignment="center")

        top_n = st.slider(
            "Mostrar top N entidades",
            min_value=1,
            max_value=len(incidenciasPorEstado),
            value=5)

        incidenciasPorEstado_plot = (
            incidenciasPorEstado.head(top_n)
        )
        st.bar_chart(incidenciasPorEstado_plot, x="entidad", y="incidencia_por_estado", 
                     x_label="Entidad", y_label="Número de incidentes",
                     color="#ff24bd")
        


def get_connection():
    return mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database= os.getenv("DB_NAME"),
    )

#Queries

bienesAfectados = """SELECT bien_juridico_afectado, 
                    SUM(incidencia_delictiva) as conteo_bienes FROM delitos 
                    GROUP BY bien_juridico_afectado
                    ORDER BY conteo_bienes 
                    DESC limit 8;"""

incidenciaPorAnio = """SELECT anio, 
                    SUM(incidencia_delictiva) as numero_de_delitos 
                    FROM delitos GROUP BY anio;"""

historicoDelitosPorMes = """SELECT mes, SUM(incidencia_delictiva) as total_delitos 
                        FROM delitos GROUP BY mes 
                        ORDER BY total_delitos DESC;"""

incidenciasPorEstado = """SELECT entidad, SUM(incidencia_delictiva) as incidencia_por_estado 
                        FROM delitos GROUP BY entidad
                        ORDER BY incidencia_por_estado DESC;
                        """


with get_connection() as conn: 
    bienesAfectadosDF = pd.read_sql(bienesAfectados, conn)

with get_connection() as conn:
    incidenciaPorAnioDF = pd.read_sql(incidenciaPorAnio, conn)

with get_connection() as conn:
    historicoDelitosPorMesDF = pd.read_sql(historicoDelitosPorMes, conn)

with get_connection() as conn:
    incidenciasPorEstadoDF = pd.read_sql(incidenciasPorEstado, conn)


bienesAfectadosDF["bien_juridico_afectado"] = pd.Categorical(
    bienesAfectadosDF["bien_juridico_afectado"],
    categories=bienesAfectadosDF["bien_juridico_afectado"],
    ordered=True
)

historicoDelitosPorMesDF["mes"] = pd.Categorical(
    historicoDelitosPorMesDF["mes"],
    categories=historicoDelitosPorMesDF["mes"],
    ordered=True
)

incidenciasPorEstadoDF["entidad"] = pd.Categorical(
    incidenciasPorEstadoDF["entidad"],
    categories = incidenciasPorEstadoDF["entidad"],
    ordered=True
)


crearSitio(bienesAfectadosDF, incidenciaPorAnioDF, historicoDelitosPorMesDF, incidenciasPorEstadoDF)
