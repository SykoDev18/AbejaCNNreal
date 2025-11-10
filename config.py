"""
Archivo de configuración global del proyecto Abeja.
Define todas las constantes, rutas y parámetros del sistema.
"""
import os

# ==================== CONFIGURACIÓN DEL MUNDO ====================
GRID_SIZE = 20  # Tamaño de la cuadrícula NxN
CELL_SIZE = 40  # Tamaño de cada celda en píxeles
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 10  # Frames por segundo

# Porcentajes de generación
OBSTACLE_PERCENTAGE = 0.15  # 15% de obstáculos
FLOWER_PERCENTAGE = 0.12    # 12% de flores
OBJECT_PERCENTAGE = 0.08    # 8% de objetos

# ==================== RUTAS DE ARCHIVOS ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sprites
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
SPRITE_BEE = os.path.join(ASSETS_DIR, 'abeja.png')
SPRITE_HIVE = os.path.join(ASSETS_DIR, 'colmena.png')
SPRITE_TREE = os.path.join(ASSETS_DIR, 'arbol.png')
SPRITE_FLOWER = os.path.join(ASSETS_DIR, 'flor.png')
SPRITE_OBJECT = os.path.join(ASSETS_DIR, 'objecto.png')

# Datasets
FLOWERS_DIR = os.path.join(BASE_DIR, 'fotos_flores_proyecto', 'flores')
TRAIN_DIR = os.path.join(FLOWERS_DIR, 'train')
TEST_DIR = os.path.join(FLOWERS_DIR, 'test')
OBJECTS_DIR = os.path.join(BASE_DIR, 'objectos')
REAL_FLOWERS_DIR = os.path.join(BASE_DIR, 'fotos_flores_proyecto')

# Modelos
MODELS_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'flower_classifier.pth')

# ==================== CONFIGURACIÓN DEL MODELO ====================
IMAGE_SIZE = 224  # Tamaño estándar para Vision Transformers
BATCH_SIZE = 16
EPOCHS = 10
LEARNING_RATE = 1e-4
NUM_CLASSES = 2  # Flor vs Objeto

# ==================== COLORES ====================
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (128, 128, 128)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_ORANGE = (255, 165, 0)
COLOR_PURPLE = (128, 0, 128)
COLOR_PATH = (173, 216, 230)  # Azul claro para el camino
COLOR_EXPLORED = (255, 182, 193)  # Rosa claro para nodos explorados

# ==================== CONFIGURACIÓN DE BÚSQUEDA ====================
SEARCH_DELAY = 0.3  # Delay en segundos entre pasos de búsqueda
ANALYSIS_DELAY = 1.0  # Delay en segundos para análisis de imagen
ANIMATION_SPEED = 200  # Milisegundos entre frames de animación

# ==================== TIPOS DE CELDAS ====================
CELL_EMPTY = 0
CELL_OBSTACLE = 1
CELL_FLOWER = 2
CELL_OBJECT = 3
CELL_BEE = 4
CELL_HIVE = 5

# ==================== MODOS DE BÚSQUEDA ====================
MODE_BFS_EXPLORATION = "BFS_EXPLORATION"
MODE_BFS_OPTIMAL = "BFS_OPTIMAL"
MODE_DFS_EXPLORATION = "DFS_EXPLORATION"
MODE_DFS_OPTIMAL = "DFS_OPTIMAL"

# ==================== MÉTRICAS ====================
METRICS_FILE = os.path.join(BASE_DIR, 'metrics_results.txt')
