// Manejar el cambio en el número de resultados por página
function updatePerPage() {
    const perPage = document.getElementById('per_page').value;
    const url = new URL(window.location.href);

    // Establecer el nuevo número de resultados por página
    url.searchParams.set('per_page', perPage);

    // Mantener otros parámetros de búsqueda
    const searchParams = new URLSearchParams(window.location.search);
    for (const [key, value] of searchParams) {
        if (key !== 'per_page') {
            url.searchParams.set(key, value);
        }
    }

    // Realizar la solicitud AJAX para actualizar los resultados
    fetch(url.toString())
        .then(response => response.text())
        .then(html => {
            // Crear un nuevo elemento DOM para contener la respuesta
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            // Obtener solo el contenido de resultados del documento cargado
            const newResults = doc.querySelector('#contenedor-resultados').innerHTML;

            // Actualizar el contenedor de resultados con la nueva información
            document.querySelector('#contenedor-resultados').innerHTML = newResults;
        })
        .catch(error => console.error('Error:', error));
}


document.addEventListener('DOMContentLoaded', function () {
        // Manejar el envío del formulario
        document.querySelector('.submit input[type="submit"]').addEventListener('click', function (event) {
            event.preventDefault(); // Evita el envío normal del formulario

            // Mostrar el contenedor de resultados
            document.querySelector('.resultado-container').style.display = 'block';

            // Crear FormData del formulario
            const form = document.querySelector('#search-form');
            const formData = new FormData(form);

            // Realizar la petición AJAX
            fetch('/', {
                method: 'POST',
                body: formData
            })
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newResults = doc.querySelector('.resultado-container').innerHTML;
                    document.querySelector('.resultado-container').innerHTML = newResults;
                })
                .catch(error => console.error('Error:', error));
        });

        // Añadir event listeners a los enlaces de paginación
        document.addEventListener('click', function (event) {
            if (event.target.matches('.pagination a')) {
                event.preventDefault(); // Evita el comportamiento predeterminado del enlace

                // Obtener el destino de la página
                const href = event.target.getAttribute('href');

                // Realizar una solicitud AJAX para obtener los resultados sin recargar la página
                fetch(href)
                    .then(response => response.text())
                    .then(html => {
                        // Crear un nuevo elemento DOM para contener la respuesta
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(html, 'text/html');

                        // Obtener solo el contenido de resultados del documento cargado
                        const newResults = doc.querySelector('.resultado-container').innerHTML;

                        // Actualizar el contenedor de resultados con la nueva información
                        document.querySelector('.resultado-container').innerHTML = newResults;
                    })
                    .catch(error => console.error('Error:', error));
            }
        });
    });
