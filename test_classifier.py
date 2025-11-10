"""
Script de prueba simple para verificar que el clasificador funciona
"""
import os
from flower_classifier import FlowerClassifier
from utils import load_random_flower_test_image, load_random_object_image
from config import TEST_DIR, OBJECTS_DIR

def test_classifier():
    print("="*60)
    print("PRUEBA DEL CLASIFICADOR DE FLORES")
    print("="*60)
    
    # Crear clasificador
    print("\n1. Inicializando clasificador...")
    try:
        classifier = FlowerClassifier()
        print("   ✓ Clasificador inicializado")
    except Exception as e:
        print(f"   ✗ Error inicializando clasificador: {e}")
        return False
    
    # Probar con imagen de flor
    print("\n2. Probando con imagen de flor del conjunto de prueba...")
    flower_image = load_random_flower_test_image(TEST_DIR)
    if flower_image:
        print(f"   Imagen seleccionada: {os.path.basename(flower_image)}")
        try:
            prediction, confidence = classifier.predict(flower_image)
            print(f"   Predicción: {prediction}")
            print(f"   Confianza: {confidence:.2f}")
            print(f"   ✓ Clasificación exitosa")
        except Exception as e:
            print(f"   ✗ Error clasificando: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("   ✗ No se encontró imagen de flor")
    
    # Probar con imagen de objeto
    print("\n3. Probando con imagen de objeto...")
    object_image = load_random_object_image(OBJECTS_DIR)
    if object_image:
        print(f"   Imagen seleccionada: {os.path.basename(object_image)}")
        try:
            prediction, confidence = classifier.predict(object_image)
            print(f"   Predicción: {prediction}")
            print(f"   Confianza: {confidence:.2f}")
            print(f"   ✓ Clasificación exitosa")
        except Exception as e:
            print(f"   ✗ Error clasificando: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("   ✗ No se encontró imagen de objeto")
    
    print("\n" + "="*60)
    print("PRUEBA COMPLETADA")
    print("="*60)
    return True

if __name__ == "__main__":
    test_classifier()
