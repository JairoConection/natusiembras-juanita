CREATE DATABASE IF NOT EXISTS natusiembras
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE natusiembras;

CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(100),
    descripcion TEXT,
    propiedades TEXT,
    unidad VARCHAR(30) NOT NULL DEFAULT 'kg',
    precio DECIMAL(10,2) NOT NULL DEFAULT 0,
    stock DECIMAL(10,2) NOT NULL DEFAULT 0,
    imagen VARCHAR(255),
    disponible TINYINT(1) NOT NULL DEFAULT 1,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_nombre VARCHAR(120) NOT NULL,
    telefono VARCHAR(30),
    direccion VARCHAR(255),
    observaciones TEXT,
    total DECIMAL(10,2) NOT NULL DEFAULT 0,
    estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS detalle_pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

INSERT INTO productos
(nombre, categoria, descripcion, propiedades, unidad, precio, stock, imagen)
VALUES
(
 'Tomate',
 'Hortalizas',
 'Tomate fresco cultivado en nuestra finca.',
 'Aporta vitamina C, vitamina A, potasio y licopeno.',
 'kg', 1.80, 100, 'tomate.jpg'
),
(
 'Pepinillo',
 'Hortalizas',
 'Pepinillo fresco, crujiente y de excelente calidad.',
 'Contiene agua, vitamina K y diferentes micronutrientes.',
 'kg', 1.50, 100, 'pepinillo.jpg'
),
(
 'Pimiento',
 'Hortalizas',
 'Pimientos frescos de nuestra finca.',
 'Fuente de vitamina C, vitamina A y antioxidantes.',
 'kg', 2.20, 80, 'pimiento.jpg'
);
