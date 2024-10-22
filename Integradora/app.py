from flask import Flask, render_template, Response

app = Flask(__name__)

#Funciones a llamar desde la web despues de cargar la pagina
@app.route('/api/contactos')
def contactos():
    return Response("<h1>Se esta tranajando en una funcion que imprima los contactos de la base de datos :)<h1>", mimetype='text/html')

@app.route('/api/texto_vision_mision')
def texto_mision_vision():
    return Response("<h1>Llamar los datos de contenido para plazmrlos en un lugar, proximamente<h1>", mimetype='text/html')

@app.route('/api/texto_valores')
def texto_valores():
    return Response("<h1>Llamar los valres y derechos de la empresa<h1>", mimetype='text/html')

#Direccionamiento de la web
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
