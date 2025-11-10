"""
Algoritmos de búsqueda: BFS y DFS con modos de exploración y óptimo.
Implementa ambos algoritmos con visualización paso a paso.
"""
from collections import deque
from utils import Logger


class SearchAlgorithm:
    """Clase base para algoritmos de búsqueda."""
    
    def __init__(self, grid_world):
        """
        Inicializa el algoritmo de búsqueda.
        
        Args:
            grid_world: Instancia de GridWorld
        """
        self.grid_world = grid_world
        self.start = None
        self.goal = None
        self.explored = set()
        self.path = []
        self.parent_map = {}  # Para reconstruir el camino
        self.graph = None  # Para usar con algoritmo de bfs_chida.py
    
    def _build_graph(self):
        """
        Construye el grafo desde grid_world para usar con bfs_meta/dfs_meta.
        Convierte la estructura de GridWorld al formato de diccionario usado en bfs_chida.py
        """
        graph = {}
        size = self.grid_world.size
        
        for i in range(size):
            for j in range(size):
                if self.grid_world.is_walkable((i, j)):
                    neighbors = self.grid_world.get_neighbors((i, j))
                    graph[(i, j)] = neighbors
        
        return graph
    
    def search(self, start, goal):
        """
        Método abstracto para realizar la búsqueda.
        Debe ser implementado por las subclases.
        """
        raise NotImplementedError("Subclases deben implementar search()")
    
    def reconstruct_path(self, start, goal):
        """
        Reconstruye el camino desde start hasta goal usando parent_map.
        
        Returns:
            Lista de posiciones desde start hasta goal
        """
        if goal not in self.parent_map and goal != start:
            return []
        
        path = []
        current = goal
        
        while current != start:
            path.append(current)
            current = self.parent_map.get(current)
            if current is None:
                return []  # No hay camino
        
        path.append(start)
        path.reverse()
        return path
    
    def get_exploration_path(self):
        """Retorna el camino de exploración completo."""
        return list(self.explored)
    
    def get_optimal_path(self):
        """Retorna el camino óptimo."""
        return self.path


class BFSSearch(SearchAlgorithm):
    """
    Implementación de Búsqueda en Amplitud (BFS).
    Modo 1: Exploración - explora nivel por nivel hasta encontrar la meta.
    Modo 2: Óptimo - retorna el camino más corto.
    """
    
    def __init__(self, grid_world):
        super().__init__(grid_world)
        self.algorithm_name = "BFS (Breadth-First Search)"
    
    def search(self, start, goal, mode='exploration'):
        """
        Ejecuta BFS desde start hasta goal.
        Código EXACTO de bfs_chida.py - función bfs_meta().
        
        Args:
            start: Posición inicial (x, y) - llamado 'inicio' en bfs_chida.py
            goal: Posición objetivo (x, y) - llamado 'meta' en bfs_chida.py
            mode: 'exploration' o 'optimal'
            
        Returns:
            Tupla (path, explored, steps) donde:
                - path: camino desde start hasta goal
                - explored: conjunto de nodos explorados
                - steps: número de pasos
        """
        Logger.log(f"Iniciando {self.algorithm_name} - Modo: {mode}")
        
        # Construir el grafo desde grid_world
        graph = self._build_graph()
        
        # ========== CÓDIGO EXACTO DE bfs_chida.py - función bfs_meta() ==========
        inicio = start
        meta = goal
        
        visitados = set()
        cola = deque([inicio])
        parent = {inicio: None}
        explored = []
        
        while cola:
            nodo = cola.popleft()
            if nodo not in visitados:
                visitados.add(nodo)
                explored.append(nodo)
                if mode == 'optimal' and nodo == meta:
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
        # ========== FIN CÓDIGO EXACTO ==========
        
        # ========== FIN CÓDIGO EXACTO ==========
        
        # Actualizar variables de instancia
        self.start = inicio
        self.goal = meta
        self.explored = visitados
        self.parent_map = parent
        self.path = path
        
        steps = len(explored)
        
        Logger.log(f"¡Meta encontrada en {steps} pasos!")
        Logger.log(f"Camino encontrado con longitud: {len(self.path)}")
        Logger.log(f"Nodos explorados: {len(self.explored)}")
        
        # Retornar explored como lista para mantener orden
        return self.path, explored, steps
    
    def search_step_by_step(self, start, goal, mode='exploration'):
        """
        Generador que ejecuta BFS paso a paso para animación.
        Código EXACTO de bfs_chida.py adaptado a generador.
        
        Yields:
            Tupla (current_pos, explored_set, found, path)
        """
        # Construir el grafo desde grid_world
        graph = self._build_graph()
        
        # ========== CÓDIGO EXACTO DE bfs_chida.py (adaptado a generador) ==========
        inicio = start
        meta = goal
        
        visitados = set()
        cola = deque([inicio])
        parent = {inicio: None}
        
        while cola:
            nodo = cola.popleft()
            if nodo not in visitados:
                visitados.add(nodo)
                
                # Yield estado actual
                if mode == 'optimal' and nodo == meta:
                    # Reconstruct path
                    path = []
                    current = meta
                    while current is not None:
                        path.append(current)
                        current = parent.get(current)
                    path.reverse()
                    
                    # Actualizar variables de instancia
                    self.start = inicio
                    self.goal = meta
                    self.explored = visitados
                    self.parent_map = parent
                    self.path = path
                    
                    yield (nodo, visitados.copy(), True, path)
                    return
                
                yield (nodo, visitados.copy(), False, [])
                
                for vecino in graph.get(nodo, []):
                    if vecino not in parent:
                        cola.append(vecino)
                        parent[vecino] = nodo
        # ========== FIN CÓDIGO EXACTO ==========
        
        # No se encontró camino o exploración completa
        yield (None, visitados.copy(), False, [])


class DFSSearch(SearchAlgorithm):
    """
    Implementación de Búsqueda en Profundidad (DFS).
    Modo 1: Exploración - explora en profundidad hasta encontrar la meta.
    Modo 2: Óptimo - intenta encontrar un camino (no necesariamente el más corto).
    """
    
    def __init__(self, grid_world):
        super().__init__(grid_world)
        self.algorithm_name = "DFS (Depth-First Search)"
    
    def search(self, start, goal, mode='exploration'):
        """
        Ejecuta DFS desde start hasta goal.
        Código EXACTO de bfs_chida.py - función dfs_meta().
        
        Args:
            start: Posición inicial (x, y) - llamado 'inicio' en bfs_chida.py
            goal: Posición objetivo (x, y) - llamado 'meta' en bfs_chida.py
            mode: 'exploration' o 'optimal'
            
        Returns:
            Tupla (path, explored, steps)
        """
        Logger.log(f"Iniciando {self.algorithm_name} - Modo: {mode}")
        
        # Construir el grafo desde grid_world
        graph = self._build_graph()
        
        # ========== CÓDIGO EXACTO DE bfs_chida.py - función dfs_meta() ==========
        inicio = start
        meta = goal
        
        visitados = set()
        pila = [inicio]
        parent = {inicio: None}
        explored = []
        
        while pila:
            nodo = pila.pop()
            if nodo not in visitados:
                visitados.add(nodo)
                explored.append(nodo)
                if mode == 'optimal' and nodo == meta:
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
        # ========== FIN CÓDIGO EXACTO ==========
        
        # Actualizar variables de instancia
        self.start = inicio
        self.goal = meta
        self.explored = visitados
        self.parent_map = parent
        self.path = path
        
        steps = len(explored)
        
        Logger.log(f"¡Meta encontrada en {steps} pasos!")
        Logger.log(f"Camino encontrado con longitud: {len(self.path)}")
        Logger.log(f"Nodos explorados: {len(self.explored)}")
        
        # Retornar explored como lista para mantener orden
        return self.path, explored, steps
    
    def search_step_by_step(self, start, goal, mode='exploration'):
        """
        Generador que ejecuta DFS paso a paso para animación.
        Código EXACTO de bfs_chida.py adaptado a generador.
        
        Yields:
            Tupla (current_pos, explored_set, found, path)
        """
        # Construir el grafo desde grid_world
        graph = self._build_graph()
        
        # ========== CÓDIGO EXACTO DE bfs_chida.py (adaptado a generador) ==========
        inicio = start
        meta = goal
        
        visitados = set()
        pila = [inicio]
        parent = {inicio: None}
        
        while pila:
            nodo = pila.pop()
            if nodo not in visitados:
                visitados.add(nodo)
                
                # Yield estado actual
                if mode == 'optimal' and nodo == meta:
                    # Reconstruct path
                    path = []
                    current = meta
                    while current is not None:
                        path.append(current)
                        current = parent.get(current)
                    path.reverse()
                    
                    # Actualizar variables de instancia
                    self.start = inicio
                    self.goal = meta
                    self.explored = visitados
                    self.parent_map = parent
                    self.path = path
                    
                    yield (nodo, visitados.copy(), True, path)
                    return
                
                yield (nodo, visitados.copy(), False, [])
                
                for vecino in reversed(graph.get(nodo, [])):
                    if vecino not in parent:
                        pila.append(vecino)
                        parent[vecino] = nodo
        # ========== FIN CÓDIGO EXACTO ==========
        
        # No se encontró camino o exploración completa
        yield (None, visitados.copy(), False, [])


class PathFinder:
    """
    Clase unificadora para gestionar algoritmos de búsqueda.
    Facilita el cambio entre BFS y DFS.
    """
    
    def __init__(self, grid_world):
        self.grid_world = grid_world
        self.bfs = BFSSearch(grid_world)
        self.dfs = DFSSearch(grid_world)
        self.current_algorithm = None
    
    def set_algorithm(self, algorithm_type):
        """
        Establece el algoritmo de búsqueda a usar.
        
        Args:
            algorithm_type: 'BFS' o 'DFS'
        """
        if algorithm_type.upper() == 'BFS':
            self.current_algorithm = self.bfs
            Logger.log("Algoritmo establecido: BFS")
        elif algorithm_type.upper() == 'DFS':
            self.current_algorithm = self.dfs
            Logger.log("Algoritmo establecido: DFS")
        else:
            Logger.log(f"Algoritmo desconocido: {algorithm_type}", "ERROR")
    
    def find_path(self, start, goal, mode='exploration'):
        """
        Encuentra un camino usando el algoritmo actual.
        
        Args:
            start: Posición inicial
            goal: Posición objetivo
            mode: 'exploration' o 'optimal'
            
        Returns:
            Tupla (path, explored, steps)
        """
        if self.current_algorithm is None:
            Logger.log("No se ha establecido un algoritmo", "ERROR")
            return [], set(), 0
        
        return self.current_algorithm.search(start, goal, mode)
    
    def find_path_animated(self, start, goal, mode='exploration'):
        """
        Retorna un generador para animación paso a paso.
        
        Returns:
            Generador que yield (current_pos, explored, found, path)
        """
        if self.current_algorithm is None:
            Logger.log("No se ha establecido un algoritmo", "ERROR")
            return
        
        return self.current_algorithm.search_step_by_step(start, goal, mode)
