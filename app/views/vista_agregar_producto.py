from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import mysql.connector
import os


agregar_producto_bp = Blueprint('agregar', __name__)


@agregar_producto_bp.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():

    if request.method == 'POST':
        from models.agregar_productos import Producto 

        nombre_producto = request.form['nombre_producto']
        precio_producto = request.form['precio_producto']
        descripcion_producto = request.form['descripcion_producto']
        categoria_id = request.form['categoria_id'].strip()
        stock_producto = request.form['stock_producto']
        producto_img = request.files['producto_img']  # Obtener la imagen del formulario
        producto_img_filename = producto_img.filename  # Obtener el nombre del archivo

        # Ruta donde se guardarán las imágenes
        ruta_imagenes = 'bd/img'

        # Crear la carpeta si no existe
        if not os.path.exists(ruta_imagenes):
            os.makedirs(ruta_imagenes)

        # Guardar la imagen en el servidor
        producto_img.save(os.path.join(ruta_imagenes, producto_img_filename))

        # Verificar si la categoría existe

        conn = mysql.connector.connect(
            host='localhost',  
            user='root',  

            password='',  

            database='miyh'  

        )
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM categorias WHERE categoria_id = %s", (categoria_id,))

        existe_categoria = cursor.fetchone()[0] > 0
        conn.close()


        # Imprimir el valor de categoria_id para depuración

        print(f"categoria_id enviado: {categoria_id}, existe: {existe_categoria}")


        if not existe_categoria:

            # Manejar el error de categoría no existente (puedes redirigir o mostrar un mensaje)

            return jsonify(success=False, error="Error: La categoría no existe."), 400


        # Agregar el producto
        resultado = Producto.agregar_producto(nombre_producto, precio_producto, descripcion_producto, categoria_id, stock_producto, producto_img_filename)

        return resultado  # Devolver la respuesta JSON del método agregar_producto

    

    conn = mysql.connector.connect(

        host='localhost',  

        user='root',  

        password='',  

        database='miyh'  

    )

    cursor = conn.cursor()

    cursor.execute("SELECT nombre_categoria, categoria_id FROM categorias")  # Consulta SQL para obtener categorías

    categorias = cursor.fetchall()  # Obtener todas las categorías

    conn.close()  # Cerrar la conexión


    return render_template('agregar_producto.html', categorias=categorias) 
