function confirmarEliminacion() {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "Esta acción eliminará el producto. No podras recuperarlo!",
        icon: 'warning',
        iconColor: '#000000',
        showCancelButton: true,
        cancelButtonColor: '#d33',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#fed800',
        confirmButtonText: 'Eliminar',
        background: '#bfbfbf', // Fondo blanco de la alerta
        backdrop: 'rgba(0,0,0,0.7)', // Fondo oscuro con transparencia
        customClass: {
            popup: 'mi-alerta-redondeada'  // Clase personalizada
        }
    }).then((result) => {
        if (result.isConfirmed) {
            // Aquí puedes agregar la lógica para eliminar el producto de tu base de datos
            Swal.fire({
                title: 'Eliminado',
                text: 'Producto eliminado correctamente',
                icon: 'success',
                iconColor: '#2b8c4b',
                background: '#bfbfbf',
                confirmButtonColor: '#fed800',
                backdrop: 'rgba(0,0,0,0.7)',
                timer: 4000, // La alerta de éxito se cerrará automáticamente
                customClass: {
                    popup: 'mi-alerta-redondeada'  // Clase personalizada
                }
            });
        }
    });
}

// Archivo: alerts.js

// Alerta para acceso como Administrador
function showAdminAccessAlert() {
    Swal.fire({
        icon: 'success',
        iconColor: '#2b8c4b',
        title: '¡Bienvenido!',
        text: 'Accediendo como Administrador',
        timer: 2000,
        showConfirmButton: false,
        background: '#bfbfbf', // Fondo blanco de la alerta
        backdrop: 'rgba(0,0,0,0.7)', // Fondo oscuro con transparencia
        customClass: {
            popup: 'mi-alerta-redondeada'
        }
    }).then(() => {
        window.location.href = "/administrador_productos";
    });
}

// Alerta para acceso como Cliente
function showClientAccessAlert() {
    Swal.fire({
        icon: 'success',
        iconColor: '#2b8c4b',
        title: '¡Bienvenido!',
        text: 'Accediendo como Cliente',
        timer: 2000,
        showConfirmButton: false,
        background: '#bfbfbf', // Fondo blanco de la alerta
        backdrop: 'rgba(0,0,0,0.7)', // Fondo oscuro con transparencia
        customClass: {
            popup: 'mi-alerta-redondeada'
        }
    }).then(() => {
        window.location.href = "/cliente";
    });
}

// Alerta de usuario o contraseña incorrectos
function showInvalidCredentialsAlert() {
    Swal.fire({
        icon: 'error',
        iconColor: '#ec221f',
        showConfirmButton: false,
        showCancelButton: true,
        cancelButtonColor: '#fed800',
        cancelButtonText: 'OK',
        title: 'Error',
        text: 'Usuario o contraseña incorrectos',
        background: '#bfbfbf', // Fondo blanco de la alerta
        backdrop: 'rgba(0,0,0,0.7)', // Fondo oscuro con transparencia
        customClass: {
            popup: 'mi-alerta-redondeada'
        }
    });
}

// Alerta de rol no reconocido
function showUnrecognizedRoleAlert() {
    Swal.fire({
        icon: 'warning',
        iconColor: '#ec221f',
        showConfirmButton: false,
        showCancelButton: true,
        cancelButtonColor: '#fed800',
        cancelButtonText: 'OK',
        title: 'Rol no reconocido',
        text: 'El rol del usuario no está autorizado para el acceso',
        background: '#bfbfbf', // Fondo blanco de la alerta
        backdrop: 'rgba(0,0,0,0.7)', // Fondo oscuro con transparencia
        customClass: {
            popup: 'mi-alerta-redondeada'
        }
    });
}

// Alerta de error en el servidor
function showServerErrorAlert() {
    Swal.fire({
        icon: 'error',
        iconColor: '#ec221f',
        title: 'Error en el servidor',
        text: 'Hubo un problema al procesar tu solicitud. Intenta nuevamente más tarde',
        showConfirmButton: false,
        showCancelButton: true,
        cancelButtonColor: '#fed800',
        cancelButtonText: 'OK',
        background: '#bfbfbf', // Fondo blanco de la alerta
        backdrop: 'rgba(0,0,0,0.7)', // Fondo oscuro con transparencia
        customClass: {
            popup: 'mi-alerta-redondeada'
        }
    });
}