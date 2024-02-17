function showAlert(message, alertType) {
    var alertPlaceholder = document.getElementById('alert_placeholder');
    var alertBox = '<div class="alert ' +  alertType + ' alert-dismissible fade show" role="alert">' +
        message +
        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
        '</div>';
    alertPlaceholder.innerHTML = alertBox;
}


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
    var emailAddress = document.getElementById('emailaddress').value;
    var password = document.getElementById('password').value;
    const csrfToken = getCSRFToken();

    // Crea un objeto FormData para almacenar los datos del formulario
    var formData = {
        username: emailAddress,
        password: password
    };
    

    console.log(formData);
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
            // Si la respuesta no es OK, lanza un error
            throw new Error(' las credenciales no son validas.');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            // Si hay un error, muéstralo
            alert("Error: " + data.error);
            showAlert(error,'alert-danger');
        } else {
            // Aquí podrías hacer algo adicional si la autenticación es exitosa
            console.log('Inicio de sesión exitoso');
            window.location.href = '/dashboard/view_dashboard';
        }
    })
    .catch(error => {
        showAlert(error,'alert-danger');
    });
    
}
