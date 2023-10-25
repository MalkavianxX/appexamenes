function hexToRGB(t, e) {
  var a = parseInt(t.slice(1, 3), 16),
    i = parseInt(t.slice(3, 5), 16),
    t = parseInt(t.slice(5, 7), 16);
  return e
    ? "rgba(" + a + ", " + i + ", " + t + ", " + e + ")"
    : "rgb(" + a + ", " + i + ", " + t + ")";
}
function skipped(t, e) {
  return t.p0.skip || t.p1.skip ? e : void 0;
}
function down(t, e) {
  return t.p0.parsed.y > t.p1.parsed.y ? e : void 0;
}
!(function (a) {
  "use strict";
  function t() {
    (this.$body = a("body")),
      (this.charts = []),
      (this.defaultColors = ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"]);
  }

    (t.prototype.pointStylingExample = function () {
      var t = document.getElementById("point-styling-example"),
        e = t.getAttribute("data-colors"),
        e = e ? e.split(",") : this.defaultColors,
        t = t.getContext("2d"),
        t = new Chart(t, {
          type: "line",
          data: {
            labels: ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"],
            datasets: [
              {
                label: "Examenes realizados",
                data: [1,5,7,3,9,0,52],
                borderColor: e[0],
                pointStyle: "circle",
                pointRadius: 10,
                pointHoverRadius: 15,
              },
            ],
          },
          options: {
            responsive: !0,
            maintainAspectRatio: !1,
            plugins: { legend: { display: !1 } },
            scales: {
              x: { stacked: !0, grid: { display: !1 } },
              y: { stacked: !0, grid: { display: !1 } },
            },
          },
        });
      this.charts.push(t);
    }),

    (t.prototype.init = function () {
      var e = this;
      (Chart.defaults.font.family =
        '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif'),
        (Chart.defaults.color = "#8391a2"),
        (Chart.defaults.borderColor = "rgba(133, 141, 152, 0.1)"),

        this.pointStylingExample(),
 
        a(window).on("resizeEnd", function (t) {
          a.each(e.charts, function (t, e) {
            try {
              e.destroy();
            } catch (t) {}
          }),
  
            e.pointStylingExample();
   
        }),
        a(window).resize(function () {
          this.resizeTO && clearTimeout(this.resizeTO),
            (this.resizeTO = setTimeout(function () {
              a(this).trigger("resizeEnd");
            }, 500));
        });
    }),
    (a.ChartJs = new t()),
    (a.ChartJs.Constructor = t);
})(window.jQuery),
  (function () {
    "use strict";
    window.jQuery.ChartJs.init();
  })();
