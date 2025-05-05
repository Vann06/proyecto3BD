import streamlit as st
import plotly.express as px
from core.utils import exportar_a_pdf
from reports.reporte_pedidos_cliente import pedidos_cliente_report

def mostrar_reporte_pedidos():
    st.header("Reporte de Pedidos por Cliente")

    col1, col2, col3 = st.columns(3)
    with col1:
        nombre_cliente = st.text_input("Cliente (nombre o apellido)")
        estado = st.selectbox("Estado", ["", "Pendiente", "Pagado", "Cancelado"])
    with col2:
        fecha_inicio = st.date_input("Fecha inicio", key="fecha_ini")
        fecha_fin = st.date_input("Fecha fin", key="fecha_fin")
    with col3:
        monto_min = st.number_input("Monto mínimo", min_value=0.0, value=0.0)
        monto_max = st.number_input("Monto máximo", min_value=0.0, value=10000.0)

    if st.button("Generar reporte", key="gen_pedidos"):
        try:
            df = pedidos_cliente_report(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                estado=estado if estado else None,
                monto_min=monto_min,
                monto_max=monto_max,
                nombre_cliente=nombre_cliente or None
            )

            if not df.empty:
                st.success(f"Se encontraron {len(df)} pedidos")
                st.dataframe(df, use_container_width=True)

                # Exportar CSV
                csv_data = df.to_csv(index=False).encode()
                st.download_button("Descargar CSV", data=csv_data, file_name="pedidos_cliente.csv", mime="text/csv")

                # Exportar PDF
                pdf_data = exportar_a_pdf(df,titulo="Reporte de Pedidos con Clientes")
                st.download_button("Descargar PDF", data=pdf_data, file_name="pedidos_cliente.pdf", mime="application/pdf")

                # Gráfica por estado
                st.subheader("Gráfica de Pedidos por Estado")
                conteo = df["estado"].value_counts().reset_index()
                conteo.columns = ["Estado", "Cantidad"]
                fig = px.bar(conteo, x="Estado", y="Cantidad", title="Cantidad de Pedidos por Estado", color="Estado")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No se encontraron pedidos con esos filtros.")
        except Exception as e:
            st.error(f"Error al generar el reporte: {e}")
