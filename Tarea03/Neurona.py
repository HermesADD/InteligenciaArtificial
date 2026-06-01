"""
Neurona Aspirante 

Clasificados para diferenciar entre Naranajas y Manzanas.
"""
import math
import random

def sigmoide(z):
    # Calcula la función de activación sigmoide.
    return 1.0 / (1.0 + math.exp(-z))

def derivada_sigmoide(z):
    # Calcula la derivada de la función sigmoide respecto a su salida.
    return z * (1.0 - z)

datos_entrenamiento = [
    [0.85, 0.92, 1],   # Naranja  — pesada y muy rugosa
    [0.15, 0.12, 0],   # Manzana  — ligera y lisa
    [0.78, 0.85, 1],   # Naranja  — pesada y rugosa
    [0.25, 0.30, 0],   # Manzana  — ligera y poco rugosa
    [0.91, 0.75, 1],   # Naranja  — muy pesada y rugosa
    [0.10, 0.45, 0],   # Manzana  — muy ligera, textura media
    [0.82, 0.65, 1],   # Naranja  — pesada, textura media-alta
    [0.35, 0.08, 0],   # Manzana  — ligera y muy lisa
    [0.68, 0.95, 1],   # Naranja  — peso medio-alto y muy rugosa
    [0.42, 0.25, 0],   # Manzana  — peso medio-bajo y lisa
    [0.55, 0.52, 1],   # Naranja  — caso ambiguo: peso y textura medios (naranja)
    [0.48, 0.45, 0],   # Manzana  — caso ambiguo: peso y textura medios (manzana)
]

random.seed(42)
w1 = random.uniform(-1, 1)
w2 = random.uniform(-1, 1)
b = random.uniform(-1, 1)

tasa_aprendizaje = 0.5
epocas = 1000

def feedforward(x1, x2, w1, w2, b):
    # Calcula la suma ponderada y la pasa por el sigmoide.
    z = w1 * x1 + w2 * x2 + b
    return sigmoide(z)

def ecm(datos, w1, w2, b):
    # Calcula el Error Cuadrático Medio sobre el dataset.
    total_error = 0.0
    for muestra in datos:
        x1, x2, etiqueta = muestra 
        prediccion = feedforward(x1,x2,w1,w2,b)
        total_error += (etiqueta - prediccion) **2
    return total_error / len(datos) 

#====================== ENTRENAMIENTO ======================= 
print("Iniciando con el entrenamiento...")

for epoca in range(1,epocas + 1):
    for x1, x2, etiqueta in datos_entrenamiento:
        prediccion = feedforward(x1,x2,w1,w2,b)
        
        error = prediccion - etiqueta
        
        gradiente = error*derivada_sigmoide(prediccion)
        
        w1 -= tasa_aprendizaje * gradiente * x1
        w2 -= tasa_aprendizaje * gradiente * x2
        b -= tasa_aprendizaje * gradiente * 1
        
    if epoca % 100 == 0:
        error_actual = ecm(datos_entrenamiento, w1, w2, b)
        print(f"Epoca {epoca:4d} | Error: {error_actual:.6f}")

#=============== RESULTADOS DEL ENTRENAMIENTO ================ 
        
print("\nEl entrenamiento ha terminado.")
print("Pesos finales") 
print(f"w1: {w1:.4f}")
print(f"w2: {w2:.4f}")
print(f"b: {b:.4f}")


#================ PRUEBA CON UNA NUEVA FRUTA ================= 
print("=========== Prueba ===========")
x1_prueba = 0.85
x2_prueba = 0.80

prediccion_final = feedforward(x1_prueba, x2_prueba, w1,w2,b)

print(f"Entrada\n", f"\tPeso: {x1_prueba}\n", f"\tTextura: {x2_prueba}")
print(f"Probabilidad de ser Naranja: {prediccion_final:.4f}")

if prediccion_final <= 0.5:
    print("Es una Manzana!")
else:
    print("Es una Naranja!")

        