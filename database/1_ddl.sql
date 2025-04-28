
CREATE TABLE Clientes (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  telefono VARCHAR(20) NOT NULL,
  correo VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE ClienteTelefonos (
  id SERIAL PRIMARY KEY,
  id_cliente INT NOT NULL,
  telefono VARCHAR(20) NOT NULL,
  FOREIGN KEY (id_cliente) REFERENCES Clientes(id)
);

CREATE TABLE Categorias (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL
);

CREATE TABLE Productos (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT NOT NULL,
  precio DECIMAL(10,2) NOT NULL,
  id_categoria INT NOT NULL,
  cantidad_disponible INT NOT NULL,
  FOREIGN KEY (id_categoria) REFERENCES Categorias(id)
);

CREATE TABLE ProductoIngredientes (
  id SERIAL PRIMARY KEY,
  id_producto INT NOT NULL,
  ingrediente VARCHAR(100) NOT NULL,
  FOREIGN KEY (id_producto) REFERENCES Productos(id)
);

CREATE TABLE Pedidos (
  id SERIAL PRIMARY KEY,
  id_cliente INT NOT NULL,
  fecha TIMESTAMP NOT NULL,
  estado VARCHAR(50) NOT NULL CHECK (estado IN ('Pendiente', 'Pagado', 'Cancelado')),
  total DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (id_cliente) REFERENCES Clientes(id)
);

CREATE TABLE DetallesPedidos (
  id SERIAL PRIMARY KEY,
  id_pedido INT NOT NULL,
  id_producto INT NOT NULL,
  cantidad INT NOT NULL CHECK (cantidad > 0),
  precio_unitario DECIMAL(10,2) NOT NULL,
  subtotal DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (id_pedido) REFERENCES Pedidos(id),
  FOREIGN KEY (id_producto) REFERENCES Productos(id)
);

CREATE TABLE Roles (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL
);

CREATE TABLE Empleados (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  id_rol INT NOT NULL,
  FOREIGN KEY (id_rol) REFERENCES Roles(id)
);

CREATE TABLE MetodoPagos (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL
);

CREATE TABLE Pagos (
  id SERIAL PRIMARY KEY,
  id_pedido INT NOT NULL,
  id_metodo_pago INT NOT NULL,
  monto DECIMAL(10,2) NOT NULL,
  fecha_pago TIMESTAMP NOT NULL,
  FOREIGN KEY (id_pedido) REFERENCES Pedidos(id),
  FOREIGN KEY (id_metodo_pago) REFERENCES MetodoPagos(id)
);


CREATE TABLE EmpleadoPedidos (
  id SERIAL PRIMARY KEY,
  id_empleado INT NOT NULL,
  id_pedido INT NOT NULL,
  FOREIGN KEY (id_empleado) REFERENCES Empleados(id),
  FOREIGN KEY (id_pedido) REFERENCES Pedidos(id)
);
