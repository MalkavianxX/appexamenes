$(document).ready(function () {
    "use strict";
    var a = $("#datatable-buttons").DataTable({
      lengthChange: !1,
      buttons: ["copy", "print"],
      language: {
        paginate: {
          previous: "<i class='mdi mdi-chevron-left'>",
          next: "<i class='mdi mdi-chevron-right'>",
        },
      },
      drawCallback: function () {
        $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
      },
    });
  
      a
        .buttons()
        .container()
        .appendTo("#datatable-buttons_wrapper .col-md-6:eq(0)"),
      $("#alternative-page-datatable").DataTable({
          language: {
              "decimal": "",
              "emptyTable": "No hay información",
              "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
              "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
              "infoFiltered": "(Filtrado de _MAX_ total entradas)",
              "infoPostFix": "",
              "thousands": ",",
              "lengthMenu": "Mostrar _MENU_ Entradas",
              "loadingRecords": "Cargando...",
              "processing": "Procesando...",
              "search": "Buscar:",
              "zeroRecords": "Sin resultados encontrados",
              "paginate": {
                  "first": "Primero",
                  "last": "Ultimo",
                  previous: "<i class='mdi mdi-chevron-left'>",
                  next: "<i class='mdi mdi-chevron-right'>",
              }
          },
        pagingType: "full_numbers",
        drawCallback: function () {
          $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
        },
      }),
      $(".dataTables_length select").addClass("form-select form-select-sm"),
      $(".dataTables_length label").addClass("form-label");
  });
  
  
  document.addEventListener('DOMContentLoaded', function () {
    const examenRows = document.querySelectorAll('[id^="invrow_"]');
    
    examenRows.forEach(row => {
        row.addEventListener('mouseover', function () {
            this.classList.add('bg-primary-lighten', 'cursor-pointer','text-primary');
        });
  
        row.addEventListener('mouseout', function () {
            this.classList.remove('bg-primary-lighten', 'cursor-pointer','text-primary');
        });
        // Agrega un evento de clic a la fila
        row.addEventListener('click', function () {
            // Obtiene la última celda de la fila
            var celda = this.cells[this.cells.length - 1];
            // Crea un nuevo textarea temporal
            var tempElemento = document.createElement('textarea');
            // Establece el valor del textarea al texto de la celda
            tempElemento.value = celda.textContent;
            // Añade el textarea al DOM
            document.body.appendChild(tempElemento);
            // Selecciona el texto del textarea
            tempElemento.select();
            // Copia el texto al portapapeles
            document.execCommand('copy');
            // Elimina el textarea temporal
            document.body.removeChild(tempElemento);
            
            // Crea una alerta de Bootstrap
            var alerta = document.createElement('div');
            alerta.className = 'alert alert-success';
            alerta.textContent = 'Link copiado al portapapeles';
            
            // Establece el estilo de la alerta para que aparezca en la parte superior de la página, centrada y por encima de los demás elementos
            alerta.style.position = 'fixed';
            alerta.style.top = '30px';
            alerta.style.left = '50%';
            alerta.style.transform = 'translateX(-50%)';
            alerta.style.zIndex = '9999';
            
            // Añade la alerta al DOM
            document.body.appendChild(alerta);
            
            // Hace que la alerta se desaparezca después de 2 segundos
            setTimeout(function() {
                alerta.remove();
            }, 2000);
        });
        
    });
  });
  