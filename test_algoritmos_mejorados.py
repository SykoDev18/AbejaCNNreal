"""
Script de prueba para los algoritmos BFS y DFS mejorados.
Compara la eficiencia y el comportamiento de ambos algoritmos.
"""

import pygame
import sys
from grid_world import GridWorld
from search_algorithms import BFSSearch, DFSSearch, PathFinder
from config import *
from utils import Logger

def main():
    """Función principal de prueba."""
    print("="*60)
    print("PRUEBA DE ALGORITMOS BFS Y DFS MEJORADOS")
    print("="*60)
    
    # Inicializar Pygame
    pygame.init()
    
    # Crear mundo
    Logger.log("Creando mundo de prueba...")
    world = GridWorld()
    world.initialize_world()
    
    # Definir posiciones de prueba
    start_pos = (0, 0)
    goal_pos = (GRID_SIZE - 1, GRID_SIZE - 1)
    
    print(f"\nInicio: {start_pos}")
    print(f"Meta: {goal_pos}")
    print(f"Tamaño del grid: {GRID_SIZE}x{GRID_SIZE}")
    print(f"Obstáculos: {OBSTACLE_PERCENTAGE*100}%")
    
    # Crear instancias de los algoritmos
    bfs = BFSSearch(world)
    dfs = DFSSearch(world)
    
    print("\n" + "="*60)
    print("EJECUTANDO BFS (Breadth-First Search)")
    print("="*60)
    
    # Ejecutar BFS
    path_bfs, explored_bfs, steps_bfs = bfs.search(start_pos, goal_pos, mode='optimal')
    
    print(f"\nResultados BFS:")
    print(f"  - Nodos explorados: {len(explored_bfs)}")
    print(f"  - Longitud del camino: {len(path_bfs)}")
    print(f"  - Pasos totales: {steps_bfs}")
    print(f"  - Camino encontrado: {'Sí' if path_bfs else 'No'}")
    
    if path_bfs:
        print(f"  - Primeros 5 nodos del camino: {path_bfs[:5]}")
        print(f"  - Últimos 5 nodos del camino: {path_bfs[-5:]}")
    
    print("\n" + "="*60)
    print("EJECUTANDO DFS (Depth-First Search)")
    print("="*60)
    
    # Ejecutar DFS
    path_dfs, explored_dfs, steps_dfs = dfs.search(start_pos, goal_pos, mode='optimal')
    
    print(f"\nResultados DFS:")
    print(f"  - Nodos explorados: {len(explored_dfs)}")
    print(f"  - Longitud del camino: {len(path_dfs)}")
    print(f"  - Pasos totales: {steps_dfs}")
    print(f"  - Camino encontrado: {'Sí' if path_dfs else 'No'}")
    
    if path_dfs:
        print(f"  - Primeros 5 nodos del camino: {path_dfs[:5]}")
        print(f"  - Últimos 5 nodos del camino: {path_dfs[-5:]}")
    
    # Comparación
    print("\n" + "="*60)
    print("COMPARACIÓN DE ALGORITMOS")
    print("="*60)
    
    if path_bfs and path_dfs:
        print(f"\n{'Métrica':<30} {'BFS':<15} {'DFS':<15} {'Mejor':<10}")
        print("-" * 70)
        
        print(f"{'Nodos explorados':<30} {len(explored_bfs):<15} {len(explored_dfs):<15} ", end="")
        if len(explored_bfs) < len(explored_dfs):
            print("BFS ✓")
        elif len(explored_dfs) < len(explored_bfs):
            print("DFS ✓")
        else:
            print("Empate")
        
        print(f"{'Longitud del camino':<30} {len(path_bfs):<15} {len(path_dfs):<15} ", end="")
        if len(path_bfs) < len(path_dfs):
            print("BFS ✓")
        elif len(path_dfs) < len(path_bfs):
            print("DFS ✓")
        else:
            print("Empate")
        
        print(f"{'Pasos de ejecución':<30} {steps_bfs:<15} {steps_dfs:<15} ", end="")
        if steps_bfs < steps_dfs:
            print("BFS ✓")
        elif steps_dfs < steps_bfs:
            print("DFS ✓")
        else:
            print("Empate")
        
        # Análisis de eficiencia
        print(f"\n{'Análisis':<30}")
        print("-" * 70)
        
        efficiency_bfs = len(path_bfs) / len(explored_bfs) if explored_bfs else 0
        efficiency_dfs = len(path_dfs) / len(explored_dfs) if explored_dfs else 0
        
        print(f"{'Eficiencia (camino/explorados)':<30} {efficiency_bfs:.3f}{'':>9} {efficiency_dfs:.3f}")
        
        print("\n💡 Conclusiones:")
        print(f"  • BFS garantiza el camino más corto: {len(path_bfs)} pasos")
        print(f"  • DFS puede explorar menos nodos pero no garantiza optimalidad")
        print(f"  • BFS exploró {len(explored_bfs)} nodos vs {len(explored_dfs)} de DFS")
        
        if len(path_bfs) == len(path_dfs):
            print(f"  • En este caso, ambos encontraron caminos de igual longitud")
        elif len(path_bfs) < len(path_dfs):
            diff = len(path_dfs) - len(path_bfs)
            print(f"  • BFS encontró un camino {diff} nodos más corto que DFS")
        else:
            print(f"  • DFS tuvo suerte y encontró un camino competitivo")
    
    elif path_bfs:
        print("\n⚠️ Solo BFS encontró un camino")
    elif path_dfs:
        print("\n⚠️ Solo DFS encontró un camino")
    else:
        print("\n❌ Ningún algoritmo encontró un camino")
    
    print("\n" + "="*60)
    print("MEJORAS IMPLEMENTADAS")
    print("="*60)
    print("""
    ✓ Mejor manejo de nodos visitados (parent_map desde el inicio)
    ✓ Eliminación de chequeos redundantes
    ✓ Tracking más eficiente de nodos explorados
    ✓ Reconstrucción de caminos más robusta
    ✓ Logging detallado para debugging
    ✓ Soporte para animación paso a paso
    ✓ Código más limpio y mantenible
    """)
    
    pygame.quit()
    print("\nPrueba completada exitosamente! 🐝✨")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        Logger.log(f"Error en prueba: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)
