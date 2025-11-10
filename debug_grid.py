"""
Script de debug para verificar qué hay en el grid
"""
from grid_world import GridWorld
from config import *

def debug_grid():
    print("="*60)
    print("DEBUG DEL GRID WORLD")
    print("="*60)
    
    # Crear mundo
    grid = GridWorld(GRID_SIZE)
    
    # Contar elementos
    flowers = []
    objects = []
    obstacles = []
    empty = []
    
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            pos = (x, y)
            cell_type = grid.get_cell_type(pos)
            
            if cell_type == CELL_FLOWER:
                flowers.append(pos)
            elif cell_type == CELL_OBJECT:
                objects.append(pos)
            elif cell_type == CELL_OBSTACLE:
                obstacles.append(pos)
            elif cell_type == CELL_EMPTY:
                empty.append(pos)
    
    print(f"\nEstadísticas del mundo {GRID_SIZE}x{GRID_SIZE}:")
    print(f"  Flores: {len(flowers)}")
    print(f"  Objetos: {len(objects)}")
    print(f"  Obstáculos: {len(obstacles)}")
    print(f"  Vacías: {len(empty)}")
    print(f"  Abeja: {grid.bee_pos}")
    print(f"  Colmena: {grid.hive_pos}")
    
    if flowers:
        print(f"\nPrimeras 5 posiciones de flores: {flowers[:5]}")
    if objects:
        print(f"Primeras 5 posiciones de objetos: {objects[:5]}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    debug_grid()
