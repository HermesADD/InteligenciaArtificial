import random
import time
import sys

# Alfabeto válido: letras mayúsculas A-Z más el espacio.
ABECEDARIO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

class MonoEscritor:
    """
    Clase que encapsula el algoritmo de Dawkins para ejecutarse en terminal.
    """
    def __init__(self):
        self.objetivo = "METHINKS IT IS LIKE A WEASEL"
        self.obj_len = len(self.objetivo)
        self.mejor_cadena = ""
        self.generacion = 0

    def limpiar_cadena(self, cadena: str) -> str:
        """Filtra la cadena para dejar solo letras mayúsculas y espacios."""
        return ''.join(c for c in cadena.upper() if c in ABECEDARIO)

    def configurar_objetivo(self):
        """Permite al usuario cambiar el objetivo o dejar el de por defecto."""
        print("\n--- CONFIGURACIÓN DEL OBJETIVO ---")
        print(f"Objetivo actual por defecto: '{self.objetivo}'")
        nuevo = input("Presiona Enter para usar el actual, o escribe una nueva frase objetivo: ")
        
        if nuevo.strip() != "":
            nuevo_limpio = self.limpiar_cadena(nuevo)
            if len(nuevo_limpio) > 0:
                self.objetivo = nuevo_limpio
                self.obj_len = len(self.objetivo)
                print(f"-> Nuevo objetivo configurado: '{self.objetivo}'")
            else:
                print("-> Entrada inválida. Se mantendrá el objetivo por defecto.")
        else:
            print("-> Se usará el objetivo por defecto.")

    def cadena_random(self) -> str:
        """Genera una cadena aleatoria de longitud igual a la del objetivo."""
        return ''.join(random.choice(ABECEDARIO) for _ in range(self.obj_len))

    def puntaje(self, cadena: str) -> int:
        """Calcula cuántas letras coinciden en su posición exacta con el objetivo."""
        return sum(1 for a, b in zip(cadena, self.objetivo) if a == b)

    def mutar(self, cadena: str) -> str:
        """Aplica un 5% de probabilidad de mutación a cada carácter."""
        resultado = ""
        for char in cadena:
            if random.random() < 0.05:
                resultado += random.choice(ABECEDARIO)
            else:
                resultado += char
        return resultado

    def configurar_inicio(self):
        """Permite al usuario elegir entre cadena aleatoria o manual."""
        print("\n--- CONFIGURACIÓN DE INICIO ---")
        print("1. Generar cadena inicial aleatoria")
        print("2. Ingresar cadena inicial manualmente")
        
        while True:
            opcion = input("Elige una opción (1 o 2): ").strip()
            
            if opcion == '1':
                self.mejor_cadena = self.cadena_random()
                break
            elif opcion == '2':
                print(f"\nTu cadena debe tener EXACTAMENTE {self.obj_len} caracteres válidos (letras y espacios).")
                while True:
                    cadena_usr = input(f"Ingresa tu cadena de {self.obj_len} caracteres: ")
                    cadena_limpia = self.limpiar_cadena(cadena_usr)
                    
                    if len(cadena_limpia) == self.obj_len:
                        self.mejor_cadena = cadena_limpia
                        break
                    else:
                        print(f"[Error] Tu cadena tiene {len(cadena_limpia)} caracteres válidos. Intenta de nuevo.")
                break
            else:
                print("[Error] Opción no válida. Por favor, escribe 1 o 2.")

    def evolucionar(self):
        """Ciclo principal de evolución en terminal."""
        print("\n================ INICIANDO EVOLUCIÓN ================\n")
        self.generacion = 0
        
        # Pequeño retraso para que el usuario alcance a leer
        time.sleep(1)

        while True:
            puntaje_actual = self.puntaje(self.mejor_cadena)
            
            # Imprimir estado de la generación (usamos \r para sobrescribir la línea si queremos, 
            # pero imprimir línea por línea da ese efecto "Matrix" de evolución).
            # Formateamos con ceros a la izquierda para que se vea alineado.
            print(f"Gen {self.generacion:04d} | {self.mejor_cadena} | Puntos: {puntaje_actual}")

            # Condición de victoria
            if puntaje_actual == self.obj_len:
                print("\n=====================================================")
                print(f"¡EVOLUCIÓN COMPLETADA CON ÉXITO EN {self.generacion} GENERACIONES!")
                print("=====================================================\n")
                break

            # Crear población de 100 hijos + el padre
            poblacion = [self.mutar(self.mejor_cadena) for _ in range(100)]
            poblacion.append(self.mejor_cadena) # Elitismo

            # Seleccionar al mejor
            self.mejor_cadena = max(poblacion, key=self.puntaje)
            self.generacion += 1

            # Pausa minúscula opcional para que la terminal no escupa todo de golpe (puedes comentarla para máxima velocidad)
            time.sleep(0.01) 

    def iniciar(self):
        """Método principal que orquesta la ejecución."""
        print("=========================================")
        print("   PROGRAMA DE RICHARD DAWKINS (TERMINAL)")
        print("=========================================")
        
        self.configurar_objetivo()
        self.configurar_inicio()
        self.evolucionar()

if __name__ == "__main__":
    juego = MonoEscritor()
    try:
        juego.iniciar()
    except KeyboardInterrupt:
        print