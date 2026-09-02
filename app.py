from flask import Flask, render_template, jsonify, request
import pymysql

app = Flask(__name__)

# =========================
# CONFIGURACIÓN MYSQL
# =========================
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"
DB_NAME = "natusiembras"


# =========================
# CONEXIÓN MYSQL
# =========================
def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


# =========================
# PÁGINA PRINCIPAL
# =========================
@app.route("/")
def inicio():
    return render_template("index.html")


# =========================
# PÁGINA PRODUCTO
# =========================
@app.route("/producto/<int:producto_id>")
def producto(producto_id):
    return render_template("producto.html", producto_id=producto_id)


# =========================
# PÁGINA PRODUCTOS
# =========================
@app.route("/productos")
def productos():
    conexion = get_connection()

    try:
        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT
                    id,
                    nombre,
                    categoria,
                    descripcion,
                    propiedades,
                    unidad,
                    precio,
                    stock,
                    imagen,
                    disponible
                FROM productos
                WHERE disponible = 1
                ORDER BY nombre
            """)

            datos = cursor.fetchall()

        return render_template(
            "productos.html",
            productos=datos
        )

    except Exception as e:
        return f"Error al consultar productos: {e}"

    finally:
        conexion.close()


# =========================
# API - TODOS LOS PRODUCTOS
# =========================
@app.route("/api/productos")
def api_productos():

    conexion = get_connection()

    try:
        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT
                    id,
                    nombre,
                    categoria,
                    descripcion,
                    propiedades,
                    unidad,
                    precio,
                    stock,
                    imagen,
                    disponible
                FROM productos
                WHERE disponible = 1
                ORDER BY nombre
            """)

            productos = cursor.fetchall()

        return jsonify(productos)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

    finally:
        conexion.close()


# =========================
# API - UN PRODUCTO
# =========================
@app.route("/api/productos/<int:producto_id>")
def api_producto(producto_id):

    conexion = get_connection()

    try:
        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT
                    id,
                    nombre,
                    categoria,
                    descripcion,
                    propiedades,
                    unidad,
                    precio,
                    stock,
                    imagen,
                    disponible
                FROM productos
                WHERE id = %s
                AND disponible = 1
            """, (producto_id,))

            producto = cursor.fetchone()

        if not producto:
            return jsonify({
                "error": "Producto no encontrado"
            }), 404

        return jsonify(producto)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

    finally:
        conexion.close()


# =========================
# REGISTRAR PEDIDO
# =========================
@app.route("/pedido", methods=["POST"])
def pedido():

    data = request.get_json(silent=True) or {}

    cliente = data.get("cliente", {})
    items = data.get("items", [])

    if not items:
        return jsonify({
            "ok": False,
            "mensaje": "El pedido está vacío"
        }), 400

    conexion = get_connection()

    try:

        with conexion.cursor() as cursor:

            cursor.execute("""
                INSERT INTO pedidos
                (
                    cliente_nombre,
                    telefono,
                    direccion,
                    observaciones,
                    total,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, 'Pendiente')
            """, (
                cliente.get("nombre", ""),
                cliente.get("telefono", ""),
                cliente.get("direccion", ""),
                cliente.get("observaciones", ""),
                data.get("total", 0)
            ))

            pedido_id = cursor.lastrowid

            for item in items:

                cursor.execute("""
                    INSERT INTO detalle_pedido
                    (
                        pedido_id,
                        producto_id,
                        cantidad,
                        precio,
                        subtotal
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    pedido_id,
                    item["id"],
                    item["cantidad"],
                    item["precio"],
                    item["subtotal"]
                ))

        return jsonify({
            "ok": True,
            "pedido_id": pedido_id,
            "mensaje": "Pedido registrado correctamente"
        })

    except Exception as e:

        return jsonify({
            "ok": False,
            "mensaje": str(e)
        }), 500

    finally:
        conexion.close()


# =========================
# MANIFEST
# =========================
@app.route("/manifest.json")
def manifest():
    return app.send_static_file("manifest.json")


# =========================
# INICIAR SERVIDOR
# =========================
if __name__ == "__main__":
    app.run(debug=True)