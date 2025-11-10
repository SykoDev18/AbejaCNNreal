'''
		Percepción → Procesamiento → Acción.

		Ejemplo práctico:

			Un agente que controla un robot virtual en un entorno simulado (ejemplo: moverse en una cuadrícula buscando un objetivo).
'''

import random

pos = [0,0]
meta = [2,2]

for paso in range(10):
    if pos == meta:
        print("¡Meta alcanzada en", paso, "pasos!")
        break
    accion = random.choice(["arriba","derecha"])
    if accion == "arriba": pos[1] += 1
    if accion == "derecha": pos[0] += 1
    print("Paso", paso, ": voy a", accion, "posición", pos)
