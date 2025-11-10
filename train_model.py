"""
Script para entrenar el modelo de clasificación de flores.
Ejecuta este script antes de usar el simulador para obtener mejores resultados.
"""
import os
import sys
from flower_classifier import FlowerClassifier
from config import TRAIN_DIR, MODEL_PATH, EPOCHS, BATCH_SIZE
from utils import Logger


def train_model():
    """Entrena el modelo clasificador de flores vs objetos."""
    Logger.log("=" * 60)
    Logger.log("ENTRENAMIENTO DEL MODELO DE CLASIFICACIÓN")
    Logger.log("=" * 60)
    
    # Verificar que existe el directorio de entrenamiento
    if not os.path.exists(TRAIN_DIR):
        Logger.log(f"Error: No se encontró el directorio de entrenamiento: {TRAIN_DIR}", "ERROR")
        Logger.log("Asegúrate de que el dataset esté en la ubicación correcta.", "ERROR")
        return False
    
    # Verificar carpetas de flores
    flower_folders = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']
    found_folders = []
    
    for folder in flower_folders:
        folder_path = os.path.join(TRAIN_DIR, folder)
        if os.path.exists(folder_path):
            num_images = len([f for f in os.listdir(folder_path) 
                            if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
            found_folders.append(folder)
            Logger.log(f"  ✓ {folder}: {num_images} imágenes")
    
    if not found_folders:
        Logger.log("No se encontraron carpetas de flores en el dataset", "ERROR")
        return False
    
    Logger.log(f"\nDataset encontrado con {len(found_folders)} tipos de flores")
    Logger.log(f"Configuración:")
    Logger.log(f"  - Épocas: {EPOCHS}")
    Logger.log(f"  - Batch size: {BATCH_SIZE}")
    Logger.log(f"  - Modelo se guardará en: {MODEL_PATH}")
    
    # Crear clasificador
    classifier = FlowerClassifier()
    
    # Entrenar
    Logger.log("\nIniciando entrenamiento...")
    Logger.log("Esto puede tomar varios minutos dependiendo del hardware...")
    
    try:
        classifier.train(train_dir=TRAIN_DIR, epochs=EPOCHS, batch_size=BATCH_SIZE)
        Logger.log("\n✓ Entrenamiento completado exitosamente!")
        Logger.log(f"Modelo guardado en: {MODEL_PATH}")
        return True
    
    except Exception as e:
        Logger.log(f"\n✗ Error durante el entrenamiento: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal."""
    print("\n🌸 ENTRENADOR DE MODELO - CLASIFICADOR DE FLORES 🌸\n")
    
    # Preguntar al usuario
    response = input("¿Deseas entrenar el modelo? (s/n): ").strip().lower()
    
    if response == 's' or response == 'si' or response == 'yes' or response == 'y':
        success = train_model()
        
        if success:
            print("\n" + "="*60)
            print("✓ ENTRENAMIENTO COMPLETADO")
            print("="*60)
            print("\nAhora puedes ejecutar el simulador principal:")
            print("  python main.py")
            print()
        else:
            print("\n" + "="*60)
            print("✗ EL ENTRENAMIENTO FALLÓ")
            print("="*60)
            print("\nRevisa los errores anteriores y asegúrate de que:")
            print("  1. El dataset esté en la ubicación correcta")
            print("  2. Las dependencias estén instaladas (PyTorch, torchvision, etc.)")
            print()
    else:
        print("\nEntrenamiento cancelado.")
        print("El simulador usará un modelo sin entrenar (menor precisión).")


if __name__ == "__main__":
    main()
