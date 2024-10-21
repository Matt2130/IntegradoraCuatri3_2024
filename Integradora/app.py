from flask import Flask, render_template, Response

app = Flask(__name__)

#Funciones a llamar desde la web despues de cargar la pagina
@app.route('/api/contactos')
def mi_funcion():
    return Response("<h1>Se esta tranajando en una funcion que imprima los contactos de la base de datos :)<h1>", mimetype='text/html')

#Direccionamiento de la web
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
