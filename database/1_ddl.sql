
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



-- Triggers funcionales 


-- trigger para manejar las sumas de un pedido 
CREATE OR REPLACE FUNCTION actualizar_total_pedido()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE Pedidos
  SET total = (
    SELECT SUM(subtotal)
    FROM DetallesPedidos
    WHERE id_pedido = NEW.id_pedido
  )
  WHERE id = NEW.id_pedido;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_actualizar_total
AFTER INSERT OR UPDATE OR DELETE ON DetallesPedidos
FOR EACH ROW EXECUTE FUNCTION actualizar_total_pedido();


-- trigger para actualizar el stock actual 
CREAtE OR REPLACE FUNCTION actualizar_stock_productos()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.estado = 'Pagado' AND OLD.estado <> 'Pagado' THEN
    UPDATE Productos
    SET cantidad_disponible = cantidad_disponible - dp.cantidad
    FROM DetallesPedidos dp
    WHERE dp.id_pedido = NEW.id AND Productos.id = dp.id_producto;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_actualizar_stock
AFTER UPDATE ON Pedidos
FOR EACH ROW EXECUTE FUNCTION actualizar_stock_productos();

-- trigger para verificar que existe suficiente stock disponible

CREATE OR REPLACE FUNCTION verificar_stock_productos()
RETURNS TRIGGER AS $$
DECLARE
  stock_actual INT;
BEGIN
  SELECT cantidad_disponible INTO stock_actual
  FROM Productos
  WHERE id = NEW.id_producto;
  
  IF NEW.cantidad > stock_actual THEN
    RAISE EXCEPTION 'Stock insuficiente para el producto %', NEW.id_producto;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_verificar_stock
BEFORE INSERT ON DetallesPedidos
FOR EACH ROW EXECUTE FUNCTION verificar_stock_productos();