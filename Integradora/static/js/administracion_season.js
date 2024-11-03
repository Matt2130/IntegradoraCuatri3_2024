document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/tabla_season_specification')
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
///////////////////////////////////////////////////////////////////////////////////////    
function eliminarProducto(param) {
    const confirmacion = confirm("¿Estás seguro de que deseas eliminar este usuario? (Ya no sera reversible esta operación)");

    if (confirmacion){
        // Mostrar la pantalla de carga
        document.getElementById('loading').style.display = 'flex';
    
        // Enviar solo el parámetro 'param' a Flask
        fetch('/eliminar_season', {
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
            window.open('/administrador_season', '_self'); // Redirige después del éxito
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
//Buscador
function buscador() {
    const buscar = document.getElementById('buscador').value;

    fetch('/api/buscador_season', {
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
///Modal de registro
document.addEventListener("DOMContentLoaded", function() {
    // Obtiene el modal
    var modal = document.getElementById("miModal");

    // Obtiene el botón que abre la modal
    var btn = document.getElementById("abrirModal");

    // Obtiene el elemento <span> que cierra la modal
    var span = document.getElementsByClassName("cerrar")[0];

    // Cuando el usuario hace clic en el botón, se abre la modal
    btn.onclick = function() {
        modal.style.display = "block";
    }

    // Cuando el usuario hace clic en <span> (x), se cierra la modal
    span.onclick = function() {
        modal.style.display = "none";
    }

});

//Registrar
function registrartemporadao(){
    const temporada = document.getElementById('temporada').value;

    fetch('/registrar_season', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            temporada: temporada
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.json();
    })
    .then(data => {
        alert(data.message); 
        window.location.href = '/administrador_season';
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Error al registrar: " + error.message);
    });
}//Modal para edición
function editarProducto(id) {
    var modal = document.getElementById("miModal2");
    modal.style.display = "block"; // Muestra el modal

    fetch('/api/buscador_season_edit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.text(); // Cambiado a text() para manejar HTML
    })
    .then(html => {
        // Inserta el HTML en el modal
        document.getElementById('miModal2').querySelector('.modal-contenido').innerHTML = html;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('miModal2').querySelector('.modal-contenido').innerText = 'Error en la edición';
    });
}

function cerrarModal() {
    var modal = document.getElementById("miModal2");
    modal.style.display = "none";
}
window.onclick = function(event) {
    var modal = document.getElementById("miModal2");
    if (event.target === modal) {
        cerrarModal();
    }
}
//Edicion en la base de datos
function editarsqltemporada(idw){
    const season = document.getElementById('temporadad').value;
    const id = idw;

    fetch('/actualizar_temporada', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            season: season,
            id:id
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.json();
    })
    .then(data => {
        alert(data.message); 
        window.location.href = '/administrador_season';
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Error al registrar: " + error.message);
    });
}