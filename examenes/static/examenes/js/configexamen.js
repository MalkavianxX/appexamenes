window.addEventListener('DOMContentLoaded', (event) => {
    $('#select_temas').change(function() {

        var preguntas = parseInt($(this).find(':selected').data('preguntas')) ;
        var select_preguntas = $('#select_preguntas');
      
        select_preguntas.empty();
        for (var i = 1; i <= preguntas; i += 1) {


            select_preguntas.append($('<option>', { value: i, text: i }));
        }
    });

    $('#boton_recopilar').click(function() {
        let modalBody = document.querySelector('.modal-body .text');

        var opcionSeleccionada = $('#select_temas').find(':selected');
        var preguntas = $('#select_preguntas').val();
        var tiempo = opcionSeleccionada.data('tiempo');
        var tema = opcionSeleccionada.data('tema');

        // Actualiza el contenido del modal
        modalBody.innerHTML = `
            <li><p class="fs-3 text-muted"> <i class="mdi mdi-timer-sand-complete "></i> ${tiempo} minutos</p></li>
            <li><p class="fs-3 text-muted"> <i class="mdi mdi-notebook-outline"></i> ${preguntas} preguntas</p></li>
            <li><p class="fs-3 text-muted"> <i class="mdi mdi-pencil-box-multiple-outline"></i> ${tema}</p></li>
        `;
    });

    $('#btn_empezar_examen').click(function() {
        var opcionSeleccionada = $('#select_temas').find(':selected');
        var id = opcionSeleccionada.data('id');
        var preguntas = $('#select_preguntas').val();

        window.location.href = '/examenesview_start_test/'+ id +'/'+preguntas + '/';
    });
});
