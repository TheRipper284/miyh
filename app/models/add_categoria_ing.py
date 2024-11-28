import mysql.connector

def agregar_categoria_ing(categoria_ing):
    # Conexión a la base de datos
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='miyh'
        )
        cursor = db.cursor()
        print("Conexión a la base de datos establecida.")
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return

    # Insertar la nueva categoría en la base de datos
    query = "INSERT INTO catego_ing(categoria_ing) VALUES (%s)"
    values = (categoria_ing,)
    
    try:
        cursor.execute(query, values)
        db.commit()  # Asegúrate de confirmar los cambios en la base de datos
        print("Categoría agregada exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error al agregar la categoría: {err}")
        db.rollback()  # Deshacer cambios en caso de error
    finally:
        cursor.close()
        db.close()
        print("Conexión a la base de datos cerrada.")
