from flask import Blueprint, render_template, request, redirect, flash
from models.add_ingrediente import agregar_ingrediente, editar_ingrediente, eliminar_ingrediente
import mysql.connector

views_ingrediente = Blueprint('views_ingrediente', __name__)

# Configuración de la conexión (puede hacerse global o gestionarse por cada función)
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='miyh'
    )

@views_ingrediente.route('/index', methods=['GET'])
def index():
    return render_template('index.html')  # Asegúrate de que este archivo exista

@views_ingrediente.route('/añadir_item', methods=['POST'])
def añadir_item():
    itemId = request.form['itemId']
    categoryId = request.form['categoryId']
    itemName = request.form['itemName']
    supplier = request.form['supplier']

    try:
        # Llamar a la función para agregar el ingrediente
        agregar_ingrediente(itemId, categoryId, itemName, supplier)
        flash("Ingrediente agregado exitosamente.", "success")
    except ValueError as ve:
        flash(str(ve), "error")  # Mensaje para errores de validación
    except mysql.connector.Error as err:
        flash(f"Error de base de datos: {err}", "error")  # Mensaje para errores de base de datos
    except Exception as e:
        flash(f"Error inesperado: {e}", "error")  # Otros errores inesperados

    return redirect('/ingredientes')

@views_ingrediente.route('/editar_item/<int:item_id>', methods=['GET', 'POST'])
def editar_item(item_id):
    if request.method == 'POST':
        categoryId = request.form['categoryId']
        itemName = request.form['itemName']
        supplier = request.form['supplier']

        try:
            # Llamar a la función para editar el ingrediente
            editar_ingrediente(item_id, categoryId, itemName, supplier)
            flash("Ingrediente actualizado exitosamente.", "success")
        except ValueError as ve:
            flash(str(ve), "error")  # Mensaje para errores de validación
        except mysql.connector.Error as err:
            flash(f"Error de base de datos: {err}", "error")  # Mensaje para errores de base de datos
        except Exception as e:
            flash(f"Error inesperado: {e}", "error")  # Otros errores inesperados

        return redirect('/ingredientes')

    # Si es un GET, deberías obtener el ítem y mostrarlo en un formulario
    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM ingredientes WHERE id_ing = %s", (item_id,))
        item = cursor.fetchone()
        
        if item is None:
            flash("Ingrediente no encontrado.", "error")
            return redirect('/ingredientes')

        return render_template('edit_item.html', item=item)
    except mysql.connector.Error as err:
        flash(f"Error al obtener el ingrediente: {err}", "error")
        return redirect('/ingredientes')
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@views_ingrediente.route('/eliminar_item/<int:item_id>', methods=['POST'])
def eliminar_item(item_id):
    try:
        # Llamar a la función para eliminar el ingrediente
        eliminar_ingrediente(item_id)
        flash("Ingrediente eliminado exitosamente.", "success")
    except mysql.connector.Error as err:
        flash(f"Error de base de datos: {err}", "error")  # Mensaje para errores de base de datos
    except Exception as e:
        flash(f"Error inesperado: {e}", "error")  # Otros errores inesperados

    return redirect('/ingredientes')

@views_ingrediente.route('/ingredientes', methods=['GET'])
def ingredientes():
    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Obtener ingredientes
        cursor.execute("SELECT * FROM ingredientes")
        ingredientes = cursor.fetchall()
        
        # Obtener categorías para el modal
        cursor.execute("SELECT * FROM catego_ing")
        categorias = cursor.fetchall()

        return render_template('ingredientes.html', inventario=ingredientes, categorias=categorias)
    except mysql.connector.Error as err:
        print(f"Error al ejecutar la consulta: {err}")
        flash("Error al obtener los ingredientes", "error")
        return "Error al obtener los ingredientes", 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@views_ingrediente.route('/categoria_ing', methods=['GET'])
def categoria_ingre():
    return render_template('categoria_ing.html')  # Asegúrate de que este archivo exista