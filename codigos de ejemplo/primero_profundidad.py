'''
	    A
      / | \
     B  C  D
    / \    |
   E   F   G

pip install networkx
'''

import networkx as nx
import matplotlib.pyplot as plt

# Árbol como diccionario
arbol = {
    'A': ['B', 'C', 'D'],
    'B': ['E', 'F'],
    'C': [],
    'D': ['G'],
    'E': [],
    'F': [],
    'G': []
}

# DFS
def dfs(nodo, visitados):
    if nodo not in visitados:
        visitados.append(nodo)
        for vecino in arbol[nodo]:
            dfs(vecino, visitados)
    return visitados

recorrido_dfs = dfs('A', [])
print("Recorrido en profundidad (DFS):", recorrido_dfs)

# --- Graficar ---
G = nx.DiGraph()
for nodo, vecinos in arbol.items():
    for vecino in vecinos:
        G.add_edge(nodo, vecino)

pos = nx.spring_layout(G, seed=42)  # disposición fija para consistencia

# Etiquetas con el orden de visita
labels = {nodo: f"{nodo}({i+1})" for i, nodo in enumerate(recorrido_dfs)}

plt.figure(figsize=(6,4))
nx.draw(G, pos, with_labels=True, labels=labels,
        node_size=2000, node_color="skyblue", font_size=10, font_weight="bold")
plt.title("Árbol con DFS (orden numerado)", fontsize=14)
plt.show()
