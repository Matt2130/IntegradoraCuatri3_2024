document.addEventListener('DOMContentLoaded', function() {
    //console.log(12345);
    fetch('/api/tabla_contact')
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
        fetch('/eliminar_contacto', {
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
            window.open('/administrador_contact', '_self'); // Redirige después del éxito
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
//Modal registrar
function abrirModal() {
    var modal = document.getElementById("miModal");
    modal.style.display = "block"; // Muestra el modal

    var span = modal.getElementsByClassName("cerrar")[0];
    span.onclick = function() {
        modal.style.display = "none"; // Cierra el modal al hacer clic en la "X"
    }

    // Cierra el modal si se hace clic fuera de él
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }
}
////////////////////////////////////////////////////////////////////////////////
function registrarcontactos(){
    //console.log(3456789);
    
    const facebook = document.getElementById('Facebook').value;
    const instagram = document.getElementById('Instagram').value;
    const tik_tok = document.getElementById('Tik_Tok').value;
    const email = document.getElementById('Email').value;
    const twitter = document.getElementById('Twiter').value;
    const whatsapp = document.getElementById('Whatsapp').value;
    const phone = document.getElementById('Telefono').value;

    fetch('/registrar_contactos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            facebook: facebook,
            instagram: instagram,
            tik_tok:tik_tok,
            email:email,
            twitter:twitter,
            whatsapp:whatsapp,
            phone:phone

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
        window.location.href = '/administrador_contact';
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Error al registrar: " + error.message);
    });
    
}
//Modal edicion
function editarProducto(id) {
    var modal = document.getElementById("miModal2");
    modal.style.display = "block"; // Muestra el modal

    fetch('/api/buscador_contacto_edit', {
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

//Actualizar bd
function actualizartabalcontactos(idw){
    //console.log(idw);
    const facebook = document.getElementById('Facebookd').value;
    const instagram = document.getElementById('Instagramd').value;
    const tik_tok = document.getElementById('Tik_Tokd').value;
    const email = document.getElementById('Emaild').value;
    const twitter = document.getElementById('Twiterd').value;
    const whatsapp = document.getElementById('Whatsappd').value;
    const phone = document.getElementById('Telefonod').value;
    const id = idw;

    fetch('/actualizar_contacto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            facebook: facebook,
            instagram: instagram,
            tik_tok:tik_tok,
            email:email,
            twitter:twitter,
            whatsapp:whatsapp,
            phone:phone,
            id_contact: id
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
        window.location.href = '/administrador_contact';
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Error al actualizar: " + error.message);
    });
}
