#!/usr/bin/env python3
"""
Script de inicio rápido multiplataforma.
Funciona en Windows, Linux y macOS.
"""
import os
import sys
import subprocess


def print_header():
    """Imprime el encabezado."""
    print("\n" + "="*60)
    print("🐝 SIMULADOR DE ABEJA INTELIGENTE 🌸")
    print("="*60 + "\n")


def print_menu():
    """Muestra el menú de opciones."""
    print("Selecciona una opción:\n")
    print("1. Verificar instalación")
    print("2. Instalar dependencias")
    print("3. Ver demo de procesamiento de imágenes")
    print("4. Entrenar modelo de clasificación")
    print("5. Ejecutar simulador principal")
    print("6. Salir\n")


def run_command(command):
    """
    Ejecuta un comando del sistema.
    
    Args:
        command: Lista con el comando y sus argumentos
        
    Returns:
        bool: True si tuvo éxito, False en caso contrario
    """
    try:
        result = subprocess.run(command, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        print(f"\n❌ Error: No se encontró el comando '{command[0]}'")
        return False


def verify_installation():
    """Verifica la instalación del sistema."""
    print("\n" + "="*60)
    print("VERIFICANDO INSTALACIÓN...")
    print("="*60 + "\n")
    
    if os.path.exists('verify_installation.py'):
        success = run_command([sys.executable, 'verify_installation.py'])
        if not success:
            print("\n⚠ Algunos componentes no están instalados correctamente.")
    else:
        print("❌ Archivo verify_installation.py no encontrado")


def install_dependencies():
    """Instala las dependencias del proyecto."""
    print("\n" + "="*60)
    print("INSTALANDO DEPENDENCIAS...")
    print("="*60 + "\n")
    
    if not os.path.exists('requirements.txt'):
        print("❌ Archivo requirements.txt no encontrado")
        return
    
    print("Esto puede tomar varios minutos...\n")
    
    # Actualizar pip
    print("Actualizando pip...")
    run_command([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    
    # Instalar dependencias
    print("\nInstalando dependencias...")
    success = run_command([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    
    if success:
        print("\n✅ Dependencias instaladas correctamente")
        
        # Crear carpeta models si no existe
        if not os.path.exists('models'):
            os.makedirs('models')
            print("✅ Carpeta 'models' creada")
    else:
        print("\n❌ Error instalando dependencias")
        print("Intenta manualmente: pip install -r requirements.txt")


def run_demo():
    """Ejecuta el demo de procesamiento de imágenes."""
    print("\n" + "="*60)
    print("EJECUTANDO DEMO DE PROCESAMIENTO...")
    print("="*60 + "\n")
    
    if os.path.exists('demo_procesamiento_flores.py'):
        run_command([sys.executable, 'demo_procesamiento_flores.py'])
    else:
        print("❌ Archivo demo_procesamiento_flores.py no encontrado")


def train_model():
    """Entrena el modelo de clasificación."""
    print("\n" + "="*60)
    print("ENTRENANDO MODELO...")
    print("="*60 + "\n")
    
    if os.path.exists('train_model.py'):
        run_command([sys.executable, 'train_model.py'])
    else:
        print("❌ Archivo train_model.py no encontrado")


def run_simulator():
    """Ejecuta el simulador principal."""
    print("\n" + "="*60)
    print("INICIANDO SIMULADOR...")
    print("="*60 + "\n")
    
    if os.path.exists('main.py'):
        run_command([sys.executable, 'main.py'])
    else:
        print("❌ Archivo main.py no encontrado")


def main():
    """Función principal del script."""
    print_header()
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('config.py'):
        print("❌ Error: Este script debe ejecutarse desde el directorio del proyecto")
        print("   (donde se encuentra config.py)")
        sys.exit(1)
    
    while True:
        print_menu()
        
        try:
            choice = input("Ingresa el número de opción: ").strip()
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            sys.exit(0)
        
        if choice == '1':
            verify_installation()
        elif choice == '2':
            install_dependencies()
        elif choice == '3':
            run_demo()
        elif choice == '4':
            train_model()
        elif choice == '5':
            run_simulator()
        elif choice == '6':
            print("\n👋 ¡Hasta luego!")
            sys.exit(0)
        else:
            print("\n❌ Opción no válida. Por favor ingresa un número del 1 al 6.")
        
        input("\nPresiona Enter para continuar...")
        print("\n" * 2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
        sys.exit(0)
