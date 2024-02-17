var quill = new Quill("#snow-editor", {
    theme: "snow",
    modules: {
        toolbar: false,
    },
    readOnly: true,
});

// Ajusta el tamaño de la letra del editor snow a 20px
document.querySelector("#snow-editor .ql-editor").style.fontSize = "20px";

// Justificar el texto
quill.format("align", "justify");
