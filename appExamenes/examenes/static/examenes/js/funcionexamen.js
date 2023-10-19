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
  startCountdown(15);
});


document.addEventListener('DOMContentLoaded', function () {

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
  const sliderContainer = document.querySelector('.slider-container');
  const sliderWrapper = document.querySelector('.slider-wrapper');
  const sliderItems = document.querySelectorAll('.slider-item');
  const prevLink = document.getElementById('prevLink');
  const nextLink = document.getElementById('nextLink');
  const btn_terminar = document.getElementById('terminar_examen');
  //bara de navegacion
  const progressBar = document.getElementById('progress-bar');
  const totalSlides = 3; // Coloca el total de slides aquí
  let currentSlide = 1; // Coloca el slide actual aquí
  let currentIndex = 0;

  //marca de tiempo
  var tiempoInicioPregunta = new Date().getTime();; // Marca de tiempo al iniciar una pregunta
  var tiemposRespuestas = [];

  function updateSlider() {
    const newPosition = -currentIndex * 100 + '%';
    sliderWrapper.style.transform = 'translateX(' + newPosition + ')';
  }

  function nextSlide() {
    currentIndex = (currentIndex + 1) % sliderItems.length;
    updateSlider();
  }

  function prevSlide() {
    currentIndex = (currentIndex - 1 + sliderItems.length) % sliderItems.length;
    updateSlider();
  }

  nextLink.addEventListener('click', function (event) {


    // Desactivar el enlace "Next" en el último slide
    if ((currentSlide + 1) === totalSlides) {
      btn_terminar.style.display = 'block';
      nextLink.style.display = 'none';
      nextLink.setAttribute('disabled', 'true');
    }
    // Obtener la pregunta actual
    const preguntaActual = 'pregunta-' + currentSlide;

    // Calcular el tiempo que tardó en seleccionar la respuesta
    const tiempoFinPregunta = new Date().getTime();
    const tiempoDiferencia = (tiempoFinPregunta - tiempoInicioPregunta) / 1000; // en segundos

    // Agregar la información al array
    tiemposRespuestas.push({ pregunta: preguntaActual, tiempo: tiempoDiferencia });
    console.log(`Tiempo para seleccionar respuesta (${preguntaActual}): ${tiempoDiferencia} segundos`);


    // Habilitar el enlace "Prev" después de hacer clic en "Next"
    prevLink.removeAttribute('disabled');

    // Actualizar la marca de tiempo al iniciar la siguiente pregunta
    tiempoInicioPregunta = new Date().getTime();

    nextSlide();
    goToNextSlide();

  });

  // Eventos de clic para enlaces "Anterior" y "Siguiente"
  prevLink.addEventListener('click', function (event) {
    // Desactivar el enlace "Prev" en el primer slide
    if ((currentSlide - 1) === 1) {

      prevLink.setAttribute('disabled', 'true');
    }

    // Habilitar el enlace "Next" después de hacer clic en "Prev"
    nextLink.removeAttribute('disabled');
    nextLink.style.display = 'block';
    btn_terminar.style.display = 'none';
    prevSlide();
    goToPrevSlide();

  });

  //FUNCIONES PROGEES BAR

  function updateProgressBar() {
    const percentage = (currentSlide / totalSlides) * 100;
    progressBar.style.width = percentage + '%';
    progressBar.setAttribute('aria-valuenow', percentage);
    progressBar.querySelector('h2').innerText = currentSlide + ' de ' + totalSlides;
  }

  function goToNextSlide() {
    if (currentSlide < totalSlides) {
      currentSlide++;
      updateProgressBar();
    }
  }

  function goToPrevSlide() {
    if (currentSlide > 1) {
      currentSlide--;
      updateProgressBar();
    }
  }
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
      id_examen: id_examen
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
      });
  }


  // Evento de clic para el botón "Terminar Examen"
  document.getElementById('terminar_examen').addEventListener('click', function () {
    // Marcamos que el examen ha sido terminado
    this.dataset.terminado = 'true';

    // Llamamos a la función para recabar la información
    recabarInformacion();
  });

});

