"""
Programa que resuelve un sudoku 4x4 mediante una red neuronal feedforward.

Tablero Inicial (0 representa una celda vacía):
    [1, 2, X, X]
    [X, X, 2, 1]
    [3, 4, X, X]
    [X, X, 4, 3]
"""

import time
import tkinter as tk
from tkinter import messagebox
from turtle import back

import numpy as np

tablero_inicial = [
    [1, 2, 0, 0],
    [0, 0, 2, 1],
    [3, 4, 0, 0],
    [0, 0, 4, 3],
]

# Coordenadas normalizadas para la entrada de la red
coordenadas_entrada = []
for fila in range(4):
    for columna in range(4):
        fila_norm = (fila / 1.5) - 1.0
        columna_norm = (columna / 1.5) - 1.0
        coordenadas_entrada.append([fila_norm, columna_norm])
coordenadas_entrada = np.array(coordenadas_entrada)


def relu(z):
    """
    Calcula la función ReLU.
    """
    return np.maximum(0, z)


def gradiente_relu(z):
    """
    Calcula el gradiente de la función ReLU.
    """
    return (z > 0).astype(float)


def sigmoide(z):
    """
    Calcula la función sigmoide.
    """
    z = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z))


def gradiente_sigmoide(activacion):
    """
    Calcula el gradiente de la función sigmoide.
    """
    return activacion * (1 - activacion)


def inicializar_red(capas):
    """
    Inicializa los parámetros de la red neuronal.
    """
    np.random.seed(42)
    parametros = {}
    for i in range(1, len(capas)):
        n_entrada = capas[i - 1]
        n_salida = capas[i]
        parametros[f"W{i}"] = np.random.randn(n_entrada, n_salida) * np.sqrt(
            2.0 / n_entrada
        )
        parametros[f"b{i}"] = np.zeros((1, n_salida))
    return parametros


def forward(entrada, parametros):
    """
    Realiza el paso hacia adelante para calcular las predicciones de la red neuronal.
    """
    memoria_cache = {"A0": entrada}
    Z1 = entrada @ parametros["W1"] + parametros["b1"]
    A1 = relu(Z1)
    memoria_cache["Z1"], memoria_cache["A1"] = Z1, A1

    Z2 = A1 @ parametros["W2"] + parametros["b2"]
    A2 = relu(Z2)
    memoria_cache["Z2"], memoria_cache["A2"] = Z2, A2

    Z3 = A2 @ parametros["W3"] + parametros["b3"]
    A3 = sigmoide(Z3)
    memoria_cache["Z3"], memoria_cache["A3"] = Z3, A3

    return A3, memoria_cache


def calcular_perdida_y_gradientes(predicciones_red, tablero):
    """
    Calcula la pérdida y los gradientes de los pesos para la red neuronal.
    """
    predicciones = predicciones_red.reshape(4, 4, 4)
    gradientes = np.zeros_like(predicciones)
    perdida_total = 0.0

    for f in range(4):
        for c in range(4):
            valor = tablero[f][c]
            if valor != 0:
                d = valor - 1
                error = predicciones[f, c, d] - 1.0
                gradientes[f, c, d] += error * 5.0
                perdida_total += (error**2) * 2.5
                for d2 in range(4):
                    if d2 != d:
                        error2 = predicciones[f, c, d2]
                        gradientes[f, c, d2] += error2 * 5.0
                        perdida_total += (error2**2) * 2.5

    suma_celda = predicciones.sum(axis=2, keepdims=True)
    gradientes += suma_celda - 1.0
    perdida_total += np.sum((suma_celda - 1.0) ** 2) * 0.5

    suma_fila = predicciones.sum(axis=1, keepdims=True)
    gradientes += suma_fila - 1.0
    perdida_total += np.sum((suma_fila - 1.0) ** 2) * 0.5

    suma_columna = predicciones.sum(axis=0, keepdims=True)
    gradientes += suma_columna - 1.0
    perdida_total += np.sum((suma_columna - 1.0) ** 2) * 0.5

    for bf in range(2):
        for bc in range(2):
            bloque = predicciones[bf * 2 : (bf + 1) * 2, bc * 2 : (bc + 1) * 2, :]
            suma_bloque = bloque.sum(axis=(0, 1), keepdims=True)
            gradientes[bf * 2 : (bf + 1) * 2, bc * 2 : (bc + 1) * 2, :] += (
                suma_bloque - 1.0
            )
            perdida_total += np.sum((suma_bloque - 1.0) ** 2) * 0.5

    return perdida_total, gradientes.reshape(16, 4)


def backward(gradiente_salida, memoria_cache, parametros):
    """
    Realiza el paso hacia atrás para calcular los gradientes de los pesos.
    """
    gradientes_pesos = {}
    dZ3 = gradiente_salida * gradiente_sigmoide(memoria_cache["A3"])
    gradientes_pesos["dW3"] = memoria_cache["A2"].T @ dZ3
    gradientes_pesos["db3"] = dZ3.sum(axis=0, keepdims=True)

    dA2 = dZ3 @ parametros["W3"].T
    dZ2 = dA2 * gradiente_relu(memoria_cache["Z2"])
    gradientes_pesos["dW2"] = memoria_cache["A1"].T @ dZ2
    gradientes_pesos["db2"] = dZ2.sum(axis=0, keepdims=True)

    dA1 = dZ2 @ parametros["W2"].T
    dZ1 = dA1 * gradiente_relu(memoria_cache["Z1"])
    gradientes_pesos["dW1"] = memoria_cache["A0"].T @ dZ1
    gradientes_pesos["db1"] = dZ1.sum(axis=0, keepdims=True)

    return gradientes_pesos


def inicializar_adam(parametros):
    """
    Inicializa los momentos para el algoritmo Adam.
    """
    momento1 = {k: np.zeros_like(p) for k, p in parametros.items()}
    momento2 = {k: np.zeros_like(p) for k, p in parametros.items()}
    return momento1, momento2


def actualizar_adam(
    parametros,
    gradientes,
    momento1,
    momento2,
    paso,
    tasa_aprendizaje=0.01,
    beta1=0.9,
    beta2=0.999,
    epsilon=1e-8,
):
    """
    Actualiza los parámetros de la red neuronal utilizando el algoritmo Adam.
    """
    for clave in parametros:
        g = gradientes[f"d{clave}"]
        momento1[clave] = beta1 * momento1[clave] + (1 - beta1) * g
        momento2[clave] = beta2 * momento2[clave] + (1 - beta2) * (g**2)
        m1_corregido = momento1[clave] / (1 - beta1**paso)
        m2_corregido = momento2[clave] / (1 - beta2**paso)
        parametros[clave] -= (
            tasa_aprendizaje * m1_corregido / (np.sqrt(m2_corregido) + epsilon)
        )
    return parametros, momento1, momento2


def entrenar_red(callback=None):
    """
    Entrena la red neuronal feedforward y devuelve el tablero resuelto (4x4).
    callback(mensaje): función opcional para reportar progreso.
    """
    capas = [2, 64, 64, 4]
    parametros = inicializar_red(capas)
    momento1, momento2 = inicializar_adam(parametros)
    epocas = 3000

    for epoca in range(1, epocas + 1):
        predicciones, memoria_cache = forward(coordenadas_entrada, parametros)
        perdida, gradiente_salida = calcular_perdida_y_gradientes(
            predicciones, tablero_inicial
        )
        gradientes_pesos = backward(gradiente_salida, memoria_cache, parametros)
        parametros, momento1, momento2 = actualizar_adam(
            parametros, gradientes_pesos, momento1, momento2, epoca
        )

        if callback and (epoca % 200 == 0 or epoca == 1):
            callback(f"Época {epoca:>4} | Pérdida {perdida:.4f}")

        if perdida < 0.05:
            if callback:
                callback(f"Convergencia en época {epoca} (pérdida {perdida:.5f})")
            break

    predicciones_finales, _ = forward(coordenadas_entrada, parametros)
    predicciones_3d = predicciones_finales.reshape(4, 4, 4)
    tablero_resuelto = (np.argmax(predicciones_3d, axis=-1) + 1).astype(int)
    return tablero_resuelto.tolist()


class SudokuNeuralGUI:
    """
    Interfaz gráfica para resolver Sudoku utilizando una red neuronal feedforward.
    """

    def __init__(self, root):
        """
        Inicializa la interfaz gráfica y configura los componentes.
        """
        self.root = root
        self.root.title("Sudoku 4x4 - Red Neuronal")
        self.root.resizable(False, False)

        self.tablero_frame = tk.LabelFrame(root, text="Tablero", padx=10, pady=10)
        self.tablero_frame.pack(pady=10)

        self.celdas = [[None for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                valor = tablero_inicial[i][j]
                texto = "" if valor == 0 else str(valor)
                lbl = tk.Label(
                    self.tablero_frame,
                    text=texto,
                    font=("Arial", 20, "bold"),
                    width=3,
                    height=1,
                    relief="ridge",
                    bg="white",
                    fg="black",
                )
                lbl.grid(row=i, column=j, padx=2, pady=2)
                self.celdas[i][j] = lbl

        self.boton_resolver = tk.Button(
            root,
            text="Resolver con Red Neuronal",
            command=self.resolver,
            padx=10,
            pady=5,
        )
        self.boton_resolver.pack(pady=5)

        self.boton_limpiar = tk.Button(
            root, text="Limpiar", command=self.limpiar, padx=10, pady=5
        )
        self.boton_limpiar.pack(pady=5)

        self.estado_var = tk.StringVar()
        self.estado_var.set("Listo")
        self.estado_lbl = tk.Label(root, textvariable=self.estado_var, fg="blue")
        self.estado_lbl.pack(pady=5)

    def log(self, mensaje):
        """Actualiza la barra de estado."""
        self.estado_var.set(mensaje)
        self.root.update()

    def resolver(self):
        """Ejecuta el entrenamiento de la red neuronal y muestra la solución."""
        self.boton_resolver.config(state=tk.DISABLED)
        self.boton_limpiar.config(state=tk.DISABLED)
        self.log("Entrenando red neuronal...")

        inicio = time.time()
        solucion = entrenar_red(callback=self.log)
        tiempo = time.time() - inicio

        if solucion is None:
            mensaje = "No se pudo encontrar una solución."
            self.log(mensaje)
            messagebox.showerror("Error", mensaje)
        else:
            for i in range(4):
                for j in range(4):
                    valor = solucion[i][j]
                    self.celdas[i][j].config(text=str(valor), fg="green")
            mensaje = f"¡Sudoku resuelto!\nTiempo: {tiempo:.4f} segundos"
            self.log(mensaje)
            messagebox.showinfo("Éxito", mensaje)

        self.boton_resolver.config(state=tk.NORMAL)
        self.boton_limpiar.config(state=tk.NORMAL)

    def limpiar(self):
        """Restaura el tablero a las pistas originales."""
        for i in range(4):
            for j in range(4):
                valor = tablero_inicial[i][j]
                texto = "" if valor == 0 else str(valor)
                self.celdas[i][j].config(text=texto, fg="black")
        self.log("Tablero reiniciado")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuNeuralGUI(root)
    root.mainloop()
