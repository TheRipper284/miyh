from flask import Blueprint, render_template, request, redirect, url_for, session
from models.product import get_product_by_id, update_product, delete_product
import os
from flask import current_app
from werkzeug.utils import secure_filename

# Crear un Blueprint para editar productos
edit_product_bp = Blueprint('edit_product', __name__)

@edit_product_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    # Verificar si el usuario está autenticado
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Obtener los datos del producto para mostrar en el formulario
    product = get_product_by_id(id)
    if not product:
        return "Producto no encontrado", 404

    if request.method == 'POST':
        # Obtener datos del formulario
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        stock = request.form['stock']
        image_filename = product['producto_img']  # Mantener la imagen existente por defecto

        if 'image' in request.files and request.files['image'].filename != '':
            image = request.files['image']  
            filename = secure_filename(image.filename)
            # Guardar la imagen en la carpeta bd/img
            ruta_imagenes = 'bd/img'
            image.save(os.path.join(ruta_imagenes, filename))
            image_filename = filename  # Actualizar solo si hay una nueva imagen
        
        # Actualizar el producto
        update_product(id, name, description, price, stock, image_filename)
        return redirect(url_for('productos.vista_productos'))

    return render_template('edit_product.html', product=product, product_id=id)

@edit_product_bp.route('/delete/<int:id>', methods=['POST'])
def delete_product_route(id):
    # Verificar si el usuario está autenticado
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Eliminar el producto
    delete_product(id)
    return redirect(url_for('productos.vista_productos'))