import streamlit as st
from sqlalchemy import select
from core.db import engine, reflect_single_table
import pandas as pd
import plotly.express as px
from io import BytesIO
from core.utils import exportar_a_pdf
from core.utils import obtener_categorias_disponibles
from reports.reporte_clientes_frecuentes import clientes_frecuentes_report
import datetime

def mostrar_reporte_clientes():
    st.header("Reporte de Clientes Frecuentes")

    categorias = obtener_categorias_disponibles()

    col1, col2, col3 = st.columns(3)
    with col1:
        fecha_inicio = st.date_input("Fecha inicio", value=datetime.date(2023, 1, 1), key="fecha_ini_cli")
        fecha_fin = st.date_input("Fecha fin", value=datetime.date.today(), key="fecha_fin_cli")
    with col2:
        gasto_minimo = st.number_input("Gasto mínimo", min_value=0.0, value=0.0, step=1.0)
        pedidos_minimos = st.number_input("Cantidad mínima de pedidos", min_value=1, value=1, step=1)
    with col3:
        categoria = st.selectbox("Categoría comprada", [""] + categorias, key="categoria_cli")

    if st.button("Generar Reporte", key="gen_clientes"):
        df = clientes_frecuentes_report(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            gasto_minimo=gasto_minimo,
            pedidos_minimos=pedidos_minimos,
            categoria_producto=categoria or None
        )

        if not df.empty:
            st.success(f"Se encontraron {len(df)} clientes frecuentes")
            st.dataframe(df, use_container_width=True)

            st.download_button("Descargar CSV", df.to_csv(index=False).encode(), "clientes_frecuentes.csv", "text/csv")
            pdf_data = exportar_a_pdf(df, titulo="Reporte de Clientes Frecuentes")
            st.download_button("Descargar PDF", data=pdf_data, file_name="clientes_frecuentes.pdf", mime="application/pdf")

            st.subheader("Gráfica de Clientes por Total Gastado")
            fig = px.bar(df, x="nombre", y="total_gastado", title="Total gastado por cliente")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No se encontraron clientes con los filtros especificados.")
