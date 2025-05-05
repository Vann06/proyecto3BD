import pandas as pd
from sqlalchemy import select, and_, func
import streamlit as st
from core.db import engine, reflect_single_table

def pagos_report(fecha_inicio=None, fecha_fin=None, metodo_pago=None, estado_pedido=None, monto_min=None, monto_max=None) -> pd.DataFrame:

    pagos_table = reflect_single_table('pagos')
    pedidos_table = reflect_single_table('pedidos')
    metodo_pago_table = reflect_single_table('metodopagos')
    clientes_table = reflect_single_table('clientes')
    
    if any(table is None for table in [pagos_table, pedidos_table, metodo_pago_table, clientes_table]):
        st.error("No se pudieron cargar las tablas necesarias para el reporte de pagos.")
        return pd.DataFrame()

    selector = select(
        pagos_table.c.id.label('id_pago'),
        pagos_table.c.fecha_pago.label('fecha_pago'),
        pagos_table.c.monto.label('monto'),
        metodo_pago_table.c.nombre.label('metodo_pago'),
        pedidos_table.c.estado.label('estado_pedido'),
        pedidos_table.c.id.label('id_pedido'),
        clientes_table.c.nombre.label('nombre_cliente'),
        clientes_table.c.apellido.label('apellido_cliente')
    ).select_from(
        pagos_table
        .join(pedidos_table, pagos_table.c.id_pedido == pedidos_table.c.id)
        .join(metodo_pago_table, pagos_table.c.id_metodo_pago == metodo_pago_table.c.id)
        .join(clientes_table, pedidos_table.c.id_cliente == clientes_table.c.id)
    )

    filtros = []
    
    if fecha_inicio:
        filtros.append(pagos_table.c.fecha_pago >= fecha_inicio)
    if fecha_fin:
        filtros.append(pagos_table.c.fecha_pago <= fecha_fin)
    if metodo_pago:
        filtros.append(metodo_pago_table.c.nombre == metodo_pago)
    if estado_pedido:
        filtros.append(pedidos_table.c.estado == estado_pedido)
    if monto_min is not None:
        filtros.append(pagos_table.c.monto >= monto_min)
    if monto_max is not None:
        filtros.append(pagos_table.c.monto <= monto_max)
    
    if filtros:
        selector = selector.where(and_(*filtros))

    selector = selector.order_by(pagos_table.c.fecha_pago.desc())
    
    try:
        with engine.connect() as connection:
            df = pd.read_sql(selector, connection)

            if not df.empty:
                df['cliente'] = df['nombre_cliente'] + ' ' + df['apellido_cliente']

                df = df[['id_pago', 'fecha_pago', 'monto', 'metodo_pago', 'estado_pedido', 'id_pedido', 'cliente']]
                
                df['monto'] = df['monto'].round(2)
                
    except Exception as e:
        st.error(f"Error ejecutando consulta de pagos: {e}")
        print(f"Error ejecutando consulta de pagos: {e}")
        return pd.DataFrame()
    
    return df
