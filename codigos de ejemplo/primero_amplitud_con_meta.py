import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# --- Definición del árbol ---
arbol = {
    'A': ['B', 'C', 'D'],
    'B': ['E', 'F'],
    'C': [],
    'D': ['G'],
    'E': [],
    'F': [],
    'G': []
}

# --- BFS con meta ---
def bfs_meta(inicio, meta):
    visitados = []
    cola = deque([inicio])
    while cola:
        nodo = cola.popleft()
        if nodo not in visitados:
            visitados.append(nodo)
            if nodo == meta:
                print(f"Meta '{meta}' encontrada ✅")
                return visitados
            for vecino in arbol[nodo]:
                cola.append(vecino)
    return visitados

# --- Parámetros ---
estado_inicial = 'A'
meta = 'F'

# Ejecutar BFS
recorrido_bfs = bfs_meta(estado_inicial, meta)
print("Recorrido hasta la meta:", recorrido_bfs)

# --- Graficar ---
G = nx.DiGraph()
for nodo, vecinos in arbol.items():
    for vecino in vecinos:
        G.add_edge(nodo, vecino)

pos = nx.spring_layout(G, seed=42)

# Etiquetas solo para nodos visitados
labels = {nodo: f"{nodo}({i+1})" for i, nodo in enumerate(recorrido_bfs)}

plt.figure(figsize=(6,4))
nx.draw(G, pos, with_labels=True, labels=labels,
        node_size=2000, node_color="lightgreen", font_size=10, font_weight="bold")

# Marcar inicio y meta
nx.draw_networkx_nodes(G, pos, nodelist=[estado_inicial], node_color="green", node_size=2200)
nx.draw_networkx_nodes(G, pos, nodelist=[meta], node_color="red", node_size=2200)

plt.title(f"BFS desde {estado_inicial} hasta {meta}", fontsize=14)
plt.show()
