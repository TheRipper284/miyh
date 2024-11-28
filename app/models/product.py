import mysql.connector

# Función para obtener la conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',  # Cambia esto si tu base de datos está en otro host
        user='root',  # Cambia esto por tu usuario de base de datos
        password='',  # Cambia esto por tu contraseña de base de datos
        database='miyh'  # Cambia esto por el nombre de tu base de datos
    )

# Función para obtener un producto por su ID
def get_product_by_id(product_id):
    db = get_db_connection()  # Obtener la conexión a la base de datos
    cursor = db.cursor(dictionary=True)

    query = "SELECT id_producto, nombre_producto, descripcion_producto, precio_producto, stock_producto, producto_img FROM productos WHERE id_producto = %s"
    cursor.execute(query, (product_id,))
    product = cursor.fetchone()

    cursor.close()  # Cerrar el cursor
    db.close()  # Cerrar la conexión a la base de datos
    return product

# Función para actualizar un producto
# Función para actualizar un producto
def update_product(product_id, nombre, descripcion, precio, stock, producto_img=None):
    db = get_db_connection()  # Obtener la conexión a la base de datos
    cursor = db.cursor()

    query = """
        UPDATE productos
        SET nombre_producto = %s, descripcion_producto = %s, precio_producto = %s, stock_producto = %s,
        producto_img = COALESCE(%s, producto_img)
        WHERE id_producto = %s
    """

    cursor.execute(query, (nombre, descripcion, precio, stock, producto_img, product_id))
    db.commit()
    cursor.close()  # Cerrar el cursor
    db.close()

# Función para eliminar un producto
def delete_product(product_id):
    db = get_db_connection()  # Obtener la conexión a la base de datos
    cursor = db.cursor()

    query = "DELETE FROM productos WHERE id_producto = %s"
    cursor.execute(query, (product_id,))
    db.commit()

    cursor.close()  # Cerrar el cursor
    db.close()  # Cerrar la conexión a la base de datos