"""
Programa que resuelve un sudoku 4x4 mediante Algoritmos Genéticos.

Tablero Inicial (0 representa una celda vacía):
    [1, 2, X, X]
    [X, X, 2, 1]
    [3, 4, X, X]
    [X, X, 4, 3]
"""

import copy
import random
import time
import tkinter as tk
from tkinter import messagebox

tablero_inicial = [
    [1, 2, 0, 0],
    [0, 0, 2, 1],
    [3, 4, 0, 0],
    [0, 0, 4, 3],
]

celdas_vacias = [
    (i, j) for i in range(4) for j in range(4) if tablero_inicial[i][j] == 0
]


def crear_individuo():
    """
    Crea un individuo aleatorio para el algoritmo genético.
    """
    return [random.randint(1, 4) for _ in range(16)]


def decodificar_individuo(individuo):
    """
    Decodifica un individuo en el tablero de Sudoku.
    """
    tablero = copy.deepcopy(tablero_inicial)
    for idx, (i, j) in enumerate(celdas_vacias):
        tablero[i][j] = individuo[idx]
    return tablero


def calcular_fitness(individuo):
    """
    Calcula el fitness de un individuo en el tablero de Sudoku.
    """
    tablero = decodificar_individuo(individuo)
    fitness = 0

    for i in range(4):
        fitness += len(set(tablero[i]))
        fitness += len(set(tablero[j][i] for j in range(4)))

    for i in (0, 2):
        for j in (0, 2):
            bloque = [tablero[x][y] for x in range(i, i + 2) for y in range(j, j + 2)]
            fitness += len(set(bloque))

    return fitness


def mutar(individuo, tasa_mutacion=0.2):
    """
    Muta un individuo con una tasa de mutación dada.
    """
    for i in range(len(individuo)):
        if random.random() < tasa_mutacion:
            individuo[i] = random.randint(1, 4)


def algoritmo_genetico(tam_poblacion=100, generaciones=1000, callback=None):
    """
    Ejecuta el algoritmo genético para resolver el Sudoku.
    """
    poblacion = [crear_individuo() for _ in range(tam_poblacion)]

    for generacion in range(generaciones):
        poblacion = sorted(poblacion, key=calcular_fitness, reverse=True)

        if calcular_fitness(poblacion[0]) == 48:
            if callback:
                print(f"Solucion encontrada en la generacion {generacion}")
            return decodificar_individuo(poblacion[0])

        nueva_poblacion = poblacion[:10]

        while len(nueva_poblacion) < tam_poblacion:
            padre1, padre2 = random.choices(poblacion[:50], k=2)
            punto_cruce = random.randint(1, len(celdas_vacias) - 1)
            hijo = padre1[:punto_cruce] + padre2[punto_cruce:]
            mutar(hijo)
            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

        if callback and generacion % 100 == 0:
            callback(
                f"Generacion {generacion}, Mejor fitness: {calcular_fitness(poblacion[0])} / 48"
            )

    return None


class SudokoGUI:
    """
    Clase que representa la interfaz gráfica del Sudoku.
    """

    def __init__(self, root):
        """
        Inicializa la interfaz gráfica del Sudoku.
        """
        self.root = root
        self.root.title("Sudoku 4x4 - Algoritmo Genético")
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
                )
                lbl.grid(row=i, column=j, padx=2, pady=2)
                self.celdas[i][j] = lbl

        self.boton_resolver = tk.Button(
            root,
            text="Resolver con Algoritmo Genético",
            command=self.resolver,
            padx=10,
            pady=10,
        )

        self.boton_resolver.pack(pady=5)

        self.boton_limpiar = tk.Button(
            root, text="Limpiar", command=self.limpiar, padx=10, pady=10
        )
        self.boton_limpiar.pack(pady=5)

        self.estado_var = tk.StringVar()
        self.estado_var.set("Listo")
        self.estado_label = tk.Label(root, textvariable=self.estado_var, fg="blue")
        self.estado_label.pack(pady=5)

    def log(self, mensaje):
        """
        Muestra un mensaje en el estado label.
        """
        self.estado_var.set(mensaje)
        self.root.update()

    def resolver(self):
        """
        Resuelve el Sudoku utilizando el algoritmo genético.
        """
        self.boton_resolver.config(state=tk.DISABLED)
        self.boton_limpiar.config(state=tk.DISABLED)
        self.log("Resolviendo...")

        inicio = time.time()
        solucion = algoritmo_genetico(callback=self.log)
        tiempo = time.time() - inicio
        if solucion is None:
            messagebox.showinfo("Error", "No se encontró solución")
        else:
            for i in range(4):
                for j in range(4):
                    self.celdas[i][j].config(text=str(solucion[i][j]), fg="green")
            self.boton_resolver.config(state=tk.NORMAL)
            mensaje = f"¡Sudoku resuelto!\nTiempo: {tiempo:.4f} segundos"
            self.log(mensaje)
            messagebox.showinfo("Éxito", mensaje)
        self.boton_resolver.config(state=tk.NORMAL)
        self.boton_limpiar.config(state=tk.NORMAL)

    def limpiar(self):
        """
        Restaura el tablero a su estado inicial borrando las soluciones.
        """
        for i in range(4):
            for j in range(4):
                valor = tablero_inicial[i][j]
                texto = "" if valor == 0 else str(valor)
                self.celdas[i][j].config(text=texto, fg="black")
        self.log("Tablero reiniciado")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokoGUI(root)
    root.mainloop()
