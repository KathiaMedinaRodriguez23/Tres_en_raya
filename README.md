# Tres en Raya con Juego Adversarial y Medición de Tiempo

Proyecto académico desarrollado en Python que implementa el juego clásico de **Tres en Raya** en modo visual, utilizando una interfaz gráfica construida con **Tkinter**. El sistema permite jugar una partida entre dos jugadores, registrar el tiempo empleado en cada jugada y utilizar el menor tiempo promedio como criterio adicional para determinar un ganador en caso de empate.

## Descripción del proyecto

El objetivo del proyecto es representar un escenario de juego adversarial en el que dos jugadores compiten por completar una línea de tres símbolos iguales en un tablero de 3x3. Cada jugador realiza sus movimientos por turnos y el sistema mide automáticamente el tiempo que demora cada uno en tomar una decisión.

Además de aplicar las reglas tradicionales del Tres en Raya, el programa incorpora un criterio adicional de evaluación basado en eficiencia: si la partida termina empatada en el tablero, el sistema compara el tiempo promedio por jugada de ambos jugadores y declara como ganador al jugador que haya tenido el menor tiempo promedio.

## Características principales

- Interfaz gráfica desarrollada con Tkinter.
- Juego visual de Tres en Raya en tablero 3x3.
- Modo adversarial entre dos jugadores.
- Registro del nombre de cada jugador.
- Cronómetro individual por jugada.
- Cálculo de estadísticas por jugador:
  - Número de jugadas.
  - Tiempo total.
  - Tiempo promedio.
  - Mejor jugada.
- Detección automática de ganador por filas, columnas o diagonales.
- Criterio de desempate basado en menor tiempo promedio por jugada.
- Opción para iniciar una nueva partida.

## Tecnologías utilizadas

- Python 3
- Tkinter
- Módulo `time`

## Requisitos

Para ejecutar el proyecto se necesita tener instalado:

- Python 3.x
- Tkinter incluido en la instalación de Python

En Windows, se puede verificar la versión de Python con:

```bash
py --version