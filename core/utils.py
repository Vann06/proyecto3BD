from sqlalchemy import select
from fpdf import FPDF
from core.db import engine, reflect_single_table

def obtener_categorias_disponibles():
    categorias_table = reflect_single_table("categorias")
    try:
        with engine.connect() as conn:
            query = select(categorias_table.c.nombre)
            result = conn.execute(query)
            categorias = [row[0] for row in result.fetchall()]
            return categorias
    except Exception as e:
        print(f"Error cargando categorías: {e}")
        return []


def exportar_a_pdf(df, titulo="Reporte"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, titulo, ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 10)
    for col in df.columns:
        pdf.cell(40, 10, str(col), 1)
    pdf.ln()

    pdf.set_font("Arial", size=10)
    for _, row in df.iterrows():
        for item in row:
            pdf.cell(40, 10, str(item), 1)
        pdf.ln()

    return pdf.output(dest="S").encode("latin1")

def obtener_metodos_pago_disponibles():
    metodos_pago_table = reflect_single_table('metodopagos')
    if metodos_pago_table is None:
        return []
    
    try:
        stmt = select(metodos_pago_table.c.nombre).distinct().order_by(metodos_pago_table.c.nombre)
        with engine.connect() as connection:
            result = connection.execute(stmt).fetchall()
        return [r[0] for r in result]
    except Exception as e:
        print(f"Error obteniendo métodos de pago: {e}")
        return []

def obtener_estados_pedido_disponibles():
    pedidos_table = reflect_single_table('pedidos')
    if pedidos_table is None:
        return []
    
    try:
        stmt = select(pedidos_table.c.estado).distinct().order_by(pedidos_table.c.estado)
        with engine.connect() as connection:
            result = connection.execute(stmt).fetchall()
        return [r[0] for r in result]
    except Exception as e:
        print(f"Error obteniendo estados de pedido: {e}")
        return []