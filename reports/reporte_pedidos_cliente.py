import pandas as pd
from sqlalchemy import select, and_
import streamlit as st

from core.db import engine, reflect_single_table

def pedidos_cliente_report(
    fecha_inicio=None,
    fecha_fin=None,
    estado=None,
    monto_min=None,
    monto_max=None,
    nombre_cliente=None
) -> pd.DataFrame:

    pedidos_table = reflect_single_table('pedidos')
    clientes_table = reflect_single_table('clientes')

    if pedidos_table is None or clientes_table is None:
        st.error("No se pudieron cargar los datos de los pedidos ni de clientes")
        return pd.DataFrame()
    
    selector = select(
        pedidos_table.c.id.label('ID pedido'),
        pedidos_table.c.fecha.label('fecha pedido'),
        (clientes_table.c.nombre + ' ' + clientes_table.c.apellido).label('Cliente'),
        pedidos_table.c.estado.label('estado'),
        pedidos_table.c.total.label('total pedido')
    ).join(
        clientes_table, pedidos_table.c.id_cliente == clientes_table.c.id
    )

    filtros = []

    if fecha_inicio:
        filtros.append(pedidos_table.c.fecha >= fecha_inicio)
    if fecha_fin:
        filtros.append(pedidos_table.c.fecha <= fecha_fin)
    if estado:
        filtros.append(pedidos_table.c.estado == estado)
    if monto_min is not None:
        filtros.append(pedidos_table.c.total >= monto_min)
    if monto_max is not None:
        filtros.append(pedidos_table.c.total <= monto_max)
    if nombre_cliente:
        filtros.append(or_(
            clientes_table.c.nombre.ilike(f"%{nombre_cliente}%"),
            clientes_table.c.apellido.ilike(f"%{nombre_cliente}%")
        ))

    if filtros:
        selector = selector.where(and_(*filtros))

    selector = selector.order_by(pedidos_table.c.fecha)

    try:
        with engine.connect() as connection:
            df = pd.read_sql(selector, connection)
        return df
    except Exception as e:
        st.error(f"Error al ejecutar el reporte: {e}")
        return pd.DataFrame()