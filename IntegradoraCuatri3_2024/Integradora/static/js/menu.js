document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('salir').addEventListener('click', function() {
        console.log(1234); // Mensaje de depuración para confirmar el clic en el botón

        // Realizar la solicitud para cerrar sesión
        fetch('/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cerrar sesión');
            }
            return response.json(); // Esperar la respuesta JSON
        })
        .then(data => {
            // Redirigir a la URL especificada en el JSON de respuesta
            window.location.href = data.redirect; // Cambia aquí según la ruta que desees
        })
        .catch(error => {
            console.error('Error:', error); // Manejo de errores
        });
    });
});
