"""
Tres en Raya (Tic-Tac-Toe) - Modo Dos Jugadores.

Características:
- Interfaz gráfica con Tkinter.
- Juego adversarial entre dos personas (Jugador 1 = X, Jugador 2 = O).
- Cronómetro por jugada que mide cuánto demora cada movimiento de cada jugador.
- Estadísticas finales: tiempo total, promedio y mejor jugada por jugador.
- Criterio de desempate: si el resultado es empate en el tablero,
  gana quien tenga el menor tiempo promedio por jugada
  (jugador más rápido = más eficiente).

Autor: Kathia Medina Rodriguez
"""

import tkinter as tk
from tkinter import messagebox, font, simpledialog
import time


# -------------------------------------------------------------------
# LÓGICA DEL TABLERO
# -------------------------------------------------------------------

JUGADOR_1 = "X"
JUGADOR_2 = "O"
VACIO = " "

LINEAS_GANADORAS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # Filas
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # Columnas
    (0, 4, 8), (2, 4, 6),              # Diagonales
]


def ganador(tablero):
    """Devuelve (ficha_ganadora, línea) o (None, None) si nadie ganó."""
    for a, b, c in LINEAS_GANADORAS:
        if tablero[a] == tablero[b] == tablero[c] != VACIO:
            return tablero[a], (a, b, c)
    return None, None


def tablero_lleno(tablero):
    return VACIO not in tablero


# -------------------------------------------------------------------
# INTERFAZ GRÁFICA
# -------------------------------------------------------------------

class JuegoTresEnRaya:
    COLOR_FONDO = "#1e1e2e"
    COLOR_TABLERO = "#313244"
    COLOR_TEXTO = "#cdd6f4"
    COLOR_X = "#f38ba8"
    COLOR_O = "#89b4fa"
    COLOR_X_PREVIEW = "#6b3d4a"   # X tenue (vista previa al pasar el mouse)
    COLOR_O_PREVIEW = "#3d4a6b"   # O tenue (vista previa al pasar el mouse)
    COLOR_HOVER = "#45475a"
    COLOR_ACENTO = "#a6e3a1"
    COLOR_AVISO = "#f9e2af"

    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Tres en Raya - Dos Jugadores")
        self.raiz.configure(bg=self.COLOR_FONDO)
        self.raiz.resizable(False, False)

        # Pedir nombres antes de empezar
        self.nombre_j1 = self._pedir_nombre("Jugador 1 (X)", "Jugador 1")
        self.nombre_j2 = self._pedir_nombre("Jugador 2 (O)", "Jugador 2")

        self.tablero = [VACIO] * 9
        self.botones = []
        self.juego_terminado = False
        self.turno_actual = JUGADOR_1   # X siempre comienza

        # Tiempos de jugada por jugador
        self.tiempos_j1 = []
        self.tiempos_j2 = []
        self.inicio_jugada = None

        # Fuentes
        self.fuente_titulo = font.Font(family="Helvetica", size=16, weight="bold")
        self.fuente_celda = font.Font(family="Helvetica", size=36, weight="bold")
        self.fuente_estado = font.Font(family="Helvetica", size=12, weight="bold")
        self.fuente_cron = font.Font(family="Courier", size=14, weight="bold")

        self._construir_ui()
        self._iniciar_cronometro()

    # ---------- Diálogos ----------

    def _pedir_nombre(self, etiqueta, predeterminado):
        nombre = simpledialog.askstring(
            "Nombre del jugador",
            f"Nombre del {etiqueta}:",
            initialvalue=predeterminado,
            parent=self.raiz,
        )
        return (nombre.strip() if nombre and nombre.strip() else predeterminado)

    # ---------- Construcción de la interfaz ----------

    def _construir_ui(self):
        # Título
        titulo = tk.Label(
            self.raiz,
            text="⚔  TRES EN RAYA - 2 JUGADORES  ⚔",
            font=self.fuente_titulo,
            bg=self.COLOR_FONDO,
            fg=self.COLOR_ACENTO,
            pady=10,
        )
        titulo.grid(row=0, column=0, columnspan=3, padx=20, pady=(15, 5))

        # Estado del turno
        self.lbl_estado = tk.Label(
            self.raiz,
            text=self._texto_turno(),
            font=self.fuente_estado,
            bg=self.COLOR_FONDO,
            fg=self.COLOR_X,
        )
        self.lbl_estado.grid(row=1, column=0, columnspan=3, pady=(0, 5))

        # Cronómetro de la jugada actual
        self.lbl_cronometro = tk.Label(
            self.raiz,
            text="⏱  0.000 s",
            font=self.fuente_cron,
            bg=self.COLOR_FONDO,
            fg=self.COLOR_AVISO,
        )
        self.lbl_cronometro.grid(row=2, column=0, columnspan=3, pady=(0, 10))

        # Tablero 3x3
        marco = tk.Frame(self.raiz, bg=self.COLOR_TABLERO, padx=4, pady=4)
        marco.grid(row=3, column=0, columnspan=3, padx=20)

        for i in range(9):
            fila = i // 3
            col = i % 3
            btn = tk.Button(
                marco,
                text=VACIO,
                font=self.fuente_celda,
                width=3,
                height=1,
                bg=self.COLOR_TABLERO,
                fg=self.COLOR_X,
                activebackground=self.COLOR_HOVER,
                relief="flat",
                bd=0,
                command=lambda idx=i: self._click_celda(idx),
            )
            btn.grid(row=fila, column=col, padx=2, pady=2, ipadx=10, ipady=10)
            btn.bind("<Enter>", lambda e, idx=i: self._on_hover(idx, entrar=True))
            btn.bind("<Leave>", lambda e, idx=i: self._on_hover(idx, entrar=False))
            self.botones.append(btn)

        # Panel de estadísticas en vivo
        self.lbl_stats = tk.Label(
            self.raiz,
            text=self._texto_stats(),
            font=("Courier", 10),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_TEXTO,
            justify="left",
        )
        self.lbl_stats.grid(row=4, column=0, columnspan=3, pady=10)

        # Botón de reinicio
        btn_reset = tk.Button(
            self.raiz,
            text="🔄 Nueva partida",
            font=self.fuente_estado,
            bg=self.COLOR_ACENTO,
            fg=self.COLOR_FONDO,
            activebackground=self.COLOR_HOVER,
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            command=self._reiniciar,
        )
        btn_reset.grid(row=5, column=0, columnspan=3, pady=(0, 15))

    def _texto_turno(self):
        if self.turno_actual == JUGADOR_1:
            return f"Turno de {self.nombre_j1}  (X)"
        return f"Turno de {self.nombre_j2}  (O)"

    def _texto_stats(self):
        prom1 = sum(self.tiempos_j1) / len(self.tiempos_j1) if self.tiempos_j1 else 0
        prom2 = sum(self.tiempos_j2) / len(self.tiempos_j2) if self.tiempos_j2 else 0
        n1 = self.nombre_j1[:12]
        n2 = self.nombre_j2[:12]
        return (
            f"{'':<13}{n1:<14}{n2:<14}\n"
            f"Jugadas    : {len(self.tiempos_j1):<14}{len(self.tiempos_j2):<14}\n"
            f"Promedio   : {prom1:>6.3f}s       {prom2:>6.3f}s"
        )

    # ---------- Vista previa al pasar el mouse ----------

    def _on_hover(self, idx, entrar):
        """Muestra una X o O tenue sobre la casilla vacía indicando dónde caerá la ficha."""
        if self.juego_terminado or self.tablero[idx] != VACIO:
            return
        if entrar:
            preview_color = (
                self.COLOR_X_PREVIEW if self.turno_actual == JUGADOR_1
                else self.COLOR_O_PREVIEW
            )
            self.botones[idx].config(text=self.turno_actual, fg=preview_color)
        else:
            self.botones[idx].config(text=VACIO)

    # ---------- Cronómetro ----------

    def _iniciar_cronometro(self):
        self.inicio_jugada = time.perf_counter()
        self._refrescar_cronometro()

    def _refrescar_cronometro(self):
        if self.juego_terminado or self.inicio_jugada is None:
            return
        transcurrido = time.perf_counter() - self.inicio_jugada
        self.lbl_cronometro.config(text=f"⏱  {transcurrido:6.3f} s")
        self.raiz.after(50, self._refrescar_cronometro)

    def _detener_cronometro(self):
        if self.inicio_jugada is None:
            return 0.0
        transcurrido = time.perf_counter() - self.inicio_jugada
        self.inicio_jugada = None
        return transcurrido

    # ---------- Lógica de turnos ----------

    def _click_celda(self, idx):
        if self.juego_terminado or self.tablero[idx] != VACIO:
            return

        # Registrar tiempo del jugador que acaba de mover
        t = self._detener_cronometro()
        if self.turno_actual == JUGADOR_1:
            self.tiempos_j1.append(t)
            color = self.COLOR_X
        else:
            self.tiempos_j2.append(t)
            color = self.COLOR_O

        # Aplicar la jugada
        self.tablero[idx] = self.turno_actual
        self.botones[idx].config(
            text=self.turno_actual,
            fg=color,
            state="disabled",
            disabledforeground=color,
        )

        # Actualizar estadísticas en vivo
        self.lbl_stats.config(text=self._texto_stats())

        # ¿Terminó la partida?
        if self._verificar_fin():
            return

        # Cambiar de turno
        self.turno_actual = JUGADOR_2 if self.turno_actual == JUGADOR_1 else JUGADOR_1
        color_turno = self.COLOR_X if self.turno_actual == JUGADOR_1 else self.COLOR_O
        self.lbl_estado.config(text=self._texto_turno(), fg=color_turno)
        self._iniciar_cronometro()

    # ---------- Fin de partida ----------

    def _verificar_fin(self):
        g, linea = ganador(self.tablero)
        if g is not None:
            self.juego_terminado = True
            self._resaltar_linea(linea)
            self._mostrar_resultado(ganador_directo=g)
            return True
        if tablero_lleno(self.tablero):
            self.juego_terminado = True
            self._mostrar_resultado(ganador_directo=None)
            return True
        return False

    def _resaltar_linea(self, linea):
        for idx in linea:
            self.botones[idx].config(
                bg=self.COLOR_ACENTO,
                disabledforeground=self.COLOR_FONDO,
            )

    def _mostrar_resultado(self, ganador_directo):
        prom1 = sum(self.tiempos_j1) / len(self.tiempos_j1) if self.tiempos_j1 else 0
        prom2 = sum(self.tiempos_j2) / len(self.tiempos_j2) if self.tiempos_j2 else 0
        total1 = sum(self.tiempos_j1)
        total2 = sum(self.tiempos_j2)
        mejor1 = min(self.tiempos_j1) if self.tiempos_j1 else 0
        mejor2 = min(self.tiempos_j2) if self.tiempos_j2 else 0

        if ganador_directo == JUGADOR_1:
            titulo = f"🎉 ¡Gana {self.nombre_j1}!"
            veredicto = f"Ganador directo: {self.nombre_j1} (X) por línea en el tablero"
        elif ganador_directo == JUGADOR_2:
            titulo = f"🎉 ¡Gana {self.nombre_j2}!"
            veredicto = f"Ganador directo: {self.nombre_j2} (O) por línea en el tablero"
        else:
            # EMPATE -> criterio de menor tiempo promedio
            titulo = "🤝 Empate en el tablero"
            if prom1 < prom2:
                veredicto = (
                    f"Empate en jugadas, pero por MENOR TIEMPO PROMEDIO\n"
                    f"gana {self.nombre_j1} (X)\n"
                    f"  {prom1:.3f}s  vs  {prom2:.3f}s"
                )
            elif prom2 < prom1:
                veredicto = (
                    f"Empate en jugadas, pero por MENOR TIEMPO PROMEDIO\n"
                    f"gana {self.nombre_j2} (O)\n"
                    f"  {prom2:.3f}s  vs  {prom1:.3f}s"
                )
            else:
                veredicto = "Empate absoluto (mismo tiempo promedio en ambos jugadores)"

        self.lbl_estado.config(text=titulo, fg=self.COLOR_ACENTO)

        n1 = self.nombre_j1[:14]
        n2 = self.nombre_j2[:14]
        mensaje = (
            f"{veredicto}\n\n"
            f"────────  ESTADÍSTICAS  ────────\n"
            f"{'':<17}{n1:<16}{n2}\n"
            f"Jugadas        : {len(self.tiempos_j1):<16}{len(self.tiempos_j2)}\n"
            f"Tiempo total   : {total1:>7.3f}s        {total2:>7.3f}s\n"
            f"Tiempo promedio: {prom1:>7.3f}s        {prom2:>7.3f}s\n"
            f"Mejor jugada   : {mejor1:>7.3f}s        {mejor2:>7.3f}s\n"
        )
        messagebox.showinfo("Fin del juego", mensaje)

    # ---------- Reinicio ----------

    def _reiniciar(self):
        self.tablero = [VACIO] * 9
        self.juego_terminado = False
        self.turno_actual = JUGADOR_1
        self.tiempos_j1 = []
        self.tiempos_j2 = []
        for btn in self.botones:
            btn.config(text=VACIO, state="normal", bg=self.COLOR_TABLERO, fg=self.COLOR_X)
        self.lbl_estado.config(text=self._texto_turno(), fg=self.COLOR_X)
        self.lbl_stats.config(text=self._texto_stats())
        self._iniciar_cronometro()


# -------------------------------------------------------------------
# PUNTO DE ENTRADA
# -------------------------------------------------------------------

def main():
    raiz = tk.Tk()
    JuegoTresEnRaya(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()