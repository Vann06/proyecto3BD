import streamlit as st
from reports.reporte_pedidos_cliente import pedidos_cliente_report

def mostrar_reporte_pedidos():
    st.header(" Reporte de Pedidos por Cliente")

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
                st.dataframe(df)
            else:
                st.info("No se encontraron pedidos con esos filtros.")
        except Exception as e:
            st.error(f"Error al generar el reporte: {e}")
