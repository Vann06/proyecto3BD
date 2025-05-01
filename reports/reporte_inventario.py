import pandas as pd
from sqlalchemy import select, and_
import streamlit as st

from core.db import engine, reflect_single_table

def inventario_report(categoria: str = None, stock_min: int = None, stock_max: int = None, precio_min: float = None, precio_max: float = None, nombre_producto: str = None) -> pd.DataFrame:

    productos_table = reflect_single_table('productos')
    categorias_table = reflect_single_table('categorias')

    if productos_table is None or categorias_table is None:
        st.error("No se pudieron cargar los datos de las categorias o de los productos")
        return pd.DataFrame()
    
    selector = select(
        productos_table.c.nombre.label('productos'),
        categorias_table.c.nombre.label('categoria'),
        productos_table.c.cantidad_disponible.label('cantidad'),
        productos_table.c.precio.label('precio')
    ).join(
        categorias_table, productos_table.c.id_categoria == categorias_table.c.id
    )

    filtros = []

    if categoria:
        filtros.append(categorias_table.c.nombre == categoria)
    if stock_min is not None:
        filtros.append(productos_table.c.cantidad_disponible >= stock_min)
    if stock_max is not None:
        filtros.append(productos_table.c.cantidad_disponible <= stock_max)
    if precio_min is not None:
        filtros.append(productos_table.c.precio >= precio_min)
    if precio_max is not None:
        filtros.append(productos_table.c.precio <= precio_max)
    if nombre_producto:
        filtros.append(productos_table.c.nombre.ilike(f"%{nombre_producto}%"))

    if filtros : 
        selector = selector.where(and_(*filtros))

    selector = selector.order_by(productos_table.c.nombre)

    try:
        with engine.connect() as connection:
            df = pd.read_sql(selector, connection)
    except Exception as e:
        print(f"Error ejecutando consulta de inventario: {e}")
        return pd.DataFrame()

    return df

