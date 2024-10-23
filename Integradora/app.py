from flask import Flask, render_template, Response
import mysql.connector 

app = Flask(__name__)

# Funciones de bases de datos
def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="integradora"
    )
    return connection


#Funciones a llamar desde la web despues de cargar la pagina
@app.route('/api/contactos')
def contactos():
    connection = connect_db() 
    cursor = connection.cursor()
    cursor.execute("SELECT contacts.Facebook, contacts.Instagram, contacts.Tik_tok, contacts.Email, contacts.Twitter, contacts.Whatsapp, contacts.Phone FROM contacts;")
    contactos = cursor.fetchall()
    nombre_columnas = [desc[0] for desc in cursor.description]
    html = ""
    
    for redes in contactos:
        html+='<div class="contacto_contenedor">'
        for url, nombre in zip(redes,nombre_columnas):
            if not url=="":
                html += f"""
                <div class="elementos">
                    <a href="{url}">
                        <img src="static/image/{nombre}.svg" alt="{nombre}" class="{nombre}">
                    </a>
                </div>
                """
        html+='</div><hr>'

    cursor.close()
    connection.close()
    
    return Response(html, mimetype='text/html')

@app.route('/api/texto_vision_mision')
def texto_mision_vision():
    connection = connect_db() 
    cursor = connection.cursor()
    cursor.execute('SELECT content.Title, content.Describe FROM content WHERE content.Title!="Valores" AND content.Title!="Derechos";')
    contenido = cursor.fetchall()
    html = ""
    
    for titulo,descripcion in contenido:
        html+='<div class="valores_derechos">'
        html+=f"""
            <h2>{titulo}</h2>
            <p>{descripcion}</p> 
        """
        html+='</div><br>'

    cursor.close()
    connection.close()
    
    return Response(html, mimetype='text/html')

@app.route('/api/texto_valores')
def texto_valores():
    connection = connect_db() 
    cursor = connection.cursor()
    cursor.execute('SELECT content.Title, content.Describe FROM content WHERE content.Title="Valores" OR content.Title="Derechos";')
    contenido = cursor.fetchall()
    html = ""
    
    for titulo,descripcion in contenido:
        html+='<div class="valores_derechos">'
        html+=f"""
            <h2>{titulo}</h2>
            <p>{descripcion}</p> 
        """
        html+='</div><br>'

    cursor.close()
    connection.close()
    
    return Response(html, mimetype='text/html')

#Direccionamiento de la web
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/otra_pagina')
def ejemplo():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)
