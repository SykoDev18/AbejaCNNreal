'''
	    A
      / | \
     B  C  D
    / \    |
   E   F   G

pip install networkx
pip install collection

'''

import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Árbol
arbol = {
    'A': ['B', 'C', 'D'],
    'B': ['E', 'F'],
    'C': [],
    'D': ['G'],
    'E': [],
    'F': [],
    'G': []
}

# BFS
def bfs(inicio):
    visitados = []
    cola = deque([inicio])
    while cola:
        nodo = cola.popleft()
        if nodo not in visitados:
            visitados.append(nodo)
            for vecino in arbol[nodo]:
                cola.append(vecino)
    return visitados

recorrido_bfs = bfs('A')
print("Recorrido en amplitud (BFS):", recorrido_bfs)

# --- Graficar ---
G = nx.DiGraph()
for nodo, vecinos in arbol.items():
    for vecino in vecinos:
        G.add_edge(nodo, vecino)

pos = nx.spring_layout(G, seed=42)

# Etiquetas con el orden de visita
labels = {nodo: f"{nodo}({i+1})" for i, nodo in enumerate(recorrido_bfs)}

plt.figure(figsize=(6,4))
nx.draw(G, pos, with_labels=True, labels=labels,
        node_size=2000, node_color="lightgreen", font_size=10, font_weight="bold")
plt.title("Árbol con BFS (orden numerado)", fontsize=14)
plt.show()
