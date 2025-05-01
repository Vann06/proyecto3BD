import streamlit as st
import pandas as pd
from sqlalchemy.exc import OperationalError
from reports.reporte_inventario import inventario_report

from core.config import DB_HOST, DB_NAME
from core.db import engine, inspect

st.set_page_config(layout="wide")
st.title("Sistema de Reportes")

if 'reporte_actual' not in st.session_state:
    st.session_state['reporte_actual'] = None

reportes = {
    "inventario": "Inventario de Productos",

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
    st.header("Reporte de Inventario de Productos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nombre_producto = st.text_input("Filtrar por nombre de producto:", key="nombre_prod")
        categoria = st.text_input("Filtrar por categoría:", key="cat")
    
    with col2:
        stock_min = st.number_input("Stock mínimo:", min_value=0, value=0, key="stock_min")
        stock_max = st.number_input("Stock máximo:", min_value=0, value=1000, key="stock_max")
    
    with col3:
        precio_min = st.number_input("Precio mínimo:", min_value=0.0, value=0.0, step=0.01, key="precio_min")
        precio_max = st.number_input("Precio máximo:", min_value=0.0, value=1000.0, step=0.01, key="precio_max")
    
    if st.button("Generar Reporte", key="gen_inventario"):
        try:
            df = inventario_report(
                nombre_producto=nombre_producto if nombre_producto else None,
                categoria=categoria if categoria else None,
                stock_min=stock_min,
                stock_max=stock_max,
                precio_min=precio_min,
                precio_max=precio_max
            )
            
            if not df.empty:
                st.subheader("Resultados")
                st.dataframe(df)
            else:
                st.info("No se encontraron productos con los filtros especificados.")
        except Exception as e:
            st.error(f"Error al generar el reporte: {e}")

elif st.session_state['reporte_actual'] is None:
    st.header("Bienvenido al Sistema de Reportes")
    st.info("Selecciona un reporte de la barra lateral para comenzar.")
