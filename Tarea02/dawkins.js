/**
 * @constant {string} Alfabeto válido: letras mayúsculas A-Z más el espacio. 
 * Los caracteres de todas cadenas deben pertenecer a este alfabeto.
 */
const ABECEDARIO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";

/** @type {number} Número de generaciones completadas desde el inicio. */
let generacion = 0;

/** @type {string} Cadena con mayor puntaje en la generación actual. */
let mejorCadena = "";

/** @type {boolean} Indica si hay una simulación en curso; evita ejecuciones simultáneas. */
let enProceso = false;

/** @type {string} Frase objetivo normalizada (mayúsculas, sin caracteres inválidos). */
let objetivo = "";

/** @type {number} Longitud de la frase objetivo; se cachea para evitar recalcularla. */
let objLen = 0;

/** @type {number|null} ID del setTimeout activo; permite cancelar el ciclo si fuera necesario. */
let timeoutId = null;

const entradaObjetivo = document.getElementById("entradaObjetivo");
const ayudaObjetivo = document.getElementById("ayudaObjetivo");
const opcionAleatoria = document.getElementById("opcionAleatoria");
const opcionManual = document.getElementById("opcionManual");
const entradaCadena = document.getElementById("entradaCadena");
const ayudaManual = document.getElementById("ayudaManual");
const btnIniciar = document.getElementById("btnIniciar");
const txtSalida = document.getElementById("txtSalida");

entradaObjetivo.addEventListener("focus", () => {
    ayudaObjetivo.classList.add("texto-resaltado");
});
entradaObjetivo.addEventListener("blur", () => {
    ayudaObjetivo.classList.remove("texto-resaltado");
});

/**
 * Habilita o deshabilita el campo de cadena manual según la opción
 * de radio activa, y gestiona el resaltado del texto de ayuda asociado.
 */
function actualizarModalidad() {
    if (opcionManual.checked) {
        entradaCadena.disabled = false;
        entradaCadena.focus();
        ayudaManual.classList.add("texto-resaltado");
    } else {
        entradaCadena.disabled = true;
        ayudaManual.classList.remove("texto-resaltado");
    }
}

opcionAleatoria.addEventListener("change", actualizarModalidad);
opcionManual.addEventListener("change", actualizarModalidad);

/**
 * Convierte la entrada a mayúsculas y filtra todo carácter que no sea
 * una letra A–Z ni un espacio. Se aplica tanto a la cadena objetivo
 * como a la cadena de inicio manual.
 *
 * @param   {string} cadena Texto de entrada sin restricciones.
 * @returns {string} Cadena en mayúsculas con solo caracteres válidos.
 */
function limpiarCadena(cadena) {
    return cadena.toUpperCase().split('').filter(c => ABECEDARIO.includes(c)).join('');
}

/**
 * Genera una cadena aleatoria del mismo largo que la frase objetivo.
 *
 * @returns {string} Cadena aleatoria de longitud {@link objLen}.
 */
function generarAleatoria() {
    let resultado = "";
    for (let i = 0; i < objLen; i++) {
        const indiceAleatorio = Math.floor(Math.random() * ABECEDARIO.length);
        resultado += ABECEDARIO[indiceAleatorio];
    }
    return resultado;
}

/**
 * Calcula el puntaje de una cadena como el número de posiciones en que 
 * coincide con la cadena objetivo.
 * @param {string} cadena Cadena candidata a puntuar. 
 * @returns {number} Número de caracteres que coinciden posición a posición con {@link objetivo}
 */
function puntaje(cadena) {
    let puntos = 0;
    for (let i = 0; i < objLen; i++) {
        if (cadena[i] === objetivo[i]) {
            puntos++;
        }
    }
    return puntos;
}

/**
 * Aplica mutación aleatoria a cada carácter de la cadena con una probabilidad
 * del 5% por posición.
 * @param   {string} cadena Cadena padre sobre la que se aplican las mutaciones.
 * @returns {string} Nueva cadena resultante de la mutación.
 */
function mutar(cadena) {
    let resultado = "";
    for (let i = 0; i < cadena.length; i++) {
        if (Math.random() < 0.05) { 
            const indiceAleatorio = Math.floor(Math.random() * ABECEDARIO.length);
            resultado += ABECEDARIO[indiceAleatorio];
        } else {
            resultado += cadena[i];
        }
    }
    return resultado;
}

btnIniciar.addEventListener("click", () => {
    if (enProceso) return;

    txtSalida.value = ""; 

    objetivo = limpiarCadena(entradaObjetivo.value);
    objLen = objetivo.length;

    if (objLen === 0) {
        alert("La frase objetivo no puede estar vacía o tener puros caracteres inválidos.");
        return;
    }

    entradaObjetivo.value = objetivo; 

    if (opcionAleatoria.checked) {
        mejorCadena = generarAleatoria();
    } else {
        let cadenaUsuario = limpiarCadena(entradaCadena.value);
        if (cadenaUsuario.length !== objLen) {
            alert(`La cadena debe tener exactamente ${objLen} caracteres válidos.\nTu cadena tiene ${cadenaUsuario.length} caracteres.`);
            return;
        }
        mejorCadena = cadenaUsuario;
    }

    generacion = 0;
    enProceso = true;
    btnIniciar.disabled = true;
    entradaObjetivo.disabled = true;

    evolucionar();
});

/**
 * Ejecuta una generación del algoritmo y programa la siguiente.
 */
function evolucionar() {
    if (!enProceso) return;

    const puntajeActual = puntaje(mejorCadena);
    
    const genFormateada = generacion.toString().padStart(3, '0');
    
    txtSalida.value += `Gen ${genFormateada} | ${mejorCadena} | Puntos: ${puntajeActual}\n`;
    txtSalida.scrollTop = txtSalida.scrollHeight;

    if (puntajeActual === objLen) {
        enProceso = false;
        btnIniciar.disabled = false;
        entradaObjetivo.disabled = false;
        txtSalida.value += `\n¡Evolución completada con éxito en ${generacion} generaciones!\n`;
        return;
    }

    let poblacion = [mejorCadena]; 
    for (let i = 0; i < 100; i++) {
        poblacion.push(mutar(mejorCadena));
    }

    mejorCadena = poblacion.reduce((mejor, actual) => {
        return puntaje(actual) > puntaje(mejor) ? actual : mejor;
    });

    generacion++;

    timeoutId = setTimeout(evolucionar, 10);
}