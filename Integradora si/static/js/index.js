document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/texto_vision_mision')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la red: ' + response.statusText);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('texto1').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
});

document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/texto_valores')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la red: ' + response.statusText);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('texto2').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
});

