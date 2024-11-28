from flask import Blueprint, render_template, request, redirect
from models.add_categoria_ing import agregar_categoria_ing

views_categoria_ing = Blueprint('views_categoria_ing', __name__)

@views_categoria_ing.route('/categoria_ing', methods=['GET'])
def categoria_ingre():
    return render_template('categoria_ing.html')  # Asegúrate de que este archivo exista

@views_categoria_ing.route('/añadir_categoria', methods=['POST'])
def añadir_categoria():
    categoria_ing = request.form['categoria_ing']

    # Llamar a la función para agregar la nueva categoría
    agregar_categoria_ing(categoria_ing)

    return redirect('/ingredientes')  # Redirigir a la página de ingredientes después de agregar