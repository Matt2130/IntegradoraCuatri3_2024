document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/mostrador_productos')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la red: ' + response.statusText);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('catalogo').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
});

