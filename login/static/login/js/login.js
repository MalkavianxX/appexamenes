
function getCSRFToken() {
    const name = 'csrftoken=';
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookieArray = decodedCookie.split(';');

    for (let i = 0; i < cookieArray.length; i++) {
        let cookie = cookieArray[i].trim();
        if (cookie.indexOf(name) === 0) {
            return cookie.substring(name.length, cookie.length);
        }
    }

    return null;
}

function login() {
    // Obtén los valores de los campos de entrada
    const emailAddress = document.getElementById('emailaddress').value;
    const password = document.getElementById('password').value;
    const csrfToken = getCSRFToken();

    // Crea un objeto FormData para almacenar los datos del formulario
    const formData = {
        username: emailAddress,
        password: password
    };

    // Muestra un mensaje de inicio de sesión
    Swal.fire({
        title: 'Iniciando sesión...',
        text: 'Por favor, espera un momento.',
        icon: 'info',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    fetch('/function_login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Las credenciales no son válidas.');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            Swal.fire({
                title: 'Error',
                text: data.error,
                icon: 'error'
            });
        } else {
            Swal.fire({
                title: 'Éxito',
                text: 'Inicio de sesión exitoso.',
                icon: 'success',
                timer: 1500,
                showConfirmButton: false
            }).then(() => {
                window.location.href = '/dashboard/view_dashboard';
            });
        }
    })
    .catch(error => {
        Swal.fire({
            title: 'Error',
            text: error.message,
            icon: 'error'
        });
    });
}

