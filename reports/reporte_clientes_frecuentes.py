import pandas as pd
from sqlalchemy import select, and_, func
import streamlit as st

from core.db import engine, reflect_single_table

def clientes_frecuentes_report(fecha_inicio=None, fecha_fin=None, gasto_minimo=None, pedidos_minimos=None, categoria_producto=None, ultima_compra=None) -> pd.DataFrame:
    
    pedidos_table = reflect_single_table('pedidos')
    clientes_table = reflect_single_table('clientes')
    detalles_table = reflect_single_table('detallespedidos')
    productos_table = reflect_single_table('productos')
    categorias_table = reflect_single_table('categorias')
    
    if None in [pedidos_table, clientes_table, detalles_table, productos_table, categorias_table]:
        st.error("No se pudieron cargar las tablas necesarias para el reporte de clientes.")
        return pd.DataFrame()
    
    selector = select(
        clientes_table.c.id.label('id_cliente'),
        clientes_table.c.nombre,
        clientes_table.c.apellido,
        clientes_table.c.correo,
        func.count(pedidos_table.c.id).label('cantidad_pedidos'),
        func.sum(pedidos_table.c.total).label('total_gastado'),
        func.max(pedidos_table.c.fecha).label('ultima_compra')
    ).select_from(
        clientes_table
        .join(pedidos_table, pedidos_table.c.id_cliente == clientes_table.c.id)
        .join(detalles_table, detalles_table.c.id_pedido == pedidos_table.c.id)
        .join(productos_table, productos_table.c.id == detalles_table.c.id_producto)
        .join(categorias_table, categorias_table.c.id == productos_table.c.id_categoria)
    ).group_by(
        clientes_table.c.id,
        clientes_table.c.nombre,
        clientes_table.c.apellido,
        clientes_table.c.correo
    )
    
    filtros = []
    having_filtros = []
    
    if fecha_inicio:
        filtros.append(pedidos_table.c.fecha >= fecha_inicio)
    if fecha_fin:
        filtros.append(pedidos_table.c.fecha <= fecha_fin)
    if categoria_producto:
        filtros.append(categorias_table.c.nombre == categoria_producto)

    if filtros:
        selector = selector.where(and_(*filtros))

    if gasto_minimo is not None:
        having_filtros.append(func.sum(pedidos_table.c.total) >= gasto_minimo)
    
    if pedidos_minimos is not None and pedidos_minimos > 0:
        having_filtros.append(func.count(pedidos_table.c.id) >= pedidos_minimos)
        
    if ultima_compra:
        fecha_limite = func.current_date() - func.make_interval(0,0,0,ultima_compra)
        having_filtros.append(func.max(pedidos_table.c.fecha) >= fecha_limite)
    
    if having_filtros:
        selector = selector.having(and_(*having_filtros))

    selector = selector.order_by(func.sum(pedidos_table.c.total).desc())
    
    try:
        with engine.connect() as connection:
            df = pd.read_sql(selector, connection)
    except Exception as e:
        print(f"Error ejecutando consulta de clientes frecuentes: {e}")
        return pd.DataFrame()
    
    return df
