import pygame
import sys
import numpy as np
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import torch
import torch.nn as nn
import torch.nn.functional as F

# Define the flower classifier model with softmax
class FlowerClassifier(nn.Module):
    def __init__(self):
        super(FlowerClassifier, self).__init__()
        self.fc = nn.Linear(100 * 100, 2)  # Simple linear layer for flattened image

    def forward(self, x):
        x = x.view(-1)  # Flatten
        x = self.fc(x)
        return F.softmax(x, dim=0)  # Softmax for probabilities

model = FlowerClassifier()

# Histogram equalization function
def equalize_histogram(image):
    image = image.astype(np.uint8)
    hist = np.bincount(image.flatten(), minlength=256)
    cdf = hist.cumsum()
    cdf = (255 * cdf / cdf[-1]).astype(np.uint8)
    image_equalized = cdf[image]
    return image_equalized

# Process and classify image
def process_and_classify(img):
    img_eq = equalize_histogram(img)
    img_smooth = gaussian_filter(img_eq, sigma=1)  # Smoothing
    input_tensor = torch.tensor(img_smooth.flatten() / 255.0, dtype=torch.float32)
    probs = model(input_tensor)
    is_flower = probs[0] > probs[1]  # Class 0: flower, 1: other (random due to untrained model)
    return is_flower

# Adapted BFS with meta (from provided script)
def bfs_meta(inicio, meta, graph):
    visitados = set()
    cola = deque([inicio])
    parent = {inicio: None}
    explored = []
    while cola:
        nodo = cola.popleft()
        if nodo not in visitados:
            visitados.add(nodo)
            explored.append(nodo)
            if nodo == meta:
                break
            for vecino in graph.get(nodo, []):
                if vecino not in parent:
                    cola.append(vecino)
                    parent[vecino] = nodo
    # Reconstruct path
    path = []
    current = meta
    while current is not None:
        path.append(current)
        current = parent.get(current)
    path.reverse()
    return explored, path

# Adapted DFS with meta (from provided script, iterative)
def dfs_meta(inicio, meta, graph):
    visitados = set()
    pila = [inicio]
    parent = {inicio: None}
    explored = []
    while pila:
        nodo = pila.pop()
        if nodo not in visitados:
            visitados.add(nodo)
            explored.append(nodo)
            if nodo == meta:
                break
            for vecino in reversed(graph.get(nodo, [])):
                if vecino not in parent:
                    pila.append(vecino)
                    parent[vecino] = nodo
    # Reconstruct path
    path = []
    current = meta
    while current is not None:
        path.append(current)
        current = parent.get(current)
    path.reverse()
    return explored, path

# Function to plot the graph with exploration order
def plot_graph(graph, explored, start, goal, title):
    G = nx.Graph()
    for nodo, vecinos in graph.items():
        for vecino in vecinos:
            G.add_edge(nodo, vecino)
    pos = {(i, j): (j, -i) for i in range(N) for j in range(N) if (i, j) in graph}
    labels = {nodo: f"{nodo}({idx+1})" for idx, nodo in enumerate(explored)}
    plt.figure(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=2000, node_color="lightgreen", font_size=10, font_weight="bold")
    nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color="green", node_size=2200)
    nx.draw_networkx_nodes(G, pos, nodelist=[goal], node_color="red", node_size=2200)
    plt.title(title, fontsize=14)
    plt.show()

# Main code
N = 10  # Grid size NxN
cell_size = 100
width, height = N * cell_size, N * cell_size

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Abejita Search Project")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Generate grid with random obstacles
grid = np.full((N, N), 'obj', dtype='<U6')
num_obs = int(N * N * 0.2)
obs_indices = np.random.choice(N * N, num_obs, replace=False)
for idx in obs_indices:
    i, j = divmod(idx, N)
    grid[i, j] = 'obs'

# Generate synthetic images for objects (subexposed random)
images = {}
for i in range(N):
    for j in range(N):
        if grid[i, j] == 'obj':
            images[(i, j)] = np.random.randint(0, 50, (100, 100), dtype=np.uint8)  # Low contrast

# Build graph
graph = {}
for i in range(N):
    for j in range(N):
        if grid[i, j] != 'obs':
            neighbors = []
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < N and 0 <= nj < N and grid[ni, nj] != 'obs':
                    neighbors.append((ni, nj))
            graph[(i, j)] = neighbors

# Variables
running = True
start = None
goal = None
phase = 'select_start'  # 'select_start', 'select_goal', 'animate_bfs', 'animate_dfs', 'done'
explored_bfs, path_bfs = [], []
explored_dfs, path_dfs = [], []
flowers_bfs = 0
flowers_dfs = 0
current_step = 0
current_strategy = None
bee_pos = None

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and (phase == 'select_start' or phase == 'select_goal'):
            x, y = event.pos
            j, i = x // cell_size, y // cell_size
            pos = (i, j)
            if pos in graph:
                if phase == 'select_start':
                    start = pos
                    phase = 'select_goal'
                elif phase == 'select_goal' and pos != start:
                    goal = pos
                    # Run searches
                    explored_bfs, path_bfs = bfs_meta(start, goal, graph)
                    explored_dfs, path_dfs = dfs_meta(start, goal, graph)
                    phase = 'animate_bfs'
                    current_step = 0
                    current_strategy = 'BFS'
                    print("Starting BFS animation")

    if phase.startswith('animate_'):
        if current_step < len(explored_bfs if current_strategy == 'BFS' else explored_dfs):
            explored = explored_bfs if current_strategy == 'BFS' else explored_dfs
            nodo = explored[current_step]
            bee_pos = nodo
            if nodo != goal and nodo in images:
                is_flower = process_and_classify(images[nodo])
                if is_flower:
                    if current_strategy == 'BFS':
                        flowers_bfs += 1
                    else:
                        flowers_dfs += 1
                    grid[nodo[0], nodo[1]] = 'flower'
                else:
                    grid[nodo[0], nodo[1]] = 'other'
            current_step += 1
            clock.tick(2)  # 0.5 sec delay
        else:
            # Finish current animation
            if current_strategy == 'BFS':
                print(f"BFS: Explored {len(explored_bfs)} nodes, Path length {len(path_bfs)}, Flowers collected: {flowers_bfs}")
                phase = 'animate_dfs'
                current_step = 0
                current_strategy = 'DFS'
                print("Starting DFS animation")
            else:
                print(f"DFS: Explored {len(explored_dfs)} nodes, Path length {len(path_dfs)}, Flowers collected: {flowers_dfs}")
                phase = 'done'

    # Draw grid
    screen.fill(WHITE)
    for i in range(N):
        for j in range(N):
            rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
            if grid[i, j] == 'obs':
                pygame.draw.rect(screen, BLACK, rect)
            elif grid[i, j] == 'flower':
                pygame.draw.rect(screen, GREEN, rect)
            elif grid[i, j] == 'other':
                pygame.draw.rect(screen, BLUE, rect)
            else:
                pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

    # Draw start and goal
    if start:
        rect = pygame.Rect(start[1] * cell_size, start[0] * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, GREEN, rect, 4)
    if goal:
        rect = pygame.Rect(goal[1] * cell_size, goal[0] * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, RED, rect, 4)

    # Draw bee
    if bee_pos:
        bee_rect = pygame.Rect(bee_pos[1] * cell_size + 25, bee_pos[0] * cell_size + 25, 50, 50)
        pygame.draw.circle(screen, YELLOW, bee_rect.center, 25)

    pygame.display.flip()

    if phase == 'done':
        # Comparison
        print("\nComparación de estrategias:")
        print(f"BFS recolectó {flowers_bfs} flores en un camino de longitud {len(path_bfs)}.")
        print(f"DFS recolectó {flowers_dfs} flores en un camino de longitud {len(path_dfs)}.")
        if flowers_bfs > flowers_dfs:
            print("BFS recolectó más flores.")
        elif flowers_dfs > flowers_bfs:
            print("DFS recolectó más flores.")
        else:
            print("Ambas estrategias recolectaron la misma cantidad de flores.")

        # Show plots
        plot_graph(graph, explored_bfs, start, goal, "BFS Exploration")
        plot_graph(graph, explored_dfs, start, goal, "DFS Exploration")

        running = False

pygame.quit()
sys.exit()