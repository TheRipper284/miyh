import os
from unicodedata import category
from flask import Flask, jsonify, redirect, render_template, request, session
import mysql.connector
from views.vista_principal import principal 
from views.vista_productos import productos_bp
from views.vista_agregar_producto import agregar_producto_bp
from views.edit_product import edit_product_bp
from views.views_categoria_ing import views_categoria_ing
from views.views_ingrediente import views_ingrediente
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Configuración de la base de datos
def get_db_connection():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='miyh'
    )
    return db

db = get_db_connection()
cursor = db.cursor()

app.secret_key = 'mi_clave'
app.register_blueprint(principal) 
app.register_blueprint(productos_bp) 
app.register_blueprint(agregar_producto_bp) 
app.register_blueprint(edit_product_bp)
app.register_blueprint(views_categoria_ing)
app.register_blueprint(views_ingrediente)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT id, user_name, password FROM users WHERE user_name = %s", (username,))
        user = cursor.fetchone()

        
        if user and user[2] == password: 
            session['user_id'] = user[0] 
            return redirect('index')  

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/categorias')
def home():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT categoria_id, nombre_categoria, descripcion_categoria, habilitado, imagen_categoria FROM Categorias")
    categories = cursor.fetchall()
    db.close()
    return render_template('editar.html', categories=categories)

@app.route('/add', methods=['POST'])
def add_category():
    data = request.form
    name = data.get('name')
    description = data.get('description', "")
    image = request.files.get('image')

    # Validar nombre
    if not name:
        return jsonify({'success': False, 'message': 'El nombre de la categoría es requerido'})

    # Guardar la imagen (si existe)
    if image and allowed_file(image.filename):
        image_filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        image.save(image_path)
        
        print(f"Imagen guardada: {image_filename}")
    # Opcional: Elimina la imagen anterior para evitar archivos huérfanos
    if category[4]:  # category[4] contiene el nombre de la imagen anterior
        old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], category[4])
        if os.path.exists(old_image_path):
            os.remove(old_image_path)

    db = get_db_connection()
    cursor = db.cursor()

    # Insertar nueva categoría con la imagen y descripción
    cursor.execute("""
    UPDATE Categorias 
    SET nombre_categoria = %s, descripcion_categoria = %s, imagen_categoria = %s 
    WHERE categoria_id = %s
""", (name, description, image_filename, category_id))
    db.commit()
    category_id = cursor.lastrowid
    db.close()

    return jsonify({'success': True, 'category': {'id': category_id, 'name': name, 'description': description, 'habilitado': True, 'imagen': image_filename}})

@app.route('/edit/<int:category_id>', methods=['PUT'])
@app.route('/edit/<int:category_id>', methods=['PUT'])
def edit_category(category_id):
    data = request.form
    name = data.get('name')
    description = data.get('description', "")
    image = request.files.get('image')

    if name:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM Categorias WHERE categoria_id = %s", (category_id,))
        category = cursor.fetchone()

        if category:
            # Mantener la imagen actual si no se sube una nueva
            image_filename = category[4]
            if image and allowed_file(image.filename):
                image_filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image.save(image_path)

                # Eliminar la imagen anterior si existe
                if category[4]:  # El nombre de la imagen anterior
                    old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], category[4])
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

            cursor.execute("""
                UPDATE Categorias 
                SET nombre_categoria = %s, descripcion_categoria = %s, imagen_categoria = %s 
                WHERE categoria_id = %s
            """, (name, description, image_filename, category_id))
            db.commit()
            db.close()

            return jsonify({'success': True, 'category': {'id': category_id, 'name': name, 'description': description, 'imagen': image_filename}})
        else:
            db.close()
            return jsonify({'success': False, 'message': 'Categoría no encontrada'}), 404

    return jsonify({'success': False, 'message': 'El nombre de la categoría es requerido'})


@app.route('/delete/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    # Deshabilitar la categoría (no eliminarla realmente de la base de datos)
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE Categorias SET habilitado = FALSE WHERE categoria_id = %s", (category_id,))
    db.commit()
    db.close()
    return jsonify({'success': True})

@app.route('/description/<int:category_id>', methods=['GET'])
def get_description(category_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT descripcion_categoria FROM Categorias WHERE categoria_id = %s", (category_id,))
    description = cursor.fetchone()
    db.close()

    if description:
        return jsonify({'success': True, 'description': description[0]})
    return jsonify({'success': False, 'message': 'Categoría no encontrada'})





if __name__ == '__main__':
    app.run(debug=True)