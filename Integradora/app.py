from flask import Flask, make_response, redirect, url_for, render_template, session, request, jsonify, Response
from sqlalchemy import create_engine, text
from functools import wraps
#Se eliminara pero es para hacer pruebas
import time

app = Flask(__name__)

# Establecer la clave secreta
app.secret_key = '12345'  # Cambia esto por una clave única

#Conexión
engine = None

##Decorador de Autorización
def login_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'permiso_usuario' not in session:
                return redirect(url_for('inicio_usuario'))
            if session['permiso_usuario'] != role:
                return redirect(url_for('/')) 
            return f(*args, **kwargs)
        return wrapped
    return decorator

#Función para iniciar la base de datos
def init_db():
    global engine
    if engine is None:
        engine = create_engine('mysql+pymysql://root:@localhost/integradora')
        #mysql+pymysql://<usuario>:<contraseña>@<host>/<nombre_base_de_datos>
        #Manuel
        #mysql+pymysql://root:'pass123'@localhost/integradora
        #Mario
        #mysql+pymysql://root:@localhost/integradora

#Funciones a llamar desde la web#####################################################################################################
@app.route('/check_session', methods=['GET'])
def check_session():
    if 'permiso_usuario' in session:
        return jsonify({"status": "active"}), 200
    return jsonify({"status": "inactive"}), 401

@app.route('/api/contactos')
def contactos():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text("SELECT contacts.Facebook, contacts.Instagram, contacts.Tik_tok, contacts.Email, contacts.Twitter, contacts.Whatsapp, contacts.Phone FROM contacts;"))
            contactos = result.fetchall()
            nombre_columnas = result.keys()
            html = ""

            for redes in contactos:
                html += '<div class="contacto_contenedor">'
                for url, nombre in zip(redes, nombre_columnas):
                    if url:
                        html += f"""
                        <div class="elementos">
                            <a href="{url}">
                                <img src="static/image/{nombre}.svg" alt="{nombre}" class="{nombre}">
                            </a>
                        </div>
                        """
                html += '</div><hr>'

            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

@app.route('/api/texto_vision_mision')
def texto_mision_vision():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text('SELECT content.Title, content.Describe FROM content WHERE content.Title!="Valores" AND content.Title!="Mision" AND content.Title!="Vision";'))
            contenido = result.fetchall()
            html = ""

            for titulo, descripcion in contenido:
                html += '<div class="valores_derechos">'
                html += f"""
                    <h2>{titulo}</h2>
                    <p>{descripcion}</p> 
                """
                html += '</div><br>'

            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

@app.route('/api/texto_valores')
def texto_valores():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text('SELECT content.Title, content.Describe FROM content WHERE content.Title="Valores" OR content.Title="Misión" OR content.Title="Visión";'))
            contenido = result.fetchall()
            html = ""

            for titulo, descripcion in contenido:
                html += '<div class="valores_derechos">'
                html += f"""
                    <h2>{titulo}</h2>
                    <p>{descripcion}</p> 
                """
                html += '</div><br>'

            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

@app.route('/api/mostrador_productos')
def mostrador_productos():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text('SELECT products.url_imagen, products.Name, products.Color, products.Price_per_unit FROM products;'))
            contenido = result.fetchall()
            
            html = ""

            for info in contenido:
                direccion_imagen= url_for('static', filename=f'image/imagenes_productos/{info[0]}', _external=True)
                html += f"""
                        <div class="producto">
                            <a href="">
                                <div id="imagen">
                                    <img src="{direccion_imagen}" alt="{info[0]}">
                                </div>
                                <div id="info">
                                    <h3 id="nombre-producto">{info[1]}</h3>
                                    <p id="color-modelo">{info[2]}</p>
                                    <strong id="precio">${info[3]}</strong>
                                </div>
                            </a>
                        </div>
                """

            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

#Tablas
@app.route('/api/tabla_productos')
def tabla_productos():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text('SELECT products.Name, products.Model, products.Size, products.Material_composition, products.Price_per_unit, products.Color, products.Id_product FROM products;'))
            contenido = result.fetchall()
            
            html = """
            <table>
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th>Modelo</th>
                        <th>Tamaño</th>
                        <th>Material de composisión</th>
                        <th>Precio</th>
                        <th>Color</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
            """
            for info in contenido:
                html += f"""
                    <tr>
                        <td>{info[0]}</td>
                        <td>{info[1]}</td>
                        <td>{info[2]}</td>
                        <td>{info[3]}</td>
                        <td>{info[4]}</td>
                        <td>{info[5]}</td>
                        <td>
                            <button onclick="detallesProducto({info[6]})" class="detalles">Detalles</button>
                            <button onclick="editarProducto({info[6]})" class="editar">Editar</button>
                            <button onclick="eliminarProducto({info[6]})" class="eliminar">Eliminar</button>
                        </td>
                    </tr>
                    
                """

            html += """
                </tbody>
            </table>
            """
            
            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

@app.route('/api/tabla_season_specification')
def tabla_season_specification	():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text('SELECT season_specification.season, season_specification.Id_season FROM season_specification;'))
            contenido = result.fetchall()
            
            html = """
            <table>
                <thead>
                    <tr>
                        <th>Temporada</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
            """
            for info in contenido:
                html += f"""
                    <tr>
                        <td>{info[0]}</td>
                        <td>
                            <button onclick="editarProducto({info[1]})" class="editar">Editar</button>
                            <button onclick="eliminarProducto({info[1]})" class="eliminar">Eliminar</button>
                        </td>
                    </tr>
                    
                """

            html += """
                </tbody>
            </table>
            """
            
            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

@app.route('/api/tabla_contact')
def tabla_contact():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text('SELECT contacts.Facebook, contacts.Instagram, contacts.Tik_tok, contacts.Email, contacts.Twitter, contacts.Whatsapp, contacts.Phone, contacts.Id_contact FROM contacts;'))
            contenido = result.fetchall()
            html = ""
            if contenido:
                for info in contenido:
                    html += f"""
                    <h2>
                        Facebook
                    </h2>
                    <h3>
                        {info[0]}
                    </h3>
                    <br>
                    <h2>
                        Instagra
                    </h2>
                    <h3>
                        {info[1]}
                    </h3>
                    <br>
                    <h2>
                        Tik Tok
                    </h2>
                    <h3>
                        {info[2]}
                    </h3>
                    <br>
                    <h2>
                        Email
                    </h2>
                    <h3>
                        {info[3]}
                    </h3>
                    <br>
                    <h2>
                        Twitter
                    </h2>
                    <h3>
                        {info[4]}
                    </h3>
                    <br>
                    <h2>
                        Whatsapp
                    </h2>
                    <h3>
                        {info[5]}
                    </h3>
                    <br>
                    <h2>
                        Telefono
                    </h2>
                    <h3>
                        {info[6]}
                    </h3>
                    <br>
                    <h2>
                        Acciones
                    </h2>
                        <button onclick="editarProducto({info[7]})" class="editar">Editar</button>
                        <button onclick="eliminarProducto({info[7]})" class="eliminar">Eliminar</button>
                    """
            else:
                html += f"""
                    <div class="arriba">
                        <button id="abrirModal" onclick="abrirModal()">Registrar</button>
                    </div>
                    """
            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

@app.route('/api/tabla_content')
def tabla_content():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text('SELECT content.Title, content.Describe, content.Id_contenido FROM content;'))
            contenido = result.fetchall()
            
            html = ""
            for info in contenido:
                html += f"""
                    <div class="content" onclick="toggleExpand(event, this)">
                        <h2>{info[0]}</h2>
                        <p>{info[1]}</p>
                        <button onclick="editarProducto({info[2]})" class="editar">Editar</button>
                        <button onclick="eliminarProducto({info[2]})" class="eliminar">Eliminar</button>
                    </div>
                """
            
            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

@app.route('/api/tabla_users')
def tabla_users():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text('SELECT users.User, users.Email, users.Name, users.Surname, users.Lastname, users.Rol, users.Id_user FROM users;'))
            contenido = result.fetchall()
            
            html = """
            <table>
                <thead>
                    <tr>
                        <th>Usuario</th>
                        <th>Correo</th>
                        <th>Nombre</th>
                        <th>Apellido paterno</th>
                        <th>Apellido Materno</th>
                        <th>Rol</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
            """
            for info in contenido:
                html += f"""
                    <tr>
                        <td>{info[0]}</td>
                        <td>{info[1]}</td>
                        <td>{info[2]}</td>
                        <td>{info[3]}</td>
                        <td>{info[4]}</td>
                        <td>{info[5]}</td>
                        <td>
                            <button onclick="editarProducto({info[6]})" class="editar">Editar/Más detalles</button>
                            <button onclick="eliminarProducto({info[6]})" class="eliminar">Eliminar</button>
                        </td>
                    </tr>
                    
                """

            html += """
                </tbody>
            </table>
            """
            
            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

@app.route('/api/contenido_inicio_administracion')
def contenido_inicio_administracion():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text('SELECT content.Title, content.Describe, content.Id_contenido FROM content;'))
            contenido = result.fetchall()
            
            html = "Proximamente"
            '''
            for info in contenido:
                html += f"""
                    <div class="content" onclick="toggleExpand(event, this)">
                        <h2>{info[0]}</h2>
                        <p>{info[1]}</p>
                        <button onclick="editarProducto({info[2]})" class="editar">Editar</button>
                        <button onclick="eliminarProducto({info[2]})" class="eliminar">Eliminar</button>
                    </div>
                """
            '''
            
            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

#Buscador tablas
@app.route('/api/buscador_content', methods=['POST'])
def buscador_content():
    informacion = request.get_json()
    buscar = informacion.get('buscar', '')

    try:
        init_db()
        with engine.connect() as connection:
            
            sql_query = """
                SELECT content.Title, content.Describe, content.Id_contenido 
                FROM content 
                WHERE content.Title LIKE :buscar OR content.Describe LIKE :buscar
            """
            result = connection.execute(text(sql_query), {"buscar": f"%{buscar}%"})
            contenido = result.fetchall()

            # Construcción de la tabla HTML con los resultados
            html = ""
            for info in contenido:
                html += f"""
                    <div class="content" onclick="toggleExpand(event, this)">
                        <h2>{info[0]}</h2>
                        <p>{info[1]}</p>
                        <button onclick="editarProducto({info[2]})" class="editar">Editar</button>
                        <button onclick="eliminarProducto({info[2]})" class="eliminar">Eliminar</button>
                    </div>
                """
            
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')

@app.route('/api/buscador_season', methods=['POST'])
def buscador_season():
    informacion = request.get_json()
    buscar = informacion.get('buscar', '')

    try:
        init_db()
        with engine.connect() as connection:
            
            sql_query = """
                SELECT season_specification.season, season_specification.Id_season FROM season_specification 
                WHERE season_specification.season LIKE :buscar;
            """
            result = connection.execute(text(sql_query), {"buscar": f"%{buscar}%"})
            contenido = result.fetchall()

            # Construcción de la tabla HTML con los resultados
            html = """
            <table>
                <thead>
                    <tr>
                        <th>Temporada</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
            """
            for info in contenido:
                html += f"""
                    <tr>
                        <td>{info[0]}</td>
                        <td>
                            <button onclick="editarProducto({info[1]})" class="editar">Editar</button>
                            <button onclick="eliminarProducto({info[1]})" class="eliminar">Eliminar</button>
                        </td>
                    </tr>
                    
                """

            html += """
                </tbody>
            </table>
            """
            
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')

@app.route('/api/buscador_users', methods=['POST'])
def buscador_users():
    informacion = request.get_json()
    buscar = informacion.get('buscar', '')
    
    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT users.User, users.Email, users.Name, users.Surname, users.Lastname, users.Rol, users.Id_user
                FROM users
                WHERE users.User LIKE :buscar
                OR users.Email LIKE :buscar
                OR users.Name LIKE :buscar
                OR users.Surname LIKE :buscar
                OR users.Lastname LIKE :buscar
                OR users.Rol LIKE :buscar
                OR users.Estado LIKE :buscar;
            """
            result = connection.execute(text(sql_query), {"buscar": f"%{buscar}%"})
            contenido = result.fetchall()
            
            html = """
            <table>
                <thead>
                    <tr>
                        <th>Usuario</th>
                        <th>Correo</th>
                        <th>Nombre</th>
                        <th>Apellido paterno</th>
                        <th>Apellido Materno</th>
                        <th>Rol</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
            """
            for info in contenido:
                html += f"""
                    <tr>
                        <td>{info[0]}</td>
                        <td>{info[1]}</td>
                        <td>{info[2]}</td>
                        <td>{info[3]}</td>
                        <td>{info[4]}</td>
                        <td>{info[5]}</td>
                        <td>
                            <button onclick="editarProducto({info[6]})" class="editar">Editar/Más detalles</button>
                            <button onclick="eliminarProducto({info[6]})" class="eliminar">Eliminar</button>
                        </td>
                    </tr>
                    
                """

            html += """
                </tbody>
            </table>
            """
            
            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

@app.route('/api/buscador_productos', methods=['POST'])
def buscador_productos():
    informacion = request.get_json()
    buscar = informacion.get('buscar', '')
    
    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT products.Name, products.Model, products.Size, products.Material_composition, products.Price_per_unit, products.Color, products.Id_product FROM products
                INNER JOIN season_specification ON products.FK_id_season=season_specification.Id_season INNER JOIN users ON products.FK_Id_user=users.Id_user
                WHERE 
                    products.Model LIKE :buscar OR
                    season_specification.season LIKE :buscar OR
                    products.Size LIKE :buscar OR
                    products.Name LIKE :buscar OR
                    products.Description LIKE :buscar OR
                    products.Price_per_unit LIKE :buscar OR
                    products.Color LIKE :buscar OR
                    users.User LIKE :buscar;
            """
            result = connection.execute(text(sql_query), {"buscar": f"%{buscar}%"})
            contenido = result.fetchall()
            
            html = """
            <table>
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th>Modelo</th>
                        <th>Tamaño</th>
                        <th>Material de composisión</th>
                        <th>Precio</th>
                        <th>Color</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
            """
            for info in contenido:
                html += f"""
                    <tr>
                        <td>{info[0]}</td>
                        <td>{info[1]}</td>
                        <td>{info[2]}</td>
                        <td>{info[3]}</td>
                        <td>{info[4]}</td>
                        <td>{info[5]}</td>
                        <td>
                            <button onclick="editarProducto({info[6]})" class="detalles">Detalles</button>
                            <button onclick="editarProducto({info[6]})" class="editar">Editar</button>
                            <button onclick="eliminarProducto({info[6]})" class="eliminar">Eliminar</button>
                        </td>
                    </tr>
                    
                """

            html += """
                </tbody>
            </table>
            """
            
            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

#Registros
@app.route('/registro_usuario', methods=['POST'])
def signup():
    init_db()

    data = request.get_json()
    name = data.get('name')
    lastname = data.get('lastname')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    surname = data.get('surname')

    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                INSERT INTO users (User, Password, Email, Name, Surname, Lastname, Rol, Estado)
                VALUES (:username, :password, :email, :name, :surname, :lastname, 'cliente', 'Activo')
            """
            print(f"Ejecutando consulta: {sql_query}")

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "username": username,
                "password": password,
                "email": email,
                "name": name,
                "surname": surname,
                "lastname": lastname
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Registro exitoso"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al registrar: {str(e)}"}), 500

@app.route('/registrar_contenido', methods=['POST'])
def registrar_contenido():
    init_db()

    data = request.get_json()
    titulo = data.get('titulo')
    descripcion = data.get('descripcion')

    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                INSERT INTO `content` (`Title`, `Describe`)
                VALUES (:titulo, :descripcion);
            """
            print(f"Ejecutando consulta: {sql_query}")

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "titulo": titulo,
                "descripcion": descripcion
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Registro exitoso"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al registrar: {str(e)}"}), 500

@app.route('/registrar_season', methods=['POST'])
def registrar_season():
    init_db()

    data = request.get_json()
    temporada = data.get('temporada')

    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                INSERT INTO `season_specification` (`season`) VALUES (:temporada);
            """

            # Ejecutar la consulta con los datos
            connection.execute(text(sql_query), {
                "temporada": temporada
            })

            # Confirmar la transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Registro exitoso"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al registrar: {str(e)}"}), 500

#ruta para guardar las imagenes subidas
app.config['UPLOAD_FOLDER'] = 'static/image/imagenes_productos' 

@app.route('/registrar_producto', methods=['POST'])
def registrar_producto():
    init_db()

    # Captura los datos del formulario
    modelo = request.form.get('modelo')
    temporada = request.form.get('temporada')
    tamaño = request.form.get('tamaño')
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio_lot = request.form.get('precio_lot')
    color = request.form.get('color')
    materia = request.form.get('materia')
    

    try:
        with engine.connect() as connection:
            #Guarda la imagen
            image = request.files.get('image')
            
            unique_filename = f"{modelo}.png"

            image_path = f"{app.config['UPLOAD_FOLDER']}/{unique_filename}"
            
            image.save(image_path)

            #image_url = url_for('static', filename=f'image/imagenes_productos/{unique_filename}', _external=True)
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
            INSERT INTO `products` (`Material_composition`, `Model`, `FK_id_season`, `Size`, `Name`, `Description`, `Price_per_unit`, `Color`, `url_imagen`, `FK_Id_user`) 
            VALUES (:materia, :modelo, :temporada, :tamaño, :nombre, :descripcion, :precio_lot, :color, :image_url, :user);
            """

            # Ejecutar la consulta con los datos
            connection.execute(text(sql_query), {
                "temporada": temporada,
                "tamaño": tamaño,
                "nombre": nombre,
                "descripcion": descripcion,
                "precio_lot": precio_lot,
                "color": color,
                "materia": materia, 
                "image_url": unique_filename,
                "modelo":modelo,
                "user":session['id_usuario']
            })

            # Confirmar la transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Registro exitoso"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al registrar: {str(e)}"}), 500
    
    # evuelve la respuesta con la URL de la imagen
    #return jsonify({"message": f"Imagen guardada exitosamente. URL:{image_url}"}), 200

#Eliminación
@app.route('/eliminar_season', methods=['POST'])
def eliminar_season():
    init_db()

    identificador = request.get_json()
    id = identificador.get('parametro')
    
    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                DELETE FROM season_specification WHERE `season_specification`.`Id_season` = :identificados;
            """
            print(f"Ejecutando consulta: {sql_query}")

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "identificados": id
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Eliminacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al eliminar: {str(e)}"}), 500

@app.route('/eliminar_usuarios', methods=['POST'])
def eliminar_usuarios():
    init_db()

    identificador = request.get_json()
    id = identificador.get('parametro')
    
    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                DELETE FROM users WHERE `users`.`Id_user`=:identificados;
            """
            print(f"Ejecutando consulta: {sql_query}")

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "identificados": id
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Eliminacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al eliminar: {str(e)}"}), 500

@app.route('/eliminar_contenido', methods=['POST'])
def eliminar_contenido():
    init_db()

    identificador = request.get_json()
    id = identificador.get('parametro')
    
    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                DELETE FROM content WHERE `content`.`Id_contenido`=:identificados;
            """
            print(f"Ejecutando consulta: {sql_query}")

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "identificados": id
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Eliminacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al eliminar: {str(e)}"}), 500

@app.route('/eliminar_contacto', methods=['POST'])
def eliminar_contacto():
    init_db()

    identificador = request.get_json()
    id = identificador.get('parametro')
    
    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                DELETE FROM contacts WHERE `contacts`.`Id_contact` =:identificados;
            """
            print(f"Ejecutando consulta: {sql_query}")

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "identificados": id
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Eliminacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al eliminar: {str(e)}"}), 500

@app.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    init_db()

    identificador = request.get_json()
    id = identificador.get('parametro')
    
    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                DELETE FROM products WHERE `products`.`Id_product` =:identificados;
            """
            print(f"Ejecutando consulta: {sql_query}")

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "identificados": id
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Eliminacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al eliminar: {str(e)}"}), 500

#Solicitar datos para edición
@app.route('/api/buscador_content_edit', methods=['POST'])
def buscador_content_edit():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT content.Title, content.Describe, content.Id_contenido 
                FROM content 
                WHERE content.Id_contenido=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            html = f"""
            <span class="cerrar" onclick="cerrarModal()">&times;</span>
            <h1>Edición de contenido</h1>
            <br>
            <label for="titulo">
                <h2>Titulo</h2>
                <br>
                <input type="text" id="tituloedit" placeholder="Titulo" value="{contenido[0]}">
            </label>
            <br>
            <label for="descripcion">
                <h2>Descripción</h2>
                <br>
                <textarea name="descripcion" id="descripcionedit" placeholder="Descripcion">{contenido[1]}</textarea>
            </label>
            <br>
            <button id="registrar" onclick="editarsqlcontenido({contenido[2]})">Actualizar</button>
            """
            
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')

@app.route('/api/buscador_contacto_edit', methods=['POST'])
def buscador_contacto_edit():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT contacts.Facebook, contacts.Instagram, contacts.Tik_tok, contacts.Email, contacts.Twitter, contacts.Whatsapp, contacts.Phone, contacts.Id_contact FROM contacts WHERE contacts.Id_contact=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            html = f"""
                <span class="cerrar">&times;</span>
            <h1>
                Editar Contactos
            </h1>
            <br>
            <div id="formulario_contactos">
                <div id="izquierda">
                    <label for="Facebook">
                        <h2>
                            Facebook
                        </h2>
                        <br>
                        <input type="text" id="Facebookd" placeholder="Facebook" value="{contenido[0]}">
                    </label>
                    <br>
                    <label for="Instagram">
                        <h2>
                            Instagram
                        </h2>
                        <br>
                        <input type="text" id="Instagramd" placeholder="Instagram" value="{contenido[1]}">
                    </label>
                    <br>
                    <label for="Tik_Tok">
                        <h2>
                            Tik Tok
                        </h2>
                        <br>
                        <input type="text" id="Tik_Tokd" placeholder="Tik Tok" value="{contenido[2]}">
                    </label>
                    <br>
                    <label for="Email">
                        <h2>
                            Email
                        </h2>
                        <br>
                        <input type="text" id="Emaild" placeholder="Email" value="{contenido[3]}">
                    </label>
                </div>
                <div id="derecha">
                    <label for="Twiter">
                        <h2>
                            Twitter
                        </h2>
                        <br>
                        <input type="text" id="Twiterd" placeholder="Twitter" value="{contenido[4]}">
                    </label>
                    <br>
                    <label for="Whatsapp">
                        <h2>
                            Whatsapp
                        </h2>
                        <br>
                        <input type="text" id="Whatsappd" placeholder="Whatsapp" value="{contenido[5]}">
                    </label>
                    <br>
                    <label for="Telefono">
                        <h2>
                            Telefono
                        </h2>
                        <br>
                        <input type="text" id="Telefonod" placeholder="Telefono" value="{contenido[6]}">
                    </label>
                </div>
            </div>
            <br>
            <button id="registrar" onclick="actualizartabalcontactos({contenido[7]})">Actualizar</button>
            """
            
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')
    
@app.route('/api/buscador_season_edit', methods=['POST'])
def buscador_season_edit():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT season_specification.season, season_specification.Id_season FROM season_specification WHERE season_specification.Id_season=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            html = f"""
            <span class="cerrar">&times;</span>
            <div class="alinear">
                <h1>
                    Edición de temporada
                </h1>
                <br>
                <label for="temporada">
                    <h2>
                        Temporada
                    </h2>
                    <br>
                    <input type="text" id="temporadad" placeholder="Temporada" value="{contenido[0]}">
                </label>
                <br>
                <button id="registrar" onclick="editarsqltemporada({contenido[1]})">Actualizar</button>
            </div>
            """
            
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')
    
@app.route('/api/buscador_users_edit', methods=['POST'])
def buscador_users_edit():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT users.User, users.Email, users.Name, users.Surname, users.Lastname, users.Rol, users.Estado, users.Id_user FROM users WHERE users.Id_user=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            html = f"""
            <span class="cerrar" onclick="cerrarModal()">&times;</span>
            <h1>Datos del usuario</h1>
            <h2>Usuario</h2>
            <p>{contenido[0]}</p>
            <br>
            <h2>Email</h2>
            <p>{contenido[1]}</p>
            <br>
            <h2>Nombre</h2>
            <p>{contenido[2]}</p>
            <br>
            <h2>Apellido paterno</h2>
            <p>{contenido[3]}</p>
            <br>
            <h2>Apellido materno</h2>
            <p>{contenido[4]}</p>
            <br>
            """
            if contenido[5]=="administrador":
                html+=f"""
                    <h2 for="estado">Rol</h2>
                    <select id="rol" name="rol">
                        <option value="administrador" selected>Administrador</option>
                        <option value="cliente">Cliente</option>
                    </select>
                    <br>
                """
            else:
                html+=f"""
                    <h2 for="estado">Rol:</h2>
                    <select id="rol" name="rol">
                        <option value="administrador">Administrador</option>
                        <option value="cliente" selected>Cliente</option>
                    </select>
                    <br>
                """
            if contenido[6]=="Activo":
                html+=f"""
                    <h2 for="estado">Estado:</h2>
                    <select id="estado" name="estado">
                        <option value="Activo" selected>Activo</option>
                        <option value="Inactivo">Inactivo</option>
                    </select>
                    <br>
                """
            else:
                html+=f"""
                    <h2 for="estado">Estado:</h2>
                    <select id="estado" name="estado">
                        <option value="Activo">Activo</option>
                        <option value="Inactivo" selected>Inactivo</option>
                    </select>
                    <br>
                """
            html+=f"""
            <br>
            <button id="registrar" onclick="editarsqlcontenido({contenido[7]})">Actualizar</button>
            """
            
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')

@app.route('/api/buscador_producto_edit', methods=['POST'])
def buscador_producto_edit():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT products.Material_composition, products.Model, season_specification.season, products.Size, products.Name, products.Description, products.Price_per_unit, products.Color, products.url_imagen, users.User, products.Id_product FROM products INNER JOIN season_specification ON products.FK_id_season=season_specification.Id_season INNER JOIN users ON products.FK_Id_user=users.Id_user WHERE products.Id_product=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            direccion_imagen= url_for('static', filename=f'image/imagenes_productos/{contenido[8]}', _external=True)
            
            html = f"""
            <span class="cerrar" onclick="cerrarModal()">&times;</span>
            <h1>Edición de producto</h1>

            <div class="izquierda">
                <label for="image">Imagen del producto:
                    <input type="file" name="image" id="image" accept="image/*">
                </label>
                <br>
                <img src="{direccion_imagen}" alt="{contenido[8]}" style="width:300px;height:auto;">
                <br>
                <label for="modelo">Modelo:
                    <input type="text" name="modelo" id="modelo" value="{contenido[1]}">
                </label>
                <br>
                <label for="temporada">Temporada:
                    <input type="text" name="temporada" id="temporada" value="{contenido[2]}">
                </label>
                <br>
                <label for="tamaño">Tamaño:
                    <input type="text" name="tamaño" id="tamaño" value="{contenido[3]}">
                </label>
                <br>
                <label for="nombre">Nombre:
                    <input type="text" name="nombre" id="nombre" value="{contenido[4]}">
                </label>
                <br>
            </div>

            <div class="derecha">
                <label for="descripcion">Descripción:
                    <textarea name="descripcion" id="descripcion">{contenido[5]}</textarea>
                </label>
                <br>
                <label for="precio_lot">Precio (lote):
                    <input type="number" name="precio_lot" id="precio_lot" value="{contenido[6]}">
                </label>
                <br>
                <label for="color">Color:
                    <input type="text" name="color" id="color" value="{contenido[7]}">
                </label>
                <br>
                <label for="materia">Material de composición:
                    <input type="text" name="materia" id="materia" value="{contenido[0]}">
                </label>
                <br>
            </div>

            <br>
            <button id="registrar" onclick="editarproducto({contenido[10]})">Editar</button>
            """

            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')

#Solisitar datos para pantalla de detalles
@app.route('/api/buscador_producto_dettalles', methods=['POST'])
def buscador_producto_dettalles():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT products.Material_composition, products.Model, season_specification.season, products.Size, products.Name, products.Description, products.Price_per_unit, products.Color, products.url_imagen, users.User FROM products INNER JOIN season_specification ON products.FK_id_season=season_specification.Id_season INNER JOIN users ON products.FK_Id_user=users.Id_user WHERE products.Id_product=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            direccion_imagen= url_for('static', filename=f'image/imagenes_productos/{contenido[8]}', _external=True)
            
            html = f"""
            <span class="cerrar" onclick="cerrarModal()">&times;</span>
            <h1>Detalles de producto</h1>

            <h2>Imagen</h2>
            <img src="{direccion_imagen}" alt="{contenido[8]}" style="width:300px;height:auto;">

            <h2>Modelo</h2>
            <p>{contenido[1]}</p>

            <h2>Temporada</h2>
            <p>{contenido[2]}</p>

            <h2>Tamaño</h2>
            <p>{contenido[3]}</p>

            <h2>Nombre</h2>
            <p>{contenido[4]}</p>

            <h2>Descripción</h2>
            <p>{contenido[5]}</p>

            <h2>Precio por unidad</h2>
            <p>${contenido[6]}</p>

            <h2>Color</h2>
            <p>{contenido[7]}</p>

            <h2>Composición del material</h2>
            <p>{contenido[0]}</p>

            <h2>Usuario que lo registro</h2>
            <p>{contenido[9]}</p>
            """
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')

#Actualizar datos
@app.route('/actualizar_contenido', methods=['POST'])
def actualizar_contenido():
    init_db()

    data = request.get_json()
    titulo = data.get('titulo')
    descripcion = data.get('descripcion')
    id = data.get('id')

    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                UPDATE `content` SET `Title` = :titulo, `Describe` = :descripcion WHERE `content`.`Id_contenido` = :id;
            """
            print(f"Ejecutando consulta: {sql_query}")

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "titulo": titulo,
                "descripcion": descripcion,
                "id":id
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Actualizacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al registrar: {str(e)}"}), 500

@app.route('/actualizar_contacto', methods=['POST'])
def actualizar_contacto():
    init_db()

    data = request.get_json()
    facebook = data.get('facebook')
    instagram = data.get('instagram')
    tik_tok = data.get('tik_tok')
    email = data.get('email')
    twitter = data.get('twitter')
    whatsapp = data.get('whatsapp')
    phone = data.get('phone')
    id = data.get('id_contact')

    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                UPDATE `contacts` 
                SET `Facebook` = :facebook, 
                    `Instagram` = :instagram, 
                    `Tik_tok` = :tik_tok, 
                    `Email` = :email, 
                    `Twitter` = :twitter, 
                    `Whatsapp` = :whatsapp, 
                    `Phone` = :phone 
                WHERE `contacts`.`Id_contact` = :id;
            """

            # Ejecutar la consulta con los datos
            connection.execute(text(sql_query), {
                "facebook": facebook,
                "instagram": instagram,
                "tik_tok": tik_tok,
                "email": email,
                "twitter": twitter,
                "whatsapp": whatsapp,
                "phone": phone,
                "id":id
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Actualizacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al actualizar: {str(e)}"}), 500

@app.route('/actualizar_temporada', methods=['POST'])
def actualizar_temporada():
    init_db()

    data = request.get_json()
    season = data.get('season')
    id = data.get('id')

    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                UPDATE `season_specification` SET `season_specification`.`season` = :season WHERE `season_specification`.`Id_season` = :id;
            """

            # Ejecutar la consulta con los datos
            connection.execute(text(sql_query), {
                "season": season,
                "id":id
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Actualizacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al actualizar: {str(e)}"}), 500

#inicio de secion y cerrar seción
@app.route('/login', methods=['POST'])
def login():
    init_db()
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    #time.sleep(3)
    try:
        with engine.connect() as connection:
            sql_query = """
            SELECT users.Rol, users.Id_user, users.Name FROM users WHERE users.Password=:password AND users.Email=:email;
            """
            result = connection.execute(text(sql_query), {
                "email": email,
                "password": password
            }).fetchone()
            
            if result:
                #Almacenar los datos del usuario
                session['permiso_usuario'] = result[0]
                session['id_usuario'] = result[1]
                session['usuario_usuario'] = result[2]
                
                # Redirige según el rol
                if session['permiso_usuario'] == 'administrador':
                    return jsonify({"redirect": "/administrador"})
                else:
                    return jsonify({"redirect": "/"})
            else:
                print(4)
                return jsonify({"message": "Usuario o contraseña incorrectos"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error en el servidor"}), 500

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    
    # Redirigir a la página de inicio o a donde desees
    return jsonify({"redirect": "/"}) # Redirige a la página principal

#Direccionamientos####################################################################
@app.route('/')
def home():
    return render_template('index.html')

def login_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'permiso_usuario' not in session or session['permiso_usuario'] != role:
                return redirect(url_for('home'))  # Redirigir al inicio si no está autenticado
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/administrador_productos')
@login_required('administrador')
def administrador_productos():
    response = make_response(render_template('administracion.html'))
    # Control de caché
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/administrador_season')
@login_required('administrador')
def administrador_season():
    response = make_response(render_template('administracion_season.html'))
    # Control de caché
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/administrador_contact')
@login_required('administrador')
def administrador_contact():
    response = make_response(render_template('administracion_contactos.html'))
    # Control de caché
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/administrador_content')
@login_required('administrador')
def administrador_content():
    response = make_response(render_template('administracion_content.html'))
    # Control de caché
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/administrador_user')
@login_required('administrador')
def administrador_user():
    response = make_response(render_template('administracion_users.html'))
    # Control de caché
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/administrador')
@login_required('administrador')
def administrador():
    response = make_response(render_template('administracion_inicio.html'))
    # Control de caché
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/cliente')
def cliente():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/producto')
def producto():
    return render_template('producto.html')

@app.route('/inicio_usuario')
def inicio_usuario():
    return render_template('registro_Inicio.html')

@app.route('/inicio_sesion')
def iniciar_sesion():
    checkbox_checked = True
    return render_template('registro_Inicio.html', checkbox_checked=checkbox_checked)

# Inicio del servidor
if __name__ == '__main__':
    init_db()
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
