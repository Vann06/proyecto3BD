import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from core.utils import exportar_a_pdf
from reports.reporte_top_productos import productos_top_report
from core.utils import obtener_categorias_disponibles

def mostrar_reporte_productos():
    st.header("Reporte de Productos Más Vendidos")
    categorias = obtener_categorias_disponibles()
    col1, col2, col3 = st.columns(3)
    with col1:
        fecha_inicio = st.date_input("Fecha inicio")
        fecha_fin = st.date_input("Fecha fin")
    with col2:
        categoria = st.selectbox("Categoría", [""] + categorias)
        nombre_producto = st.text_input("Nombre del producto")
    with col3:
        monto_min = st.number_input("Monto mínimo vendido", min_value=0.0, value=0.0)
        stock_max = st.number_input("Stock máximo disponible", min_value=0, value=100)

    if st.button("Generar Reporte"):
        df = productos_top_report(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            categoria=categoria or None,
            nombre_producto=nombre_producto or None,
            monto_min=monto_min,
            stock_max=stock_max
        )

        if not df.empty:
            df["Cantidad Vendida"] = df["Cantidad Vendida"].apply(lambda x: f"{int(x)}")
            df["Última Venta"] = pd.to_datetime(df["Última Venta"]).dt.strftime("%Y-%m-%d")

            st.success(f"Se encontraron {len(df)} productos vendidos.")
            st.dataframe(df, use_container_width=True)

            # Exportar CSV
            csv_data = df.to_csv(index=False).encode()
            st.download_button("Descargar CSV", data=csv_data, file_name="top_productos.csv", mime="text/csv")

            # Exportar PDF
            pdf_data = exportar_a_pdf(df,titulo="Reporte de TOP Productos")
            st.download_button("Descargar PDF", data=pdf_data, file_name="top_productos.pdf", mime="application/pdf")

            # Visualización gráfica
            st.subheader("Gráfica de Productos Más Vendidos")
            fig = px.bar(df, x="Producto", y="Cantidad Vendida", color="Categoría", title="Top Productos por Cantidad Vendida")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No se encontraron productos con los filtros especificados.")