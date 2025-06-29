import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class TaTeTi:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ta Te Ti")
        self.ventana.withdraw()

        # Seleccion de modo de juego
        self.modo = None
        self.modo_var = tk.StringVar()
        self.pedir_modo()
        self.ventana.wait_variable(self.modo_var)

        # Nombres de jugadores
        self.nombre = None
        self.nombre2 = None
        self.simbolo_jugador = "X"
        self.simbolo_jugador2 = "O"
        self.turno = 1 

        self.pedir_nombres()

        # Dificultad solo si es contra la PC
        if self.modo == "pc":
            self.dificultad = None
            self.pedir_dificultad()
            self.ventana.wait_variable(self.dificultad_var)
        else:
            self.dificultad = None

        self.ventana.deiconify()
        self.centrar_ventana(self.ventana)

        self.botones = [[None for _ in range(3)] for _ in range(3)]
        self.crear_tablero()

    def centrar_ventana(self, ventana):
        ventana.update_idletasks()
        ancho = ventana.winfo_width()
        alto = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f"+{x}+{y}")

    def pedir_modo(self):
        ventana_modo = tk.Toplevel(self.ventana)
        ventana_modo.title("Modo de juego")
        tk.Label(ventana_modo, text="¿Contra quién quieres jugar?", font=("Arial", 14)).pack(padx=10, pady=10)

        def elegir(modo):
            self.modo = modo
            self.modo_var.set(modo)
            ventana_modo.destroy()

        tk.Button(ventana_modo, text="Contra un amigo", width=20, font=("Arial", 12), command=lambda: elegir("amigo")).pack(pady=5)
        tk.Button(ventana_modo, text="Contra la computadora", width=20, font=("Arial", 12), command=lambda: elegir("pc")).pack(pady=5)

        ventana_modo.grab_set()
        ventana_modo.protocol("WM_DELETE_WINDOW", self.ventana.destroy)
        self.centrar_ventana(ventana_modo)

    def pedir_nombres(self):
        while not self.nombre:
            nombre_ingresado = simpledialog.askstring("Nombre", "¿Cuál es tu nombre?")
            if nombre_ingresado is None:
                self.ventana.destroy()
                return
            if nombre_ingresado.strip() != "":
                self.nombre = nombre_ingresado.strip().capitalize()
            else:
                messagebox.showwarning("Nombre requerido", "Por favor, ingresa tu nombre para continuar.")

        if self.modo == "amigo":
            while not self.nombre2:
                nombre_ingresado = simpledialog.askstring("Nombre", "¿Cuál es el nombre jugador 2?")
                if nombre_ingresado is None:
                    self.ventana.destroy()
                    return
                if nombre_ingresado.strip() != "":
                    self.nombre2 = nombre_ingresado.strip().capitalize()
                else:
                    messagebox.showwarning("Nombre requerido", "Por favor, ingresa el nombre de tu amigo para continuar.")

    def pedir_dificultad(self):
        self.dificultad_var = tk.StringVar()
        ventana_dificultad = tk.Toplevel(self.ventana)
        ventana_dificultad.title("Elige dificultad")
        tk.Label(ventana_dificultad, text="Elige la dificultad", font=("Arial", 14)).pack(padx=10, pady=10)

        def elegir(dificultad):
            self.dificultad = dificultad
            self.dificultad_var.set(dificultad)
            ventana_dificultad.destroy()

        tk.Button(ventana_dificultad, text="Baja", width=15, font=("Arial", 12), command=lambda: elegir("baja")).pack(pady=5)
        tk.Button(ventana_dificultad, text="Media", width=15, font=("Arial", 12), command=lambda: elegir("media")).pack(pady=5)
        tk.Button(ventana_dificultad, text="Experto", width=15, font=("Arial", 12), command=lambda: elegir("experto")).pack(pady=5)

        ventana_dificultad.grab_set()
        ventana_dificultad.protocol("WM_DELETE_WINDOW", self.ventana.destroy)
        self.centrar_ventana(ventana_dificultad)

    def crear_tablero(self):
        if self.modo == "pc":
            texto_info = f"{self.nombre}: {self.simbolo_jugador} | Computadora: {self.simbolo_jugador2} | Dificultad: {self.dificultad.capitalize()}"
        else:
            texto_info = f"{self.nombre}: {self.simbolo_jugador} | {self.nombre2}: {self.simbolo_jugador2}"
        tk.Label(self.ventana, text=texto_info, font=("Arial", 12)).grid(row=0, column=0, columnspan=3)

        for fila in range(3):
            for columna in range(3):
                boton = tk.Button(self.ventana, text="", width=10, height=3, font=("Arial", 24),
                                  command=lambda f=fila, c=columna: self.clic_jugador(f, c))
                boton.grid(row=fila+1, column=columna, padx=2, pady=2)
                self.botones[fila][columna] = boton

    def deshabilitar_todos(self):
        for fila in self.botones:
            for boton in fila:
                boton['state'] = "disabled"

    def habilitar_vacios(self):
        for fila in self.botones:
            for boton in fila:
                if boton['text'] == "":
                    boton['state'] = "normal"

    def obtener_tablero(self):
        return [[self.botones[f][c]['text'] for c in range(3)] for f in range(3)]

    def hay_ganador(self, tablero):
        # Filas
        for f in range(3):
            if tablero[f][0] == tablero[f][1] == tablero[f][2] != "":
                return tablero[f][0], [(f,0), (f,1), (f,2)]
        # Columnas
        for c in range(3):
            if tablero[0][c] == tablero[1][c] == tablero[2][c] != "":
                return tablero[0][c], [(0,c), (1,c), (2,c)]
        # Diagonales
        if tablero[0][0] == tablero[1][1] == tablero[2][2] != "":
            return tablero[0][0], [(0,0), (1,1), (2,2)]
        if tablero[0][2] == tablero[1][1] == tablero[2][0] != "":
            return tablero[0][2], [(0,2), (1,1), (2,0)]
        return None, []

    def tablero_lleno(self, tablero):
        for fila in tablero:
            for celda in fila:
                if celda == "":
                    return False
        return True

    def resaltar_ganador(self, posiciones):
        for f, c in posiciones:
            self.botones[f][c]['bg'] = "lightgreen"

    def clic_jugador(self, f, c):
        if self.botones[f][c]['text'] == "":
            if self.modo == "pc":
                self.botones[f][c]['text'] = self.simbolo_jugador
                self.botones[f][c]['state'] = "disabled"
                self.botones[f][c]['bg'] = "lightblue"
                ganador, posiciones = self.hay_ganador(self.obtener_tablero())
                if ganador:
                    self.resaltar_ganador(posiciones)
                    self.deshabilitar_todos()
                    self.ventana.after(500, lambda: self.mostrar_ganador(ganador))
                elif self.tablero_lleno(self.obtener_tablero()):
                    self.deshabilitar_todos()
                    self.ventana.after(500, self.mostrar_empate)
                else:
                    self.deshabilitar_todos()
                    self.ventana.after(500, self.movimiento_pc)
            else:
                if self.turno == 1:
                    self.botones[f][c]['text'] = self.simbolo_jugador
                    self.botones[f][c]['bg'] = "lightblue"
                else:
                    self.botones[f][c]['text'] = self.simbolo_jugador2
                    self.botones[f][c]['bg'] = "lightcoral"
                self.botones[f][c]['state'] = "disabled"
                ganador, posiciones = self.hay_ganador(self.obtener_tablero())
                if ganador:
                    self.resaltar_ganador(posiciones)
                    self.deshabilitar_todos()
                    self.ventana.after(500, lambda: self.mostrar_ganador(ganador))
                elif self.tablero_lleno(self.obtener_tablero()):
                    self.deshabilitar_todos()
                    self.ventana.after(500, self.mostrar_empate)
                else:
                    self.turno = 2 if self.turno == 1 else 1
                    self.habilitar_vacios()

    def movimiento_pc(self):
        if self.dificultad == "baja":
            self.movimiento_aleatorio()
        elif self.dificultad == "media":
            self.movimiento_medio()
        else:
            self.movimiento_experto()

    def movimiento_aleatorio(self):
        vacios = [(f, c) for f in range(3) for c in range(3) if self.botones[f][c]['text'] == ""]
        if vacios:
            f, c = random.choice(vacios)
            self.colocar_pc(f, c)

    def movimiento_medio(self):
        # Intentar ganar
        for f, c in self.celdas_vacias():
            self.botones[f][c]['text'] = self.simbolo_jugador2
            ganador, _ = self.hay_ganador(self.obtener_tablero())
            self.botones[f][c]['text'] = ""
            if ganador == self.simbolo_jugador2:
                self.colocar_pc(f, c)
                return
        # Bloquear al jugador
        for f, c in self.celdas_vacias():
            self.botones[f][c]['text'] = self.simbolo_jugador
            ganador, _ = self.hay_ganador(self.obtener_tablero())
            self.botones[f][c]['text'] = ""
            if ganador == self.simbolo_jugador:
                self.colocar_pc(f, c)
                return
        # Si no, aleatorio
        self.movimiento_aleatorio()

    def movimiento_experto(self):
        tablero = self.obtener_tablero()
        mejor_puntaje = -float('inf')
        mejor_movimiento = None
        for f, c in self.celdas_vacias():
            tablero[f][c] = self.simbolo_jugador2
            puntaje = self.minimax(tablero, False)
            tablero[f][c] = ""
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_movimiento = (f, c)
        if mejor_movimiento:
            self.colocar_pc(*mejor_movimiento)

    def minimax(self, tablero, maximizando):
        ganador, _ = self.hay_ganador(tablero)
        if ganador == self.simbolo_jugador2:
            return 1
        elif ganador == self.simbolo_jugador:
            return -1
        elif self.tablero_lleno(tablero):
            return 0

        if maximizando:
            mejor = -float('inf')
            for f, c in self.celdas_vacias_tablero(tablero):
                tablero[f][c] = self.simbolo_jugador2
                puntaje = self.minimax(tablero, False)
                tablero[f][c] = ""
                mejor = max(puntaje, mejor)
            return mejor
        else:
            peor = float('inf')
            for f, c in self.celdas_vacias_tablero(tablero):
                tablero[f][c] = self.simbolo_jugador
                puntaje = self.minimax(tablero, True)
                tablero[f][c] = ""
                peor = min(puntaje, peor)
            return peor

    def celdas_vacias(self):
        return [(f, c) for f in range(3) for c in range(3) if self.botones[f][c]['text'] == ""]

    def celdas_vacias_tablero(self, tablero):
        return [(f, c) for f in range(3) for c in range(3) if tablero[f][c] == ""]

    def colocar_pc(self, f, c):
        self.botones[f][c]['text'] = self.simbolo_jugador2
        self.botones[f][c]['state'] = "disabled"
        self.botones[f][c]['bg'] = "lightcoral"

        ganador, posiciones = self.hay_ganador(self.obtener_tablero())
        if ganador:
            self.resaltar_ganador(posiciones)
            self.deshabilitar_todos()
            self.ventana.after(500, lambda: self.mostrar_ganador(ganador))
        elif self.tablero_lleno(self.obtener_tablero()):
            self.deshabilitar_todos()
            self.ventana.after(500, self.mostrar_empate)
        else:
            self.habilitar_vacios()

    def mostrar_ganador(self, ganador):
        if self.modo == "pc":
            if ganador == self.simbolo_jugador:
                mensaje = "¡Ganaste!\n\n¿Quieres jugar de nuevo?"
            else:
                mensaje = "¡Perdiste!\n\n¿Quieres jugar de nuevo?"
        else:
            if ganador == self.simbolo_jugador:
                mensaje = f"¡Ganó {self.nombre}!\n\n¿Quieren jugar de nuevo?"
            else:
                mensaje = f"¡Ganó {self.nombre2}!\n\n¿Quieren jugar de nuevo?"
        if messagebox.askyesno("Fin del juego", mensaje):
            self.reiniciar_tablero()
        else:
            self.ventana.quit()

    def mostrar_empate(self):
        if messagebox.askyesno("Fin del juego", "¡Empate!\n\n¿Quieren jugar de nuevo?"):
            self.reiniciar_tablero()
        else:
            self.ventana.quit()

    def reiniciar_tablero(self):
        for fila in self.botones:
            for boton in fila:
                boton['text'] = ""
                boton['state'] = "normal"
                boton['bg'] = "SystemButtonFace"
        self.turno = 1
        self.habilitar_vacios()

    def ejecutar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    juego = TaTeTi()
    juego.ejecutar()