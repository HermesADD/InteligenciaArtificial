Nombre: Hermes Alberto Delgado Díaz
Número de cuenta: 319258613

======================================
PROGRAMA PROPUESTO POR RICHARD DAWKINS
======================================

El objetivo de este programa es tratar de poner a un mono a escribir aleatoriamente en 
una máquina de escribir con el alfabeto (26 letras en mayúsculas) y el espacio.
La frase que debe encontrar el sistema es: METHINKS IT IS LIKE A WEASEL.

--- ALGORITMO ---
Es un algoritmo evolutivo con las siguientes reglas:
1. Comienza con una cadena de texto (puede ser generada al azar o por el usuario).
2. Se clona esta cadena 100 veces.
3. Cada carácter de cada clon tiene un 5% de probabilidad de mutar.
4. Se compara cada clon con la cadena objetivo y el que obtenga la mayor puntuación 
se convierte en el padre de la siguiente generación.
5. El ciclo se repite hasta alcanzar la puntuación perfecta, es decir, que sea exactamente 
igual a la cadena objetivo.

--- INTERFAZ ---
- El usuario puede cambiar la frase objetivo por la que él desee.
- Se puede empezar con una cadena inicial aleatoria o que el usuario ingrese una manualmente.
- Uso de IA: La programación y la lógica central del algoritmo son totalmente mías. 
Originalmente desarrollé el código para ejecutarse en la terminal con Python. 
Dado que sé programar en JavaScript para adaptar la lógica al navegador, me apoyé 
en Inteligencia Artificial de manera exclusiva para estructurar el entorno visual (HTML y CSS) y 
construir la interfaz gráfica. Mi objetivo con esto fue hacer que el programa sea más interactivo, accesible 
y fácil de probar desde cualquier navegador web, sin obligar al usuario a instalar 
lenguajes de programación o librerías adicionales.

--- EJECUCIÓN ---
No se necesita instalar nada. Solo se descarga la carpeta Tarea02 con los archivos 
(index.html, style.css, dawkins.js), se da doble clic al archivo index.html 
(o le das clic derecho y "Abrir con") y se ejecutará en cualquier navegador web.