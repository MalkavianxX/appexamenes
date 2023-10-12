$(document).ready(function() {
  $('.input-group').click(function() {
    // Desactivar la clase 'text-bg-primary' en todos los elementos excepto el clicado
    $('.input-group').not(this).removeClass('text-bg-primary');
    
    // Cambiar la clase 'text-bg-primary' tanto en el input como en el span del elemento clicado
    var clickedElement = $(this);
    $('.input-group').not(clickedElement).find('input, span').removeClass('text-bg-primary');
    clickedElement.toggleClass('text-bg-primary').find('input, span').toggleClass('text-bg-primary');
  });

  $('.img-fluid').click(function() {
    // Abre el modal al hacer clic
    $('#imgmodal').modal('show');
  });

  function startCountdown(minutes) {
    var countdownElement = $("#countdown");
    var totalSeconds = minutes * 60;

    var interval = setInterval(function() {
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
