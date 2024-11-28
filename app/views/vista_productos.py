from flask import Blueprint, render_template, request, send_from_directory
import mysql.connector

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos', methods=['GET'])
def vista_productos():
    # Conexión a la base de datos
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='miyh'
    )
    cursor = db.cursor()

    # Obtener categorías para el filtro
    cursor.execute("SELECT DISTINCT nombre_categoria FROM categorias;")
    categorias = cursor.fetchall()

    # Inicializar la consulta
    query = """
    SELECT p.id_producto, p.nombre_producto, p.precio_producto, p.descripcion_producto, 
           p.stock_producto, c.nombre_categoria, p.producto_img 
    FROM productos p 
    JOIN categorias c ON p.categoria_id = c.categoria_id
    """
    filters = []
    
    # Filtrar por categoría
    categoria = request.args.get('categoria')
    if categoria:
        filters.append(f"c.nombre_categoria = '{categoria}'")

    # Filtrar por stock
    stock = request.args.get('stock')
    if stock:
        if stock == 'mayor':
            filters.append("p.stock_producto > 20")  
        elif stock == 'menor':
            filters.append("p.stock_producto <= 6") 

    # Añadir filtros a la consulta
    if filters:
        query += " WHERE " + " AND ".join(filters)

    # Ejecutar la consulta
    cursor.execute(query)
    productos = cursor.fetchall()

    # Cerrar la conexión
    cursor.close()
    db.close()

    return render_template('productos.html', productos=productos, categorias=categorias)

@productos_bp.route('/bd/img/<path:filename>')
def serve_image(filename):
    return send_from_directory('bd/img', filename)