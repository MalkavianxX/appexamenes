function convertirJsonString(jsonObj) {
    // Obtiene las claves y valores
    var jsonObj = JSON.parse(jsonObj.value);

    console.log(jsonObj);
    var keys = Object.keys(jsonObj);
    console.log(keys);
    var values = Object.values(jsonObj);

    // Convierte las claves a un formato adecuado (capitalizando la primera letra)
    var labels = keys.map(function (key) {
        return key.charAt(0).toUpperCase() + key.slice(1);
    });

    // Devuelve un array con las etiquetas y datos
    return [labels, values];
}
var labels_categorias = convertirJsonString(document.getElementById("categorias_por_examen"));
var labels_examenes_errores= convertirJsonString(document.getElementById("examenes_respuestas_equivocadas"));
var colors = ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"],
    dataColors = $("#campaign-sent-chart").data("colors"),
    options1 = {
        chart: { type: "bar", height: 60, sparkline: { enabled: !0 } },
        plotOptions: { bar: { columnWidth: "60%" } },
        colors: (colors = dataColors ? dataColors.split(",") : colors),
        series: [{ data: [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54] }],
        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        xaxis: { crosshairs: { width: 1 } },
        tooltip: {
            fixed: { enabled: !1 },
            x: { show: !1 },
            y: {
                title: {
                    formatter: function (o) {
                        return "";
                    },
                },
            },
            marker: { show: !1 },
        },
    },
    colors =
        (new ApexCharts(
            document.querySelector("#campaign-sent-chart"),
            options1
        ).render(),
            ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"]),
    dataColors = $("#new-leads-chart").data("colors"),
    options2 = {
        chart: { type: "line", height: 60, sparkline: { enabled: !0 } },
        series: [{ data: [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54] }],
        stroke: { width: 2, curve: "smooth" },
        markers: { size: 0 },
        colors: (colors = dataColors ? dataColors.split(",") : colors),
        tooltip: {
            fixed: { enabled: !1 },
            x: { show: !1 },
            y: {
                title: {
                    formatter: function (o) {
                        return "";
                    },
                },
            },
            marker: { show: !1 },
        },
    },
    colors =
        (new ApexCharts(
            document.querySelector("#new-leads-chart"),
            options2
        ).render(),
            ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"]),
    dataColors = $("#deals-chart").data("colors"),
    options3 = {
        chart: { type: "bar", height: 60, sparkline: { enabled: !0 } },
        plotOptions: { bar: { columnWidth: "60%" } },
        colors: (colors = dataColors ? dataColors.split(",") : colors),
        series: [{ data: [12, 14, 2, 47, 42, 15, 47, 75, 65, 19, 14] }],
        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        xaxis: { crosshairs: { width: 1 } },
        tooltip: {
            fixed: { enabled: !1 },
            x: { show: !1 },
            y: {
                title: {
                    formatter: function (o) {
                        return "";
                    },
                },
            },
            marker: { show: !1 },
        },
    },
    colors =
        (new ApexCharts(document.querySelector("#deals-chart"), options3).render(),
            ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"]),
    dataColors = $("#booked-revenue-chart").data("colors"),
    options4 = {
        chart: { type: "bar", height: 60, sparkline: { enabled: !0 } },
        plotOptions: { bar: { columnWidth: "60%" } },
        colors: (colors = dataColors ? dataColors.split(",") : colors),
        series: [{ data: [47, 45, 74, 14, 56, 74, 14, 11, 7, 39, 82] }],
        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        xaxis: { crosshairs: { width: 1 } },
        tooltip: {
            fixed: { enabled: !1 },
            x: { show: !1 },
            y: {
                title: {
                    formatter: function (o) {
                        return "";
                    },
                },
            },
            marker: { show: !1 },
        },
    },
    colors =
        (new ApexCharts(
            document.querySelector("#booked-revenue-chart"),
            options4
        ).render(),
            ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"]),
    dataColors = $("#dash-campaigns-chart").data("colors"),
    options = {
        series: [{
            data: labels_categorias[1],
            name: "Examenes",
        }],
        chart: {
            type: 'bar',
            height: 350
        },


        plotOptions: {
            bar: {
                borderRadius: 4,
                horizontal: true,
            }
        },
        dataLabels: {
            enabled: true
        },
        xaxis: {
            type: 'category',
            categories: labels_categorias[0],
        },
        colors: (colors = dataColors ? dataColors.split(",") : colors),
        responsive: [
            {
                breakpoint: 600,
                options: { xaxis: { show: !1 }, legend: { show: !1 } },
            },
        ],

    },
    chart = new ApexCharts(
        document.querySelector("#dash-campaigns-chart"),
        options
    ),
    colors = (chart.render());


//buble chart


      
var optionsa = {
    series: [{
    name: 'Inflation',
    data: labels_examenes_errores[1]
  }],
    chart: {
    height: 350,
    type: 'bar',
  },
  plotOptions: {
    bar: {
      borderRadius: 10,
      dataLabels: {
        position: 'top', // top, center, bottom
      },
    }
  },
  dataLabels: {
    enabled: true,
    formatter: function (val) {
      return val + "errores";
    },
    offsetY: -20,
    style: {
      fontSize: '12px',
      colors: ["#304758"]
    }
  },
  
  xaxis: {
    categories: labels_examenes_errores[0],
    position: 'top',
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false
    },
    crosshairs: {
      fill: {
        type: 'gradient',
        gradient: {
          colorFrom: '#D8E3F0',
          colorTo: '#BED1E6',
          stops: [0, 100],
          opacityFrom: 0.4,
          opacityTo: 0.5,
        }
      }
    },
    tooltip: {
      enabled: true,
    }
  },
  yaxis: {
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false,
    },
    labels: {
      show: false,
      formatter: function (val) {
        return val + "%";
      }
    }
  
  },
  title: {
    text: 'Monthly Inflation in Argentina, 2002',
    floating: true,
    offsetY: 330,
    align: 'center',
    style: {
      color: '#444'
    }
  }
  };

  var chart = new ApexCharts(document.querySelector("#dash-buble-chart"), optionsa);
  chart.render();

