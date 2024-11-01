from sqlalchemy import create_engine, text

# Configuración global
engine = None

def init_db():
    global engine
    if engine is None:
        engine = create_engine('mysql+pymysql://root:@localhost/integradora')

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

