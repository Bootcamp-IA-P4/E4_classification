// Funcionalidad para los botones extra

document.addEventListener('DOMContentLoaded', function() {
    const formulario = document.getElementById('formulario-prediccion');
    const resultado = document.getElementById('resultado');
    const botonesExtra = document.querySelector('.botones-extra');
    const mensajeFinal = document.getElementById('mensaje-final');
    const btnNueva = document.getElementById('btn-nueva-prediccion');
    const btnFinalizar = document.getElementById('btn-finalizar');

    // Ocultar botones extra al inicio
    botonesExtra.style.display = 'none';

    formulario.onsubmit = function(e) {
        e.preventDefault();
        // Aquí deberías poner la lógica real de predicción y mostrar el resultado
        // Por ejemplo, simular un resultado:
        resultado.innerHTML = '<strong>Bajo riesgo de enfermedad cardíaca</strong>';
        resultado.style.display = 'block';
        botonesExtra.style.display = 'flex';
        mensajeFinal.style.display = 'none';
    };

    btnNueva.onclick = function() {
        formulario.reset();
        resultado.innerHTML = '';
        resultado.style.display = 'none';
        botonesExtra.style.display = 'none';
        mensajeFinal.style.display = 'none';
    };

    btnFinalizar.onclick = function() {
        mensajeFinal.innerText = 'Muchas gracias por elegirnos, que tenga un excelente día';
        mensajeFinal.style.display = 'block';
        resultado.innerHTML = '';
        resultado.style.display = 'none';
        botonesExtra.style.display = 'none';
    };
});
