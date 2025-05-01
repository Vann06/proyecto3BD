import streamlit as st
import pandas as pd
from sqlalchemy.exc import OperationalError
from render_reports.render_inventario import mostrar_reporte_inventario
from render_reports.render_pedidos_cliente import mostrar_reporte_pedidos
from render_reports.render_top_productos import mostrar_reporte_productos
from core.config import DB_HOST, DB_NAME
from core.db import engine, inspect

st.set_page_config(layout="wide")
st.title("Sistema de Reportes")

if 'reporte_actual' not in st.session_state:
    st.session_state['reporte_actual'] = None

reportes = {
    "inventario": "Inventario de Productos",
    "pedidos" : "Pedidos con Clientes",
    "top_productos": "Productos más Vendidos",

}


def set_reporte(nombre_reporte):
    st.session_state['reporte_actual'] = nombre_reporte


# Verificar conexión y mostrar barra lateral
try:
    ins = inspect(engine)
    table_names = ins.get_table_names()
    
    st.sidebar.success(f"Conectado a: {DB_NAME}@{DB_HOST}")
    st.sidebar.header("Reportes Disponibles")
    
    if table_names:
        for key, nombre in reportes.items():
            st.sidebar.button(nombre, key=f"btn_{key}", on_click=set_reporte, args=(key,))
    else:
        st.sidebar.error("No hay tablas disponibles en la base de datos.")
        st.warning("No se pueden generar reportes sin tablas en la base de datos.")

except OperationalError as e:
    st.sidebar.error("Error de conexión a la base de datos")
    st.info(f"Verifica la conexión: {e}")
except Exception as e:
    st.sidebar.error(f"Error: {e}")

if st.session_state['reporte_actual'] == "inventario":
    mostrar_reporte_inventario()

elif st.session_state['reporte_actual'] == "pedidos":
    mostrar_reporte_pedidos()

elif st.session_state["reporte_actual"] == "top_productos":
    mostrar_reporte_productos()

    

elif st.session_state['reporte_actual'] is None:
    st.header("Bienvenido al Sistema de Reportes")
    st.info("Selecciona un reporte de la barra lateral para comenzar.")
