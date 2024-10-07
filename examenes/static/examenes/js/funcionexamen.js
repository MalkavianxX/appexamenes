

document.addEventListener('DOMContentLoaded', function () {
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

  let tiempoRestante; // Declarar tiempoRestante en un ámbito más amplio

  $(document).ready(function () {


    $('.img-fluid').click(function () {
      // Abre el modal al hacer clic
      $('#imgmodal').modal('show');
    });
    var time = document.getElementById('numpreguntas').value;
    Swal.fire({
      title: `Tienes ${time} minutos`,
      showDenyButton: true,

      confirmButtonText: "Comenzar",
      denyButtonText: `Cancelar`
    }).then((result) => {
      /* Read more about isConfirmed, isDenied below */
      if (result.isConfirmed) {
        Swal.fire("Mucho exito!", "", "success");
        startCountdown(parseFloat(time));
      } else if (result.isDenied) {
        window.location.href = "/examenesview_config_examenes"
        Swal.fire({
          title: 'Cancelando examen',
          text: 'Por favor, espera mientras cancelamos tu examen.',
          allowOutsideClick: false,
          didOpen: () => {
            Swal.showLoading();
          }
        });

      }
    });
    function startCountdown(minutes) {
      var countdownElement = $("#countdown");
      var totalSeconds = minutes * 60;

      var interval = setInterval(function () {
        if (totalSeconds >= 0) {
          var formattedTime = formatTime(totalSeconds);
          countdownElement.html("<strong>" + formattedTime + "</strong>");
          tiempoRestante = totalSeconds; // Actualizar tiempoRestante
          totalSeconds--;

          if (totalSeconds < 0) {
            // El tiempo se agotó, llamar a recabarInformacion
            console.log("El tiempo se agotó, llamar a recab");
            recabarInformacion();
            clearInterval(interval); // Detener el intervalo
          }
        }
      }, 1000); // Actualiza cada segundo (1000 milisegundos)
    }

    function formatTime(totalSeconds) {
      var minutes = Math.floor(totalSeconds / 60);
      var seconds = totalSeconds % 60;
      return minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
    }

    // Inicia el temporizador con 15 minutos

  });

  // Selecciona todos los elementos con la clase 'respuesta'
  const respuestas = document.querySelectorAll('.respuesta');


  // Itera sobre cada respuesta
  respuestas.forEach(function (respuesta) {
    // Agrega un evento de clic a cada respuesta
    respuesta.addEventListener('click', function () {
      // Obtiene el valor del atributo 'data-respuesta'
      const preguntaActual = respuesta.getAttribute('data-respuesta');

      // Desactiva todas las respuestas de la pregunta actual
      document.querySelectorAll('.respuesta[data-respuesta="' + preguntaActual + '"]').forEach(function (elemento) {
        if (elemento !== respuesta) {
          elemento.classList.remove('text-bg-primary');
          elemento.querySelector('input').classList.remove('text-bg-primary');
          elemento.querySelector('span').classList.remove('text-bg-primary');
        }
      });

      // Activa o desactiva la respuesta actual dependiendo de su estado actual
      respuesta.classList.toggle('text-bg-primary');

      // Agrega o quita la clase 'text-bg-primary' al input y al span de la respuesta actual
      respuesta.querySelector('input').classList.toggle('text-bg-primary');
      respuesta.querySelector('span').classList.toggle('text-bg-primary');


    });
  });

  const numpreguntas = document.getElementById('numpreguntas').value;
  //bara de navegacion

  var tiemposRespuestas = [];





  function recabarInformacion() {
    // Recabar los IDs y valores de los input con la clase "text-bg-primary"
    const respuestasSeleccionadas = Array.from(document.querySelectorAll('.text-bg-primary input'))
      .reduce((acc, input) => {
        const pregunta = input.closest('.respuesta').getAttribute('data-id');
        acc[pregunta] = input.id;
        return acc;
      }, {});

    // Crear el objeto JSON con la información
    const id_examen = document.getElementById('id_examen').value;
    const data = {
      respuestas: respuestasSeleccionadas,
      tiempos: tiemposRespuestas,
      termino: 'error', // Valor predeterminado si hay un error
      id_examen: id_examen,
      numpreguntas: document.getElementById('numpreguntas').value,
    };

    // Verificar si el tiempo se agotó
    if (tiempoRestante <= 0) {
      data.termino = 'agotado';
    } else {
      // Verificar si el usuario hizo clic en "Terminar Examen"
      const botonTerminar = document.getElementById('terminar_examen');
      if (botonTerminar && botonTerminar.dataset.terminado === 'true') {
        data.termino = 'hecho';
      }
    }

    // Agregar el tiempo restante al objeto JSON
    data.tiempoRestante = tiempoRestante;
    const csrfToken = getCSRFToken();
    // Enviar el objeto JSON mediante Fetch a una función en Django
    Swal.fire({
      title: 'Evaluando examen',
      text: 'Por favor, espera mientras evaluamos tu examen.',
      allowOutsideClick: false,
      didOpen: () => {
        Swal.showLoading();
      }
    });

    fetch('/examenesevaluate_examan', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(data => {
        // Manejar la respuesta de Django si es necesario
        console.log(data);
        // Redirigir a la siguiente URL con el ID del examen
        const miexamenId = data.miexamen_id;
        window.location.href = `/examenesview_result_examen/${miexamenId}`;
      })
      .catch(error => {
        console.error('Error al enviar los datos:', error);
        // Muestra la alerta de error
        Swal.fire({
          title: 'Error',
          text: 'Hubo un problema al evaluar tu examen. Por favor, contacta a soporte.',
          icon: 'error',
          confirmButtonText: 'Contactar a soporte'
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.href = '/ruta/a/soporte/';  // Cambia esto a la URL de soporte
          }
        });
      });
  }


  // Evento de clic para el botón "Terminar Examen"
  document.getElementById('terminar_examen').addEventListener('click', function () {
    const button = this;

    // Mostrar alerta de confirmación 
    Swal.fire({
      title: '¿Seguro que deseas terminar tu examen?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Sí, terminar',
      cancelButtonText: 'No, cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        // Si el usuario confirma, marcamos que el examen ha sido terminado
        button.dataset.terminado = 'true';

        // Llamamos a la función para recabar la información
        recabarInformacion();
      } else {
        // Si el usuario cancela, no hacemos nada
        Swal.fire('Operación cancelada', 'Puedes continuar con tu examen.', 'info');
      }
    });
  });


  document.getElementById('cancelar-examen').addEventListener('click', function () {
    const button = this;

    // Mostrar alerta de confirmación
    Swal.fire({
      title: '¿Seguro que deseas terminar tu examen?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Sí, terminar',
      cancelButtonText: 'No, cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        // Si el usuario confirma, marcamos que el examen ha sido terminado
        button.dataset.terminado = 'true';

        // Llamamos a la función para recabar la información
        recabarInformacion();
      } else {
        // Si el usuario cancela, no hacemos nada
        Swal.fire('Operación cancelada', 'Puedes continuar con tu examen.', 'info');
      }
    });
  });
});

