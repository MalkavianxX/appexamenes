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
        totalSeconds--;
      } else {
        clearInterval(interval);
        countdownElement.html("<strong>0:00</strong>");
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
  //bara de navegacion
  const progressBar = document.getElementById('progress-bar');
  const totalSlides = 3; // Coloca el total de slides aquí
  let currentSlide = 1; // Coloca el slide actual aquí

  let currentIndex = 0;

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

      nextLink.setAttribute('disabled', 'true');
    }

    // Habilitar el enlace "Prev" después de hacer clic en "Next"
    prevLink.removeAttribute('disabled');
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
});