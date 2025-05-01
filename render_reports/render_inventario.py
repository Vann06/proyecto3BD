
import streamlit as st
from reports.reporte_inventario import inventario_report
from sqlalchemy import select
from core.db import engine, reflect_single_table

def mostrar_reporte_inventario():
    st.header(" Reporte de Inventario de Productos")
    categorias_disponibles = obtener_categorias_disponibles()

    col1, col2, col3 = st.columns(3)
    
    with col1:
        nombre_producto = st.text_input("Nombre del producto:", key="nombre_prod")
        categoria = st.selectbox("Categoría:", options=[""] + categorias_disponibles, key="cat")

    
    with col2:
        stock_min = st.number_input("Stock mínimo:", min_value=0, value=0, key="stock_min")
        stock_max = st.number_input("Stock máximo:", min_value=0, value=1000, key="stock_max")
    
    with col3:
        precio_min = st.number_input("Precio mínimo:", min_value=0.0, value=0.0, step=0.01, key="precio_min")
        precio_max = st.number_input("Precio máximo:", min_value=0.0, value=1000.0, step=0.01, key="precio_max")
    
    if st.button("Generar Reporte", key="gen_inventario"):
        try:
            df = inventario_report(
                nombre_producto=nombre_producto or None,
                categoria=categoria or None,
                stock_min=stock_min,
                stock_max=stock_max,
                precio_min=precio_min,
                precio_max=precio_max
            )
            
            if not df.empty:
                st.success(f"Se encontraron {len(df)} resultados")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No se encontraron productos con los filtros especificados.")
        except Exception as e:
            st.error(f" Error al generar el reporte: {e}")


def obtener_categorias_disponibles():
    categorias_table = reflect_single_table("categorias")
    try:
        with engine.connect() as conn:
            query = select(categorias_table.c.nombre)
            result = conn.execute(query)
            categorias = [row[0] for row in result.fetchall()]
            return categorias
    except Exception as e:
        print(f"Error cargando categorías: {e}")
        return []