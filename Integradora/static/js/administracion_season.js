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