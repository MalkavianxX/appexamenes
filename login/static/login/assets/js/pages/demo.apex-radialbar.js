var resultado = parseInt(document.getElementById('examen_resultado').value) *10;
var numpreguntas = parseInt(document.getElementById('num_preguntas').value);
console.log(resultado);
var colors = ["#727cf5"],
dataColors = $("#gradient-chart").data("colors"),
options = {
    chart: { height: 330, type: "radialBar" },
    plotOptions: {
      radialBar: {
        startAngle: -135,
        endAngle: 225,
        hollow: {
          margin: 0,
          size: "70%",
          background: "transparent",
          image: void 0,
          imageOffsetX: 0,
          imageOffsetY: 0,
          position: "front",
          dropShadow: { enabled: true, top: 3, left: 0, blur: 4, opacity: 0.24 },
        },
        track: {
          background: "rgba(170,184,197, 0.2)",
          strokeWidth: "67%",
          margin: 0,
        },
        dataLabels: {
          showOn: "always",
          name: { offsetY: -10, show: true, color: "#888", fontSize: "17px" },
          value: {
            formatter: function (a) {
              return parseInt(a);
            },
            color: "#111",
            fontSize: "36px",
            show: true,
          },
        },
      },
    },
    fill: {
      type: "gradient",
      gradient: {
        shade: "dark",
        type: "horizontal",
        shadeIntensity: 0.5,
        gradientToColors: (colors = dataColors
          ? dataColors.split(",")
          : colors),
        inverseColors: true,
        opacityFrom: 1,
        opacityTo: 1,
        stops: [0, 100],
      },
    },
    series: [resultado],
    stroke: { lineCap: "round" },
    labels: ["Calificación"],
  };

var chart = new ApexCharts(
  document.querySelector("#gradient-chart"),
  options
);
chart.render();
