import networkx as nx
import matplotlib.pyplot as plt

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

# --- DFS con estado inicial y meta ---
def dfs_meta(nodo_inicial, meta, visitados):
    pila = [nodo_inicial]
    while pila:
        nodo = pila.pop()
        if nodo not in visitados:
            visitados.append(nodo)
            if nodo == meta:
                print(f"Meta '{meta}' encontrada ✅")
                return visitados
            # agregamos vecinos en orden inverso para mantener lógica DFS
            pila.extend(reversed(arbol[nodo]))
    return visitados

# --- Parámetros ---
estado_inicial = 'A'
meta = 'F'

# Ejecutar DFS
recorrido_dfs = dfs_meta(estado_inicial, meta, [])
print("Recorrido hasta la meta:", recorrido_dfs)

# --- Graficar ---
G = nx.DiGraph()
for nodo, vecinos in arbol.items():
    for vecino in vecinos:
        G.add_edge(nodo, vecino)

pos = nx.spring_layout(G, seed=42)  # disposición fija para consistencia

# Etiquetas: solo nodos visitados llevan numeración
labels = {nodo: f"{nodo}({i+1})" for i, nodo in enumerate(recorrido_dfs)}

plt.figure(figsize=(6,4))
nx.draw(G, pos, with_labels=True, labels=labels,
        node_size=2000, node_color="skyblue", font_size=10, font_weight="bold")

# Marcar inicio y meta
nx.draw_networkx_nodes(G, pos, nodelist=[estado_inicial], node_color="green", node_size=2200)
nx.draw_networkx_nodes(G, pos, nodelist=[meta], node_color="red", node_size=2200)

plt.title(f"DFS desde {estado_inicial} hasta {meta}", fontsize=14)
plt.show()
