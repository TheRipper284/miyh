import mysql.connector
from flask import jsonify

class Producto:
    @staticmethod
    def agregar_producto(nombre, precio, descripcion, categoria_id, stock_producto, producto_img):
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='miyh'
            )
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO productos (nombre_producto, precio_producto, descripcion_producto, categoria_id, stock_producto, producto_img)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, precio, descripcion, categoria_id, stock_producto, producto_img))
            db.commit()
            cursor.close()
            db.close()
            return jsonify(success=True)
        except Exception as e:
            return jsonify(success=False, error=str(e))