import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st

load_dotenv()

def crearSitio():
    st.title("Dataset Delitos México")


def get_connection():
    return mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database= os.getenv("DB_NAME"),
    )

#Queries
delitoCiudad = """SELECT * FROM delitos 
        WHERE entidad like %s
        AND tipo_delito = %s;"""

registrosAnio = """SELECT anio, 
            COUNT(*) as numero_de_delitos FROM delitos 
            GROUP BY anio;"""

#with get_connection() as conn:
 #   df = pd.read_sql(delitoCiudad, conn, params=("Ciudad %","Despojo",))

#df.to_csv("despojosCdmx.csv")

with get_connection() as conn:
    registrosAnioDF = pd.read_sql(registrosAnio, conn)

#print(registrosAnioDF)

crearSitio()
