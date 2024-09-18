window.addEventListener('DOMContentLoaded', (event) => {
    $('#select_temas').change(function () {
        var preguntas = parseInt($(this).find(':selected').data('preguntas'));
        var select_preguntas = $('#select_preguntas');

        select_preguntas.empty();

        // Genera opciones de 10 en 10 hasta el número de preguntas truncado hacia abajo
        for (var i = 10; i <= Math.min(90, Math.floor(preguntas / 10) * 10); i += 10) {
            select_preguntas.append($('<option>', { value: i, text: i }));
        }

        // Si el número de preguntas no es múltiplo de 10 y es menor o igual a 91, añade la opción final
        if (preguntas % 10 !== 0 && preguntas <= 91) {
            select_preguntas.append($('<option>', { value: preguntas, text: preguntas }));
        }
    });

    $('#boton_recopilar').click(function () {
        let modalBody = document.querySelector('.modal-body .text');

        var opcionSeleccionada = $('#select_temas').find(':selected');
        var preguntas = $('#select_preguntas').val();
        var tiempo = $('#select_preguntas').val(); + "min"

        var tema = opcionSeleccionada.data('tema');

        // Actualiza el contenido del modal
        modalBody.innerHTML = `
            <li><p class="fs-3 text-muted"> <i class="mdi mdi-timer-sand-complete "></i> ${tiempo} minutos</p></li>
            <li><p class="fs-3 text-muted"> <i class="mdi mdi-notebook-outline"></i> ${preguntas} preguntas</p></li>
            <li><p class="fs-3 text-muted"> <i class="mdi mdi-pencil-box-multiple-outline"></i> ${tema}</p></li>
        `;
    });

    $('#btn_empezar_examen').click(function () {
        var opcionSeleccionada = $('#select_temas').find(':selected');
        var id = opcionSeleccionada.data('id');
        var preguntas = $('#select_preguntas').val();


        // Mostrar alerta de confirmación
        Swal.fire({
            title: '¿Seguro que deseas empezar tu examen?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, empezar',
            cancelButtonText: 'No, cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                // Mostrar alerta de carga
                Swal.fire({
                    title: 'Construyendo examen...',
                    text: 'Estamos preparando tu examen, exito.',
                    allowOutsideClick: false,
                    didOpen: () => {
                        Swal.showLoading();
                    }
                });

                // Redirigir a la página del examen
                window.location.href = '/examenesview_start_test/' + id + '/' + preguntas + '/';
            } else {
                // Si el usuario cancela, no hacemos nada
                Swal.fire('Operación cancelada', 'Puedes continuar seleccionando tus opciones.', 'info');
            }
        });
    });
});

