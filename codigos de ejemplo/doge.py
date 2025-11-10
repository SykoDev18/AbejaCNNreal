import sys
import numpy as np
import os
import random
from collections import deque
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QBrush, QColor, QPixmap

import torch
from torchvision import datasets, transforms
from PIL import Image

class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene, parent):
        super().__init__(scene, parent)
        self.parent = parent
        self.selected_count = 0

    def mousePressEvent(self, event):
        if self.selected_count < 2:
            pos = self.mapToScene(event.pos())
            x, y = pos.x(), pos.y()
            i = int(y // self.parent.cell_size)
            j = int(x // self.parent.cell_size)
            if 0 <= i < self.parent.N and 0 <= j < self.parent.N:
                if self.parent.grid[i, j] not in ['obs', 'special', 'start', 'goal']:
                    if self.selected_count == 0:
                        self.parent.grid[i, j] = 'start'
                        self.selected_count += 1
                    elif self.selected_count == 1:
                        self.parent.grid[i, j] = 'goal'
                        self.selected_count += 1
                        self.parent.bfs_button.setEnabled(True)
                        self.parent.dfs_button.setEnabled(True)
                    self.parent.update_cell(i, j)

class GridWindow(QMainWindow):
    def __init__(self, N=5, obs_percentage=0.2, special_percentage=0.1, flores_dir="flores", objetos_dir="objetos"):
        super().__init__()
        self.N = N
        self.obs_percentage = obs_percentage
        self.special_percentage = special_percentage
        self.flores_dir = flores_dir
        self.objetos_dir = objetos_dir
        self.cell_size = 50
        self.path = []
        self.visited_order = []  # Almacenar orden de visita para animación
        self.current_step = 0  # Índice para animación
        self.show_path = False
        self.algorithm = ""
        self.init_images()
        self.init_grid()
        self.init_ui()

    def init_images(self):
        self.flores_images = []
        self.objetos_images = []
        try:
            if os.path.exists(self.flores_dir):
                self.flores_images = [os.path.join(self.flores_dir, f) for f in os.listdir(self.flores_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
                print(f"Imágenes en flores_dir: {len(self.flores_images)} encontradas")
            else:
                print(f"Error: La carpeta {self.flores_dir} no existe")
            if os.path.exists(self.objetos_dir):
                self.objetos_images = [os.path.join(self.objetos_dir, f) for f in os.listdir(self.objetos_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
                print(f"Imágenes en objetos_dir: {len(self.objetos_images)} encontradas")
            else:
                print(f"Error: La carpeta {self.objetos_dir} no existe")
            if not self.flores_images and not self.objetos_images:
                print("Advertencia: No se encontraron imágenes en ninguna carpeta")
        except Exception as e:
            print(f"Error al cargar imágenes: {e}")

    def init_grid(self):
        self.grid = np.full((self.N, self.N), 'obj', dtype='<U7')
        self.image_grid = np.full((self.N, self.N), None, dtype=object)
        self.type_grid = np.full((self.N, self.N), None, dtype=object)
        total_cells = self.N * self.N
        num_special = int(total_cells * self.special_percentage)
        num_obs = int(total_cells * self.obs_percentage)
        if num_special + num_obs > total_cells:
            num_obs = total_cells - num_special

        special_indices = np.random.choice(total_cells, num_special, replace=False)
        for idx in special_indices:
            i, j = divmod(idx, self.N)
            self.grid[i, j] = 'special'
            image_list = random.choice([self.flores_images, self.objetos_images])
            if image_list:
                self.image_grid[i, j] = random.choice(image_list)
                self.type_grid[i, j] = 'flower' if image_list == self.flores_images else 'object'

        remaining_indices = [i for i in range(total_cells) if i not in special_indices]
        obs_indices = np.random.choice(remaining_indices, num_obs, replace=False)
        for idx in obs_indices:
            i, j = divmod(idx, self.N)
            self.grid[i, j] = 'obs'

    def init_ui(self):
        self.setWindowTitle('Cuadrícula NxN con BFS y DFS')
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.scene = QGraphicsScene()
        self.view = CustomGraphicsView(self.scene, self)
        layout.addWidget(self.view)
        self.bfs_button = QPushButton("Ejecutar BFS")
        self.dfs_button = QPushButton("Ejecutar DFS")
        self.bfs_button.setEnabled(False)
        self.dfs_button.setEnabled(False)
        self.bfs_button.clicked.connect(self.run_bfs)
        self.dfs_button.clicked.connect(self.run_dfs)
        layout.addWidget(self.bfs_button)
        layout.addWidget(self.dfs_button)
        self.draw_grid()
        self.resize(self.N * self.cell_size + 20, self.N * self.cell_size + 120)

    def draw_grid(self):
        self.scene.clear()
        self.path = self.path if hasattr(self, 'path') else []
        self.visited_order = self.visited_order if hasattr(self, 'visited_order') else []
        for i in range(self.N):
            for j in range(self.N):
                self.draw_cell(i, j)
        if self.current_step > 0 and self.current_step <= len(self.visited_order):
            bee_i, bee_j = self.visited_order[self.current_step - 1]
            x = bee_j * self.cell_size + self.cell_size // 4
            y = bee_i * self.cell_size + self.cell_size // 4
            self.scene.addEllipse(x, y, self.cell_size // 2, self.cell_size // 2, brush=QBrush(QColor('yellow')))

    def draw_cell(self, i, j):
        x = j * self.cell_size
        y = i * self.cell_size
        try:
            if self.show_path and (i, j) in self.path and self.grid[i, j] not in ['start', 'goal']:
                brush = QBrush(QColor('yellow'))
                self.scene.addRect(x, y, self.cell_size, self.cell_size, brush=brush)
            elif (i, j) in self.visited_order[:self.current_step] and self.grid[i, j] not in ['start', 'goal', 'obs']:
                brush = QBrush(QColor('lightblue'))  # Celdas visitadas en azul claro
                self.scene.addRect(x, y, self.cell_size, self.cell_size, brush=brush)
            elif self.grid[i, j] == 'obj':
                brush = QBrush(QColor('white'))
                self.scene.addRect(x, y, self.cell_size, self.cell_size, brush=brush)
            elif self.grid[i, j] == 'obs':
                brush = QBrush(QColor('black'))
                self.scene.addRect(x, y, self.cell_size, self.cell_size, brush=brush)
            elif self.grid[i, j] == 'special':
                image_path = self.image_grid[i, j]
                if image_path and os.path.exists(image_path):
                    pixmap = QPixmap(image_path).scaled(self.cell_size, self.cell_size, Qt.KeepAspectRatio)
                    if pixmap.isNull():
                        print(f"Error: No se pudo cargar la imagen {image_path}")
                        brush = QBrush(QColor('blue'))
                        self.scene.addRect(x, y, self.cell_size, self.cell_size, brush=brush)
                    else:
                        self.scene.addPixmap(pixmap).setPos(x, y)
                else:
                    brush = QBrush(QColor('blue'))
                    self.scene.addRect(x, y, self.cell_size, self.cell_size, brush=brush)
            elif self.grid[i, j] == 'start':
                brush = QBrush(QColor('lime'))
                self.scene.addRect(x, y, self.cell_size, self.cell_size, brush=brush)
            elif self.grid[i, j] == 'goal':
                brush = QBrush(QColor('red'))
                self.scene.addRect(x, y, self.cell_size, self.cell_size, brush=brush)
        except Exception as e:
            print(f"Error al dibujar celda ({i}, {j}): {e}")

    def update_cell(self, i, j):
        self.draw_grid()

    def get_neighbors(self, i, j):
        neighbors = []
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.N and 0 <= nj < self.N and self.grid[ni, nj] != 'obs':
                neighbors.append((ni, nj))
        return neighbors

    def bfs(self, start, goal):
        self.visited_order = []
        queue = deque([(start, [start])])
        visited = {start}
        while queue:
            (i, j), path = queue.popleft()
            self.visited_order.append((i, j))
            if (i, j) == goal:
                return path
            for ni, nj in self.get_neighbors(i, j):
                if (ni, nj) not in visited:
                    visited.add((ni, nj))
                    queue.append(((ni, nj), path + [(ni, nj)]))
        return []

    def dfs(self, start, goal):
        self.visited_order = []
        stack = [(start, [start])]
        visited = {start}
        while stack:
            (i, j), path = stack.pop()
            self.visited_order.append((i, j))
            if (i, j) == goal:
                return path
            for ni, nj in self.get_neighbors(i, j):
                if (ni, nj) not in visited:
                    visited.add((ni, nj))
                    stack.append(((ni, nj), path + [(ni, nj)]))
        return []

    def animate_search(self):
        if self.current_step < len(self.visited_order):
            self.draw_grid()
            self.current_step += 1
            QTimer.singleShot(500, self.animate_search)
        else:
            if self.path:
                self.show_path = True
                self.draw_grid()
                flowers_path = sum(1 for pos in self.path if self.grid[pos[0], pos[1]] == 'special' and self.type_grid[pos[0], pos[1]] == 'flower')
                flowers_explored = sum(1 for pos in self.visited_order if self.grid[pos[0], pos[1]] == 'special' and self.type_grid[pos[0], pos[1]] == 'flower')
                QMessageBox.information(self, self.algorithm, f"Camino encontrado!\nLongitud: {len(self.path)}\nFlores en el camino: {flowers_path}\nFlores exploradas: {flowers_explored}")
            else:
                flowers_explored = sum(1 for pos in self.visited_order if self.grid[pos[0], pos[1]] == 'special' and self.type_grid[pos[0], pos[1]] == 'flower')
                QMessageBox.information(self, self.algorithm, f"No se encontró un camino a la meta.\nCeldas exploradas: {len(self.visited_order)}\nFlores exploradas: {flowers_explored}")

    def run_bfs(self):
        start = goal = None
        for i in range(self.N):
            for j in range(self.N):
                if self.grid[i, j] == 'start':
                    start = (i, j)
                elif self.grid[i, j] == 'goal':
                    goal = (i, j)
        if not start or not goal:
            QMessageBox.warning(self, "Error", "Selecciona un inicio (verde) y una meta (rojo) primero.")
            return
        self.algorithm = "BFS"
        self.path = self.bfs(start, goal)
        self.current_step = 0
        self.show_path = False
        self.animate_search()

    def run_dfs(self):
        start = goal = None
        for i in range(self.N):
            for j in range(self.N):
                if self.grid[i, j] == 'start':
                    start = (i, j)
                elif self.grid[i, j] == 'goal':
                    goal = (i, j)
        if not start or not goal:
            QMessageBox.warning(self, "Error", "Selecciona un inicio (verde) y una meta (rojo) primero.")
            return
        self.algorithm = "DFS"
        self.path = self.dfs(start, goal)
        self.current_step = 0
        self.show_path = False
        self.animate_search()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        flores_dir = r"C:\Users\Alexis Vladimir\Downloads\gemma\2doParcial\búsquedas_sin_información\búsquedas_sin_informacón\fotos_flores_proyecto_abeja"
        objetos_dir = r"C:\Users\Alexis Vladimir\Downloads\gemma\2doParcial\búsquedas_sin_información\búsquedas_sin_informacón\fotos_objetos"
        window = GridWindow(N=10, obs_percentage=0.2, special_percentage=0.1, flores_dir=flores_dir, objetos_dir=objetos_dir)
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error al ejecutar la aplicación: {e}")