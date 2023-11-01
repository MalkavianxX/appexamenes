
function actualizarColorTexto() {
    var banner = document.querySelector('.banner');
    var colorFondo = window.getComputedStyle(banner).backgroundColor;

    // Convertir el color de fondo a formato RGB
    var rgb = colorFondo.replace(/[^\d,]/g, '').split(',');

    // Calcular la luminancia
    var luminancia = (0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2])/255;

    // Si el fondo es claro, usar texto oscuro. Si es oscuro, usar texto claro.
    if (luminancia > 0.5) {
        banner.style.color = 'black';
    } else {
        banner.style.color = 'white';
    }
}

// Llamar a la función cuando la página se carga
window.onload = actualizarColorTexto;
function subirImagen() {
var input = document.createElement('input');
input.type = 'file';
input.accept = 'image/*';
input.addEventListener('change', function() {
    var file = input.files[0];

    // Comprobar el tipo de archivo
    if (!['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
        alert('Tipo de archivo no permitido. Por favor, sube una imagen en formato JPEG o PNG.');
        return;
    }

    // Comprobar el tamaño del archivo (2.5MB en bytes)
    if (file.size > 2.5 * 1024 * 1024) {
        alert('El archivo es demasiado grande. Por favor, sube una imagen que sea menor a 2.5MB.');
        return;
    }

    var reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('avatar-visualizacion').src = e.target.result;
        document.getElementById('avatar').value = e.target.result;
    };
    reader.readAsDataURL(file);
});
input.click();
}


document.getElementById('colorback').addEventListener('change', function() {
    var colorDeFondo = this.value;
    document.getElementById('color-previsualizacion').style.backgroundColor = colorDeFondo;
    document.getElementById('color').value = colorDeFondo;
});

document.querySelectorAll('.img-fluid.avatar-md.rounded-circle').forEach(function(avatar) {
    avatar.addEventListener('click', function() {
        // Cambia la imagen del img con id "avatar-visualizacion"
        document.getElementById('avatar-visualizacion').src = avatar.src;
        document.getElementById('avatar').value = avatar.src;
    });
});


document.getElementById('passwordForm').addEventListener('input', function() {
    var password1 = document.getElementById('password1');
    var password2 = document.getElementById('password2');
    var submitBtn = document.getElementById('submitBtn');

    // Comprobar si las contraseñas son iguales y tienen más de 6 caracteres
    if (password1.value === password2.value && password1.value.length >= 6) {
        password1.setCustomValidity('');
        password2.setCustomValidity('');
        submitBtn.disabled = false;
    } else {
        if (password1.value.length < 6) {
            password1.setCustomValidity('La contraseña debe tener al menos 6 caracteres.');
        } else {
            password1.setCustomValidity('');
        }
        if (password1.value !== password2.value) {
            password2.setCustomValidity('Las contraseñas no coinciden.');
        } else {
            password2.setCustomValidity('');
        }
        submitBtn.disabled = true;
    }
});


