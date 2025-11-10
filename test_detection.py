"""
Script para probar si ahora detecta correctamente las flores y objetos
"""
from grid_world import GridWorld
from bee_agent import BeeAgent
from flower_classifier import FlowerClassifier
from config import *

def test_detection():
    print("="*60)
    print("PRUEBA DE DETECCIÓN DE FLORES Y OBJETOS")
    print("="*60)
    
    # Crear mundo y classifier
    grid = GridWorld(GRID_SIZE)
    classifier = FlowerClassifier()
    agent = BeeAgent(grid, classifier)
    
    # Inicializar mundo con posiciones específicas
    bee_pos = (0, 0)
    hive_pos = (19, 19)
    grid.initialize_world(bee_pos, hive_pos)
    agent.set_position(bee_pos)
    
    print(f"\nMundo inicializado:")
    print(f"  Flores: {len(grid.flowers)}")
    print(f"  Objetos: {len(grid.objects)}")
    print(f"  Obstáculos: {len(grid.obstacles)}")
    
    if grid.flowers:
        print(f"\nPrimeras 3 posiciones de flores: {grid.flowers[:3]}")
    if grid.objects:
        print(f"Primeras 3 posiciones de objetos: {grid.objects[:3]}")
    
    # Probar detección en una flor
    if grid.flowers:
        test_pos = grid.flowers[0]
        print(f"\n Probando detección en flor en posición {test_pos}")
        cell_type_before = grid.get_cell_type(test_pos)
        print(f"  Tipo de celda ANTES de mover: {cell_type_before}")
        
        agent.move_to(test_pos)
        cell_type_after = grid.get_cell_type(test_pos)
        print(f"  Tipo de celda DESPUÉS de mover: {cell_type_after}")
        
        # Detectar usando el tipo anterior
        _, classification, confidence, image = agent.detect_cell_content(cell_type_before)
        print(f"  Imagen: {image}")
        print(f"  Clasificación: {classification}")
        print(f"  Confianza: {confidence:.2f}")
    
    # Probar detección en un objeto
    if grid.objects:
        test_pos = grid.objects[0]
        print(f"\n🔍 Probando detección en objeto en posición {test_pos}")
        cell_type_before = grid.get_cell_type(test_pos)
        print(f"  Tipo de celda ANTES de mover: {cell_type_before}")
        
        agent.move_to(test_pos)
        cell_type_after = grid.get_cell_type(test_pos)
        print(f"  Tipo de celda DESPUÉS de mover: {cell_type_after}")
        
        # Detectar usando el tipo anterior
        _, classification, confidence, image = agent.detect_cell_content(cell_type_before)
        print(f"  Imagen: {image}")
        print(f"  Clasificación: {classification}")
        print(f"  Confianza: {confidence:.2f}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    test_detection()
