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
  const examenRows = document.querySelectorAll('[id^="userrow_"]');
  
  examenRows.forEach(row => {
      row.addEventListener('mouseover', function () {
          this.classList.add('bg-primary-lighten', 'cursor-pointer','text-primary');
      });

      row.addEventListener('mouseout', function () {
          this.classList.remove('bg-primary-lighten', 'cursor-pointer','text-primary');
      });

      row.addEventListener('click', function () {
          const examenId = this.id.split('_')[1];
          window.location.href = `/usuariosview_my_perfil/${examenId}`;
      });
  });

  
});
