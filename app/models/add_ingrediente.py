import os
import mysql.connector
from flask import request, current_app

def agregar_ingrediente(itemId, categoryId, itemName, supplier):
    """Agrega un nuevo ingrediente a la tabla ingredientes."""
    try:
        # Conexión a la base de datos
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='miyh'
        )
        cursor = db.cursor()
        print("Conexión a la base de datos establecida.")
        
        # Verificar si la categoría existe
        cursor.execute("SELECT categoria_ing FROM catego_ing WHERE categoria_id = %s", (categoryId,))
        result = cursor.fetchone()
        print(result)

        if result is None:
            raise ValueError(f"La categoría con ID {categoryId} no existe.")  # Lanzar una excepción si no existe

        # Manejo del archivo de imagen
        if 'image' not in request.files:
            raise ValueError("No se ha subido ninguna imagen.")
        
        image_file = request.files['image']
        if image_file.filename == '':
            raise ValueError("No se ha seleccionado ninguna imagen.")
        
        # Guardar la imagen en el directorio deseado
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path)

        # Insertar el nuevo ingrediente en la base de datos
        query = "INSERT INTO ingredientes (id_ing, categoria_ing, nombre, proveedor, imagen) VALUES (%s, %s, %s, %s, %s)"
        values = (itemId, result[0], itemName, supplier, image_path)
        cursor.execute(query, values)
        db.commit()  # Confirmar los cambios
        print("Ingrediente agregado exitosamente.")

    except mysql.connector.Error as err:
        print(f"Error al interactuar con la base de datos: {err}")
        raise  # Propagar el error para que Flask pueda manejarlo
    except ValueError as ve:
        print(ve)
        raise  # Propagar el error para que Flask pueda manejarlo
    finally:
        # Cerrar la conexión a la base de datos
        if cursor:
            cursor.close()
        if db:
            db.close()
        print("Conexión a la base de datos cerrada.")

def editar_ingrediente(itemId, categoryId, itemName, supplier):
    """Edita un ingrediente existente en la tabla ingredientes."""
    try:
        # Conexión a la base de datos
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='miyh'
        )
        cursor = db.cursor()
        print("Conexión a la base de datos establecida.")

        # Verificar si la categoría existe
        cursor.execute("SELECT categoria_ing FROM catego_ing WHERE categoria_id = %s", (categoryId,))
        result = cursor.fetchone()
        print(result)

        if result is None:
            raise ValueError(f"La categoría con ID {categoryId} no existe.")  # Lanzar una excepción si no existe

        # Manejo del archivo de imagen (opcional)
        image_path = None
        if 'image' in request.files and request.files['image'].filename != '':
            image_file = request.files['image']
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_file.filename)
            image_file.save(image_path)

        # Actualizar el ingrediente en la base de datos
        if image_path:
            query = "UPDATE ingredientes SET categoria_ing = %s, nombre = %s, proveedor = %s, imagen = %s WHERE id_ing = %s"
            values = (result[0], itemName, supplier, image_path, itemId)
        else:
            query = "UPDATE ingredientes SET categoria_ing = %s, nombre = %s, proveedor = %s WHERE id_ing = %s"
            values = (result[0], itemName, supplier, itemId)

        cursor.execute(query, values) 
        db.commit()  # Confirmar los cambios
        print("Ingrediente actualizado exitosamente.")

    except mysql.connector.Error as err:
        print(f"Error al interactuar con la base de datos: {err}")
        raise  # Propagar el error para que Flask pueda manejarlo
    except ValueError as ve:
        print(ve)
        raise  # Propagar el error para que Flask pueda manejarlo
    finally:
        # Cerrar la conexión a la base de datos
        if cursor:
            cursor.close()
        if db:
            db.close()
        print("Conexión a la base de datos cerrada.")

def eliminar_ingrediente(itemId):
    """Elimina un ingrediente de la tabla ingredientes."""
    try:
        # Conexión a la base de datos
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='miyh'
        )
        cursor = db.cursor()
        print("Conexión a la base de datos establecida.")

        # Eliminar el ingrediente de la base de datos
        query = "DELETE FROM ingredientes WHERE id_ing = %s"
        cursor.execute(query, (itemId,))
        db.commit()  # Confirmar los cambios
        print("Ingrediente eliminado exitosamente.")

    except mysql.connector.Error as err:
        print(f"Error al interactuar con la base de datos: {err}")
        raise  # Propagar el error para que Flask pueda manejarlo
    finally:
        # Cerrar la conexión a la base de datos
        if cursor:
            cursor.close()
        if db:
            db.close()
        print("Conexión a la base de datos cerrada.")