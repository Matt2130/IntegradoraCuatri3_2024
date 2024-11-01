//console.log(1);
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('signupForm').addEventListener('submit', function(e) {
        console.log(123456);
        e.preventDefault(); // Prevenir el comportamiento por defecto del formulario

        //Pantalla de carga
        document.getElementById('loading').style.display = 'flex';

        const formData = {
            name: document.getElementById('name').value,
            lastname: document.getElementById('lastname').value,
            surname: document.getElementById('surname').value,
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
        };

        fetch('/registro_usuario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message);
            document.getElementById('loading').style.display = 'none';
            alert("Registro exitoso: " + data.message);
            window.open('/', '_self');
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Error al registrar: " + error.message); // Mostrar alerta de error
        })
        .finally(() => {
            // Desaparecer la pantalla de carga
            document.getElementById('loading').style.display = 'none';
        });
    });
    //Iniciar secion
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();

        document.getElementById('loading').style.display = 'flex';

        // Obtener los datos del formulario
        const formData = {
            email: document.getElementById('email2').value,
            password: document.getElementById('password2').value,
        };

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('loading').style.display = 'none';
            
            if (data.redirect) {
                // Redirigir a la URL proporcionada
                window.open(data.redirect, '_self');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('loading').style.display = 'none';
            alert("Error al iniciar sesión: " + error.message);
        });
    });
});
