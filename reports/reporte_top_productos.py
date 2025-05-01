import pandas as pd
from sqlalchemy import select, func, and_, or_
import streamlit as st
from core.db import engine, reflect_single_table

def productos_top_report(
    fecha_inicio=None,
    fecha_fin=None,
    categoria=None,
    nombre_producto=None,
    monto_min=None,
    stock_max=None
) -> pd.DataFrame:

    dp = reflect_single_table("detallespedidos")
    p = reflect_single_table("productos")
    c = reflect_single_table("categorias")
    pe = reflect_single_table("pedidos")

    if None in [dp, p, c, pe]:
        st.error("No se pudieron reflejar las tablas necesarias para este reporte.")
        return pd.DataFrame()

    selector = select(
        p.c.nombre.label("Producto"),
        c.c.nombre.label("Categoría"),
        func.sum(dp.c.cantidad).label("Cantidad Vendida"),
        func.sum(dp.c.subtotal).label("Total Vendido"),
        p.c.precio.label("Precio Unitario"),
        func.max(pe.c.fecha).label("Última Venta")
    ).join(
        dp, dp.c.id_producto == p.c.id
    ).join(
        pe, dp.c.id_pedido == pe.c.id
    ).join(
        c, p.c.id_categoria == c.c.id
    )

    filtros = []
    if fecha_inicio:
        filtros.append(pe.c.fecha >= fecha_inicio)
    if fecha_fin:
        filtros.append(pe.c.fecha <= fecha_fin)
    if categoria:
        filtros.append(c.c.nombre == categoria)
    if nombre_producto:
        filtros.append(p.c.nombre.ilike(f"%{nombre_producto}%"))
    if stock_max is not None:
        filtros.append(p.c.cantidad_disponible <= stock_max)

    if filtros:
        selector = selector.where(and_(*filtros))

    selector = selector.group_by(p.c.nombre, c.c.nombre, p.c.precio)

    if monto_min is not None and monto_min > 0:
        selector = selector.having(func.sum(dp.c.subtotal) >= monto_min)

    selector = selector.order_by(func.sum(dp.c.cantidad).desc())

    try:
        with engine.connect() as conn:
            df = pd.read_sql(selector, conn)
            return df
    except Exception as e:
        st.error(f"Error al ejecutar el reporte: {e}")
        return pd.DataFrame()
