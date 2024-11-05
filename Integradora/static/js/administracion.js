document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/tabla_productos')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la red: ' + response.statusText);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('administracion-tabla').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
});


function eliminarProducto(param) {
    const confirmacion = confirm("¿Estás seguro de que deseas eliminar este usuario? (Ya no sera reversible esta operación)");

    if (confirmacion){
        // Mostrar la pantalla de carga
        document.getElementById('loading').style.display = 'flex';
    
        // Enviar solo el parámetro 'param' a Flask
        fetch('/eliminar_producto', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ parametro: param })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json();
        })
        .then(() => {
            // Ocultar la pantalla de carga y mostrar alerta de éxito
            document.getElementById('loading').style.display = 'none';
            alert("Eliminación exitosa");
            window.open('/administrador_productos', '_self'); // Redirige después del éxito
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Error al eliminar: " + error.message); // Mostrar alerta de error
        })
        .finally(() => {
            // Asegurarse de ocultar la pantalla de carga en cualquier caso
            document.getElementById('loading').style.display = 'none';
        });
    }
}
/////////////////////////////////////////////////////////////////////////////////////////
//Buscador
function buscador() {
    const buscar = document.getElementById('buscador').value;

    fetch('/api/buscador_productos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ buscar: buscar })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.text();  // Cambiado de .json() a .text() para recibir HTML
    })
    .then(html => {
        // Muestra los resultados HTML en el contenedor
        const resultsContainer = document.getElementById('administracion-tabla');
        resultsContainer.innerHTML = html;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}