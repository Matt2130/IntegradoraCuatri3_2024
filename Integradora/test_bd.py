from sqlalchemy import create_engine, text

# URL de conexión a la base de datos
DATABASE_URL = "mysql+pymysql://root:@localhost/integradora"

# Crea el motor de conexión
engine = create_engine(DATABASE_URL)

def obtener_season_specification():
    try:
        # Intenta conectar y ejecutar una consulta
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM season_specification;"))
            result = connection.execute(text("SHOW tables;"))
            seasons = result.fetchall()  # Obtener todas las filas
            nombre_columnas = result.keys()  # Obtener los nombres de las columnas

            # Imprimir los nombres de las columnas
            print(", ".join(nombre_columnas))

            # Imprimir cada fila de resultados
            for season in seasons:
                print(", ".join(str(valor) for valor in season))
                
    except Exception as e:
        print(f"Error de conexión: {e}")  # Imprime el error en consola para depuración

# Ejecución de la función
if __name__ == "__main__":
    obtener_season_specification()  # Llama a la función para ejecutar

#host:RitaCid.mysql.pythonanywhere-services.com
#user:RitaCid
#pass:
#database:RitaCid$integradora
'''
from sqlalchemy import create_engine, text

# Configuración global
engine = None

def init_db():
    global engine
    if engine is None:
        engine = create_engine('mysql+pymysql://if0_37642511:CgsVW1Ls0UwhD@sql206.infinityfree.com:3306/if0_37642511_integradora')
        #engine = create_engine('mysql+pymysql://root:@localhost/integradora')

def test_signup():
    test_data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "testuser@example.com",
        "name": "Test",
        "surname": "User",
        "lastname": "Example"
    }

    try:
        init_db()
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))
            
            sql_query = """
                INSERT INTO users (User, Password, Email, Name, Surname, Lastname, Rol)
                VALUES (:username, :password, :email, :name, :surname, :lastname, 'cliente')
            """

            connection.execute(text(sql_query), {
                "username": test_data["username"],
                "password": test_data["password"],
                "email": test_data["email"],
                "name": test_data["name"],
                "surname": test_data["surname"],
                "lastname": test_data["lastname"]
            })

            # Confirmar la transacción
            connection.execute(text("COMMIT;"))
            print("Registro exitoso.")
    except Exception as e:
        print("Error al registrar:")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje de error: {str(e)}")
        # Hacer rollback en caso de error
        connection.execute(text("ROLLBACK;"))

if __name__ == "__main__":
    test_signup()
    
'''