import streamlit as st
from sqlalchemy import select
from core.db import engine, reflect_single_table
import pandas as pd
import plotly.express as px
import datetime
from io import BytesIO
from core.utils import exportar_a_pdf, obtener_metodos_pago_disponibles, obtener_estados_pedido_disponibles
from reports.reporte_pagos import pagos_report

def mostrar_reporte_pagos():
    st.header("Reporte de Pagos")
    
    metodos_pago = obtener_metodos_pago_disponibles()
    estados_pedido = obtener_estados_pedido_disponibles()

    col1, col2, col3 = st.columns(3)
    with col1:
        fecha_inicio = st.date_input("Fecha inicio", value=datetime.date(2023, 1, 1), key="fecha_ini")
        fecha_fin = st.date_input("Fecha fin", value=datetime.date.today(), key="fecha_fin")
    with col2:
        metodo = st.selectbox("Método de pago", [""] + metodos_pago, key="metodo")
        estado = st.selectbox("Estado del pedido", [""] + estados_pedido, key="estado")
    with col3:
        monto_min = st.number_input("Monto mínimo", min_value=0.0, value=0.0, step=0.01)
        monto_max = st.number_input("Monto máximo", min_value=0.0, value=10000.0, step=0.01)
    
    if st.button("Generar Reporte", key="gen_pagos"):
        df = pagos_report(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            metodo_pago=metodo or None,
            estado_pedido=estado or None,
            monto_min=monto_min,
            monto_max=monto_max
        )
        
        if not df.empty:
            st.success(f"Se encontraron {len(df)} resultados")
            st.dataframe(df, use_container_width=True)
            
            st.download_button("Descargar CSV", df.to_csv(index=False).encode(), "pagos.csv", "text/csv")
            pdf_data = exportar_a_pdf(df, titulo="Reporte de Pagos")
            st.download_button("Descargar PDF", data=pdf_data, file_name="pagos.pdf", mime="application/pdf")
            
            st.subheader("Gráfica de Pagos por Fecha")
            if not pd.api.types.is_datetime64_any_dtype(df['fecha_pago']):
                df['fecha_pago'] = pd.to_datetime(df['fecha_pago'])
            
            fig = px.histogram(df, x="fecha_pago", y="monto", nbins=30, title="Monto de pagos por día")
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Pagos por Método de Pago")
            fig_pie = px.pie(df, names="metodo_pago", values="monto", title="Distribución de pagos por método")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("No se encontraron pagos con los filtros especificados.")
