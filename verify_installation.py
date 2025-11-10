"""
Script de verificación del sistema.
Verifica que todas las dependencias estén instaladas correctamente.
"""
import sys
import importlib


def check_module(module_name, display_name=None):
    """
    Verifica si un módulo está instalado.
    
    Args:
        module_name: Nombre del módulo a verificar
        display_name: Nombre a mostrar (opcional)
    
    Returns:
        bool: True si está instalado, False en caso contrario
    """
    if display_name is None:
        display_name = module_name
    
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"  ✓ {display_name}: {version}")
        return True
    except ImportError:
        print(f"  ✗ {display_name}: NO INSTALADO")
        return False


def check_files():
    """Verifica que los archivos necesarios existan."""
    import os
    
    required_files = {
        'Configuración': ['config.py', 'utils.py'],
        'Módulos Principales': [
            'grid_world.py',
            'search_algorithms.py',
            'flower_classifier.py',
            'bee_agent.py',
            'gui_controller.py',
            'main.py'
        ],
        'Scripts': ['train_model.py', 'demo_procesamiento_flores.py'],
        'Documentación': ['README.md', 'requirements.txt']
    }
    
    print("\n" + "="*60)
    print("VERIFICACIÓN DE ARCHIVOS")
    print("="*60)
    
    all_ok = True
    
    for category, files in required_files.items():
        print(f"\n{category}:")
        for file in files:
            if os.path.exists(file):
                print(f"  ✓ {file}")
            else:
                print(f"  ✗ {file} - NO ENCONTRADO")
                all_ok = False
    
    return all_ok


def check_directories():
    """Verifica que las carpetas necesarias existan."""
    import os
    
    required_dirs = {
        'assets': 'Sprites del juego',
        'fotos_flores_proyecto': 'Fotos de flores',
        'objectos': 'Imágenes de objetos',
    }
    
    optional_dirs = {
        'models': 'Modelos entrenados (se crea automáticamente)',
    }
    
    print("\n" + "="*60)
    print("VERIFICACIÓN DE CARPETAS")
    print("="*60)
    
    all_ok = True
    
    print("\nCarpetas requeridas:")
    for dir_name, description in required_dirs.items():
        if os.path.exists(dir_name):
            # Contar archivos
            num_files = len([f for f in os.listdir(dir_name) 
                           if os.path.isfile(os.path.join(dir_name, f))])
            print(f"  ✓ {dir_name}/ ({description}) - {num_files} archivos")
        else:
            print(f"  ✗ {dir_name}/ ({description}) - NO ENCONTRADA")
            all_ok = False
    
    print("\nCarpetas opcionales:")
    for dir_name, description in optional_dirs.items():
        if os.path.exists(dir_name):
            print(f"  ✓ {dir_name}/ ({description})")
        else:
            print(f"  ⚠ {dir_name}/ ({description}) - No existe aún")
    
    return all_ok


def check_sprites():
    """Verifica que los sprites necesarios existan."""
    import os
    
    required_sprites = [
        'abeja.png',
        'colmena.png',
        'arbol.png',
        'flor.png'
    ]
    
    print("\n" + "="*60)
    print("VERIFICACIÓN DE SPRITES")
    print("="*60)
    
    if not os.path.exists('assets'):
        print("\n  ✗ Carpeta 'assets' no encontrada")
        return False
    
    all_ok = True
    print("")
    
    for sprite in required_sprites:
        sprite_path = os.path.join('assets', sprite)
        if os.path.exists(sprite_path):
            print(f"  ✓ {sprite}")
        else:
            print(f"  ✗ {sprite} - NO ENCONTRADO")
            all_ok = False
    
    return all_ok


def main():
    """Función principal de verificación."""
    print("\n" + "="*60)
    print("VERIFICACIÓN DEL SISTEMA - SIMULADOR DE ABEJA INTELIGENTE")
    print("="*60)
    
    # Verificar Python
    print(f"\nPython: {sys.version}")
    print(f"Plataforma: {sys.platform}")
    
    # Verificar módulos
    print("\n" + "="*60)
    print("VERIFICACIÓN DE DEPENDENCIAS")
    print("="*60)
    
    modules_to_check = [
        ('pygame', 'Pygame'),
        ('torch', 'PyTorch'),
        ('torchvision', 'TorchVision'),
        ('cv2', 'OpenCV'),
        ('PIL', 'Pillow'),
        ('numpy', 'NumPy'),
        ('tkinter', 'Tkinter'),
    ]
    
    print("\nDependencias principales:")
    results = []
    for module_name, display_name in modules_to_check:
        result = check_module(module_name, display_name)
        results.append(result)
    
    # Verificar archivos
    files_ok = check_files()
    
    # Verificar directorios
    dirs_ok = check_directories()
    
    # Verificar sprites
    sprites_ok = check_sprites()
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    
    all_modules_ok = all(results)
    
    print(f"\nDependencias: {'✓ OK' if all_modules_ok else '✗ FALTAN MÓDULOS'}")
    print(f"Archivos: {'✓ OK' if files_ok else '✗ FALTAN ARCHIVOS'}")
    print(f"Carpetas: {'✓ OK' if dirs_ok else '✗ FALTAN CARPETAS'}")
    print(f"Sprites: {'✓ OK' if sprites_ok else '✗ FALTAN SPRITES'}")
    
    if all_modules_ok and files_ok and dirs_ok and sprites_ok:
        print("\n" + "="*60)
        print("✓ SISTEMA LISTO PARA USAR")
        print("="*60)
        print("\nPróximos pasos:")
        print("  1. Entrenar el modelo: python train_model.py")
        print("  2. Ejecutar el simulador: python main.py")
    else:
        print("\n" + "="*60)
        print("⚠ SISTEMA INCOMPLETO")
        print("="*60)
        print("\nAcciones recomendadas:")
        
        if not all_modules_ok:
            print("  - Instalar dependencias: pip install -r requirements.txt")
            print("    O ejecutar: .\\install.ps1")
        
        if not files_ok:
            print("  - Verificar que todos los archivos .py estén presentes")
        
        if not dirs_ok:
            print("  - Crear las carpetas faltantes y añadir los recursos necesarios")
        
        if not sprites_ok:
            print("  - Añadir los sprites requeridos en la carpeta 'assets/'")
    
    print("")


if __name__ == "__main__":
    main()
