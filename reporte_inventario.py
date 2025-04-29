import pandas as pd
from sqlalchemy import text

def reporte_inventario(categoria=None, stock_min=None, stock_max=None, precio_min=None, precio_max=None, nombre_producto=None):
    query = """
    SELECT p.nombre AS producto, 
           c.nombre AS categoria, 
           p.cantidad_disponible AS stock_actual, 
           p.precio AS precio_unitario
    FROM Productos p
    JOIN Categorias c ON p.id_categoria = c.id
    WHERE 1=1
    """
    
    if categoria:
        query += f" AND c.nombre = :categoria"
    if stock_min is not None:
        query += f" AND p.cantidad_disponible >= :stock_min"
    if stock_max is not None:
        query += f" AND p.cantidad_disponible <= :stock_max"
    if precio_min is not None:
        query += f" AND p.precio >= :precio_min"
    if precio_max is not None:
        query += f" AND p.precio <= :precio_max"
    if nombre_producto:
        query += f" AND p.nombre ILIKE :nombre_producto"
    
    query += " ORDER BY p.nombre"
    
    result = session.execute(text(query), {'categoria': categoria, 'stock_min': stock_min, 'stock_max': stock_max, 
                                            'precio_min': precio_min, 'precio_max': precio_max, 'nombre_producto': f"%{nombre_producto}%"})
    
    df = pd.DataFrame(result.fetchall(), columns=['Producto', 'Categoría', 'Stock Actual', 'Precio Unitario'])
    
    return df
