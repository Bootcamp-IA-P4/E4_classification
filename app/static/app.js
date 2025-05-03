document.getElementById("formulario-prediccion").addEventListener("submit", async function(e) {
    e.preventDefault();
    const form = e.target;
    const datos = new FormData(form);
    const resultadoDiv = document.getElementById("resultado");
    resultadoDiv.innerHTML = "Procesando...";
    try {
        const resp = await fetch("/predecir", {
            method: "POST",
            body: datos
        });
        const data = await resp.json();
        resultadoDiv.innerHTML = `
            <div class="mensaje">
                <h2>Resultado:</h2>
                <p><strong>Probabilidad de enfermedad cardíaca:</strong> ${Math.round(data.probabilidad*100)}%</p>
                <p><strong>Riesgo:</strong> ${data.riesgo}</p>
                <p>${data.mensaje}</p>
            </div>
        `;
    } catch (err) {
        resultadoDiv.innerHTML = "<span style='color:red'>Error al procesar la predicción.</span>";
    }
});
