from flask import Flask, make_response, redirect, url_for, render_template, session, request, jsonify, Response
from sqlalchemy import create_engine, text
#Se eliminara pero es para hacer pruebas
import time

app = Flask(__name__)

# Establecer la clave secreta
app.secret_key = '12345'  # Cambia esto por una clave única

#Conexión
engine = None

#Función para iniciar la base de datos
def init_db():
    global engine
    if engine is None:
        engine = create_engine('mysql+pymysql://root:@localhost/integradora')
        #mysql+pymysql://<usuario>:<contraseña>@<host>/<nombre_base_de_datos>

#Funciones a llamar desde la web después de cargar la página
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
            
            html = """
            <table>
                <thead>
                    <tr>
                        <th>Facebook</th>
                        <th>Instagram</th>
                        <th>Tik_tok</th>
                        <th>Email</th>
                        <th>Twitter</th>
                        <th>Whatsapp</th>
                        <th>Telefono</th>
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
                        <td>{info[6]}</td>
                        <td>
                            <button onclick="editarProducto({info[7]})" class="editar">Editar</button>
                            <button onclick="eliminarProducto({info[7]})" class="eliminar">Eliminar</button>
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

@app.route('/api/tabla_content')
def tabla_content():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text('SELECT content.Title, content.Describe, content.Id_contenido FROM content;'))
            contenido = result.fetchall()
            
            html = """
            <table>
                <thead>
                    <tr>
                        <th>Titulo</th>
                        <th>Descripción</th>
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
                        <td>
                            <button onclick="editarProducto({info[2]})" class="editar">Editar</button>
                            <button onclick="eliminarProducto({info[2]})" class="eliminar">Eliminar</button>
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

@app.route('/api/tabla_users')
def tabla_users():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text('SELECT users.User, users.Password, users.Email, users.Name, users.Surname, users.Lastname, users.Rol, users.Id_user FROM users;'))
            contenido = result.fetchall()
            
            html = """
            <table>
                <thead>
                    <tr>
                        <th>Usuario</th>
                        <th>Contraseña</th>
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
                        <td>{info[6]}</td>
                        <td>
                            <button onclick="editarProducto({info[7]})" class="editar">Editar</button>
                            <button onclick="eliminarProducto({info[7]})" class="eliminar">Eliminar</button>
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

    time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                INSERT INTO users (User, Password, Email, Name, Surname, Lastname, Rol)
                VALUES (:username, :password, :email, :name, :surname, :lastname, 'cliente')
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

@app.route('/login', methods=['POST'])
def login():
    init_db()
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    print(email)
    print(password)
    time.sleep(3)
    try:
        with engine.connect() as connection:
            sql_query = """
            SELECT users.Rol FROM users WHERE users.Password=:password AND users.Email=:email;
            """
            result = connection.execute(text(sql_query), {
                "email": email,
                "password": password
            }).fetchone()
            
            print(result)
            
            if result:
                rol = result[0]
                # Almacena la información del usuario en la sesión
                session['email'] = email
                session['rol'] = rol
                
                print(rol)
                
                # Redirige según el rol
                if rol == 'administrador':
                    print(1)
                    return jsonify({"redirect": "/administrador_productos"})
                elif rol == 'cliente':
                    print(2)
                    return jsonify({"redirect": "/cliente"})
                else:
                    print(3)
                    return jsonify({"message": "Rol no reconocido"})
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

#Direccionamientos
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/administrador_productos')
def administrador_productos():
    #if 'email' not in session:  # Verifica si el usuario está logueado
    #    return redirect(url_for('/'))
    #response = make_response(render_template('administracion.html'))
    #response.headers['Cache-Control'] = 'no-store'
    return render_template('administracion.html')

@app.route('/administrador_season')
def administrador_season():
    #if 'email' not in session:  # Verifica si el usuario está logueado
    #    return redirect(url_for('/'))
    #response = make_response(render_template('administracion.html'))
    #response.headers['Cache-Control'] = 'no-store'
    return render_template('administracion_season.html')

@app.route('/administrador_contact')
def administrador_contact():
    #if 'email' not in session:  # Verifica si el usuario está logueado
    #    return redirect(url_for('/'))
    #response = make_response(render_template('administracion.html'))
    #response.headers['Cache-Control'] = 'no-store'
    return render_template('administracion_contactos.html')

@app.route('/administrador_content')
def administrador_content():
    #if 'email' not in session:  # Verifica si el usuario está logueado
    #    return redirect(url_for('/'))
    #response = make_response(render_template('administracion.html'))
    #response.headers['Cache-Control'] = 'no-store'
    return render_template('administracion_content.html')

@app.route('/administrador_user')
def administrador_user():
    #if 'email' not in session:  # Verifica si el usuario está logueado
    #    return redirect(url_for('/'))
    #response = make_response(render_template('administracion.html'))
    #response.headers['Cache-Control'] = 'no-store'
    return render_template('administracion_users.html')

@app.route('/cliente')
def cliente():
    return render_template('index.html')

@app.route('/inicio_usuario')
def inicio_usuario():
    return render_template('registro_Inicio.html')

# Inicio del servidor
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
