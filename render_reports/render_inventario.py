
import streamlit as st
import plotly.express as px
from core.utils import exportar_a_pdf
from reports.reporte_inventario import inventario_report
from core.utils import obtener_categorias_disponibles

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
                st.download_button("Descargar CSV", df.to_csv(index=False).encode(), "inventario.csv", "text/csv")
                pdf_data = exportar_a_pdf(df, titulo="Reporte de Inventario")
                st.download_button("Descargar PDF", data=pdf_data, file_name="pedidos_cliente.pdf", mime="application/pdf")

                st.subheader("Gráfica de Inventario")
                fig = px.bar(df, x="productos", y="cantidad", title="Cantidad disponible por producto")
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.warning("No se encontraron productos con los filtros especificados.")
        except Exception as e:
            st.error(f" Error al generar el reporte: {e}")

