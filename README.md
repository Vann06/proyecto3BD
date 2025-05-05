# 📋 Sistema de Reportes para Cafetería

Esta es una aplicación web desarrollada en **Python (Streamlit)** con base de datos en **PostgreSQL**, diseñada para generar reportes visuales y exportables sobre inventario, pedidos, pagos y productos más vendidos en una cafetería. Se ejecuta completamente en contenedores Docker y permite filtros dinámicos, gráficas interactivas y descarga de reportes en formatos CSV y PDF.

---

## 🚀 Características actuales

✅ Reporte de inventario de productos  
✅ Reporte de pedidos por cliente  
✅ Reporte de productos más vendidos  
✅ Filtros dinámicos en cada reporte  
✅ Exportación a CSV y PDF  
✅ Gráficas interactivas con Plotly  
✅ Ejecutable desde Docker Compose  

---

## 📦 Tecnologías utilizadas

- [Python 3.11](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Docker](https://www.docker.com/)
- [Plotly](https://plotly.com/python/)
- [FPDF](https://py-pdf.github.io/fpdf2/)

---

## 📁 Estructura del proyecto

```plaintext
proyecto/
├── app.py                      # Navegación principal de la app
├── requirements.txt            # Dependencias de Python
├── Dockerfile                  # Imagen para Streamlit
├── docker-compose.yml          # Orquestador de app + base de datos

├── core/
│   ├── config.py               # Variables de entorno (host, puerto, etc.)
│   ├── db.py                   # Motor de conexión SQLAlchemy
│   └── utils.py                # Funciones reutilizables

├── database/
│   ├── 1_ddl.sql               # Script de creación de tablas y triggers
│   └── 2_data.sql              # Datos de prueba

├── reports/                    # Consultas SQL por reporte
│   ├── reporte_inventario.py
│   ├── reporte_pedidos_cliente.py
│   ├── reporte_top_productos.py
│   ├── reporte_clientes_frecuentes.py
│   └── reporte_pagos.py

├── render_reports/             # Interfaz de cada reporte (filtros + tabla + gráficas)
│   ├── render_inventario.py
│   ├── render_pedidos.py
│   ├── render_top_productos.py
│   ├── render_clientes_frecuentes.py
│   └── render_pagos.py

```

---

## ⚙️ Instalación y ejecución

### 1. Clona el repositorio

```bash
git clone https://github.com/tuusuario/proyecto3BD.git
cd proyecto3BD
```

### 2. Ejecuta con Docker

```bash
docker-compose up --build
```

### 3. Abre la aplicación en el navegador 
```bash
http://localhost:8502
```

Servidor disponible en:  
📍 \`http://localhost:8502\`

---

## 📊 Reportes disponibles

---

## 🧠 Reporte de Inventario de Productos

### Filtros aplicables:
- Nombre del producto
- Categoría
- Stock mínimo
- Stock máximo
- Precio mínimo
- Precio máximo
---

## 🧠 Reporte de Pedidos por Cliente

### Filtros aplicables:
- Fecha de inicio
- Fecha de fin
- Estado del pedido (Pendiente, Pagado, Cancelado)
- Monto mínimo
- Monto máximo
- Nombre o apellido del cliente
---

## 🧠 Reporte de Productos Más Vendidos

### Filtros aplicables:
- Fecha de inicio
- Fecha de fin
- Categoría
- Nombre del producto
- Monto mínimo vendido
- Stock máximo disponible

## 🧭 Funcionalidades para todos los Reportes

### Funcionalidades:
- Exportación a CSV
- Exportación a PDF
- Visualización de resultados en tabla
- Gráfica de barras modificable

## 👩‍💻 Autores

Vianka Castro - 23201
Ricardo Godínez - 23247
Camila Ritcher - 23183

