"""
Clase GridWorld - Representa el mundo cuadriculado del simulador.
Maneja la generación aleatoria del mundo, obstáculos, flores y objetos.
"""
import random
import pygame
from config import *
from utils import Logger, load_random_object_sprite


class GridWorld:
    """
    Clase que representa el mundo cuadriculado donde se mueve la abeja.
    Maneja la generación de obstáculos, flores, objetos y renderizado.
    """
    
    def __init__(self, size=GRID_SIZE):
        """
        Inicializa el mundo cuadriculado.
        
        Args:
            size: Tamaño de la cuadrícula (NxN)
        """
        self.size = size
        self.grid = {}  # Diccionario para almacenar el estado de cada celda
        self.bee_pos = None
        self.hive_pos = None
        
        # Listas para tracking
        self.flowers = []
        self.objects = []
        self.obstacles = []
        
        # Sprites
        self.sprites = {}
        self.load_sprites()
        
        Logger.log(f"GridWorld inicializado con tamaño {size}x{size}")
    
    def load_sprites(self):
        """Carga todos los sprites necesarios para el mundo."""
        try:
            # Cargar y escalar sprites principales
            self.sprites['bee'] = pygame.transform.scale(
                pygame.image.load(SPRITE_BEE), (CELL_SIZE, CELL_SIZE)
            )
            self.sprites['hive'] = pygame.transform.scale(
                pygame.image.load(SPRITE_HIVE), (CELL_SIZE, CELL_SIZE)
            )
            self.sprites['tree'] = pygame.transform.scale(
                pygame.image.load(SPRITE_TREE), (CELL_SIZE, CELL_SIZE)
            )
            self.sprites['flower'] = pygame.transform.scale(
                pygame.image.load(SPRITE_FLOWER), (CELL_SIZE, CELL_SIZE)
            )
            self.sprites['object'] = pygame.transform.scale(
                pygame.image.load(SPRITE_OBJECT), (CELL_SIZE, CELL_SIZE)
            )
            
            Logger.log("Sprites cargados exitosamente")
        except Exception as e:
            Logger.log(f"Error cargando sprites: {e}", "ERROR")
            # Crear sprites de respaldo (rectángulos de colores)
            self.create_fallback_sprites()
    
    def create_fallback_sprites(self):
        """Crea sprites de respaldo si no se pueden cargar las imágenes."""
        for sprite_name, color in [
            ('bee', COLOR_YELLOW),
            ('hive', COLOR_ORANGE),
            ('tree', (139, 69, 19)),  # Marrón
            ('flower', (255, 105, 180)),  # Rosa
            ('object', COLOR_BLUE)  # Azul para objetos
        ]:
            surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
            surface.fill(color)
            self.sprites[sprite_name] = surface
    
    def initialize_world(self, bee_pos=None, hive_pos=None):
        """
        Inicializa el mundo con posiciones aleatorias de elementos.
        
        Args:
            bee_pos: Posición inicial de la abeja (x, y). Si es None, se genera aleatoriamente.
            hive_pos: Posición de la colmena (x, y). Si es None, se genera aleatoriamente.
        """
        # Limpiar el mundo
        self.grid = {}
        self.flowers = []
        self.objects = []
        self.obstacles = []
        
        # Inicializar todas las celdas como vacías
        for i in range(self.size):
            for j in range(self.size):
                self.grid[(i, j)] = CELL_EMPTY
        
        # Establecer posición de la abeja
        if bee_pos is None:
            self.bee_pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        else:
            self.bee_pos = bee_pos
        self.grid[self.bee_pos] = CELL_BEE
        
        # Establecer posición de la colmena (asegurándose de que no sea la misma que la abeja)
        if hive_pos is None:
            while True:
                self.hive_pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
                if self.hive_pos != self.bee_pos:
                    break
        else:
            self.hive_pos = hive_pos
        self.grid[self.hive_pos] = CELL_HIVE
        
        # Generar obstáculos
        num_obstacles = int(self.size * self.size * OBSTACLE_PERCENTAGE)
        self.generate_obstacles(num_obstacles)
        
        # Generar flores
        num_flowers = int(self.size * self.size * FLOWER_PERCENTAGE)
        self.generate_flowers(num_flowers)
        
        # Generar objetos (no-flores)
        num_objects = int(self.size * self.size * OBJECT_PERCENTAGE)
        self.generate_objects(num_objects)
        
        Logger.log(f"Mundo generado: {num_obstacles} obstáculos, {num_flowers} flores, {num_objects} objetos")
        Logger.log(f"Abeja en {self.bee_pos}, Colmena en {self.hive_pos}")
    
    def generate_obstacles(self, count):
        """Genera obstáculos aleatorios en el mundo."""
        placed = 0
        attempts = 0
        max_attempts = count * 10
        
        while placed < count and attempts < max_attempts:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            pos = (x, y)
            
            # No colocar obstáculos donde ya hay algo importante
            if self.grid[pos] == CELL_EMPTY:
                self.grid[pos] = CELL_OBSTACLE
                self.obstacles.append(pos)
                placed += 1
            
            attempts += 1
    
    def generate_flowers(self, count):
        """Genera flores aleatorias en el mundo."""
        placed = 0
        attempts = 0
        max_attempts = count * 10
        
        while placed < count and attempts < max_attempts:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            pos = (x, y)
            
            # Solo colocar en celdas vacías
            if self.grid[pos] == CELL_EMPTY:
                self.grid[pos] = CELL_FLOWER
                self.flowers.append(pos)
                placed += 1
            
            attempts += 1
    
    def generate_objects(self, count):
        """Genera objetos (no-flores) aleatorios en el mundo."""
        placed = 0
        attempts = 0
        max_attempts = count * 10
        
        while placed < count and attempts < max_attempts:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            pos = (x, y)
            
            # Solo colocar en celdas vacías
            if self.grid[pos] == CELL_EMPTY:
                self.grid[pos] = CELL_OBJECT
                self.objects.append(pos)
                placed += 1
            
            attempts += 1
    
    def is_walkable(self, position):
        """
        Verifica si una posición es transitable (no es obstáculo y está dentro del grid).
        
        Args:
            position: Tupla (x, y) de la posición a verificar
            
        Returns:
            bool: True si es transitable, False en caso contrario
        """
        x, y = position
        
        # Verificar límites
        if not (0 <= x < self.size and 0 <= y < self.size):
            return False
        
        # Verificar que no sea obstáculo
        return self.grid.get(position, CELL_EMPTY) != CELL_OBSTACLE
    
    def get_cell_type(self, position):
        """
        Obtiene el tipo de celda en una posición.
        
        Args:
            position: Tupla (x, y)
            
        Returns:
            int: Tipo de celda (CELL_EMPTY, CELL_OBSTACLE, etc.)
        """
        return self.grid.get(position, CELL_EMPTY)
    
    def render(self, screen, path=None, explored=None):
        """
        Renderiza el mundo en la pantalla de Pygame.
        
        Args:
            screen: Superficie de Pygame donde renderizar
            path: Lista de posiciones que representan el camino (opcional)
            explored: Conjunto de posiciones exploradas (opcional)
        """
        # Dibujar fondo
        screen.fill(COLOR_WHITE)
        
        # Dibujar grid
        for i in range(self.size):
            for j in range(self.size):
                pos = (i, j)
                rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                # Dibujar celdas exploradas
                if explored and pos in explored and pos != self.bee_pos:
                    pygame.draw.rect(screen, COLOR_EXPLORED, rect)
                
                # Dibujar camino
                if path and pos in path and pos != self.bee_pos and pos != self.hive_pos:
                    pygame.draw.rect(screen, COLOR_PATH, rect)
                
                # Dibujar contenido de la celda
                cell_type = self.grid[pos]
                
                if cell_type == CELL_OBSTACLE:
                    screen.blit(self.sprites['tree'], (j * CELL_SIZE, i * CELL_SIZE))
                elif cell_type == CELL_FLOWER:
                    screen.blit(self.sprites['flower'], (j * CELL_SIZE, i * CELL_SIZE))
                elif cell_type == CELL_OBJECT:
                    screen.blit(self.sprites['object'], (j * CELL_SIZE, i * CELL_SIZE))
                elif cell_type == CELL_HIVE and pos == self.hive_pos:
                    screen.blit(self.sprites['hive'], (j * CELL_SIZE, i * CELL_SIZE))
                
                # Dibujar bordes de celda
                pygame.draw.rect(screen, COLOR_BLACK, rect, 1)
        
        # Dibujar abeja (siempre encima)
        if self.bee_pos:
            bee_x, bee_y = self.bee_pos
            screen.blit(self.sprites['bee'], (bee_y * CELL_SIZE, bee_x * CELL_SIZE))
    
    def set_bee_position(self, position):
        """Actualiza la posición de la abeja."""
        # Limpiar posición anterior
        if self.bee_pos and self.bee_pos != self.hive_pos:
            old_type = CELL_EMPTY
            if self.bee_pos in self.flowers:
                old_type = CELL_FLOWER
            elif self.bee_pos in self.objects:
                old_type = CELL_OBJECT
            self.grid[self.bee_pos] = old_type
        
        # Establecer nueva posición
        self.bee_pos = position
        if position != self.hive_pos:
            self.grid[position] = CELL_BEE
    
    def get_neighbors(self, position):
        """
        Obtiene los vecinos transitables de una posición.
        
        Args:
            position: Tupla (x, y)
            
        Returns:
            Lista de tuplas (x, y) de vecinos transitables
        """
        x, y = position
        neighbors = []
        
        # Arriba, Derecha, Abajo, Izquierda
        for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            
            if self.is_walkable(neighbor):
                neighbors.append(neighbor)
        
        return neighbors
