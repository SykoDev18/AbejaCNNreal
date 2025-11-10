"""
Demo de procesamiento de imágenes de flores.
Muestra las diferentes técnicas de mejora aplicadas.
"""
import os
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from utils import ImageProcessor, Logger
from config import REAL_FLOWERS_DIR


def demo_image_processing(image_path):
    """
    Demuestra todas las técnicas de procesamiento en una imagen.
    
    Args:
        image_path: Ruta a la imagen de flor
    """
    Logger.log(f"Procesando imagen: {image_path}")
    
    # Cargar imagen
    try:
        original_image = Image.open(image_path).convert('RGB')
    except Exception as e:
        Logger.log(f"Error cargando imagen: {e}", "ERROR")
        return
    
    # Aplicar diferentes técnicas
    techniques = {
        'Original': original_image,
        'Ecualización Global': ImageProcessor.equalize_histogram_global(original_image),
        'CLAHE (Adaptativa)': ImageProcessor.equalize_histogram_adaptive(original_image),
        'Contraste Mejorado': ImageProcessor.enhance_contrast(original_image, factor=1.5),
        'Subexpuesta': ImageProcessor.create_underexposed(original_image, factor=0.6),
        'Sobreexpuesta': ImageProcessor.create_overexposed(original_image, factor=1.4),
        'Gaussian Blur': ImageProcessor.apply_gaussian_blur(original_image, kernel_size=5),
        'Median Blur': ImageProcessor.apply_median_blur(original_image, kernel_size=5),
    }
    
    # Calcular métricas para cada técnica
    print("\n" + "="*60)
    print("MÉTRICAS DE CALIDAD DE IMAGEN")
    print("="*60)
    
    for name, img in techniques.items():
        metrics = ImageProcessor.calculate_metrics(img)
        print(f"\n{name}:")
        print(f"  Contraste: {metrics['contrast']:.2f}")
        print(f"  Entropía: {metrics['entropy']:.2f}")
        print(f"  Brillo: {metrics['brightness']:.2f}")
    
    # Visualizar resultados
    fig, axes = plt.subplots(3, 3, figsize=(15, 15))
    fig.suptitle('Técnicas de Procesamiento de Imágenes de Flores', fontsize=16, fontweight='bold')
    
    axes = axes.ravel()
    
    for idx, (name, img) in enumerate(techniques.items()):
        if idx < len(axes):
            axes[idx].imshow(img)
            axes[idx].set_title(name, fontsize=10)
            axes[idx].axis('off')
    
    # Ocultar ejes sobrantes
    for idx in range(len(techniques), len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig('demo_procesamiento_flores.png', dpi=150, bbox_inches='tight')
    Logger.log("Visualización guardada en: demo_procesamiento_flores.png")
    plt.show()


def compare_histogram_equalization(image_path):
    """
    Compara específicamente técnicas de ecualización de histograma.
    
    Args:
        image_path: Ruta a la imagen
    """
    # Cargar imagen
    original = Image.open(image_path).convert('RGB')
    
    # Crear versión subexpuesta para demostrar la efectividad
    underexposed = ImageProcessor.create_underexposed(original, factor=0.5)
    
    # Aplicar ecualizaciones
    eq_global = ImageProcessor.equalize_histogram_global(underexposed)
    eq_adaptive = ImageProcessor.equalize_histogram_adaptive(underexposed)
    
    # Visualizar
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    fig.suptitle('Comparación de Técnicas de Ecualización', fontsize=14, fontweight='bold')
    
    images = [
        (original, 'Original'),
        (underexposed, 'Subexpuesta'),
        (eq_global, 'Ecualización Global'),
        (eq_adaptive, 'CLAHE (Adaptativa)')
    ]
    
    for idx, (img, title) in enumerate(images):
        ax = axes[idx // 2, idx % 2]
        ax.imshow(img)
        ax.set_title(title, fontsize=12)
        ax.axis('off')
        
        # Calcular y mostrar métricas
        metrics = ImageProcessor.calculate_metrics(img)
        text = f"Contraste: {metrics['contrast']:.1f}\n"
        text += f"Entropía: {metrics['entropy']:.1f}\n"
        text += f"Brillo: {metrics['brightness']:.1f}"
        
        ax.text(0.02, 0.98, text, 
                transform=ax.transAxes,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                fontsize=9)
    
    plt.tight_layout()
    plt.savefig('comparacion_ecualizacion.png', dpi=150, bbox_inches='tight')
    Logger.log("Comparación guardada en: comparacion_ecualizacion.png")
    plt.show()


def main():
    """Función principal del demo."""
    print("\n" + "="*60)
    print("DEMO - PROCESAMIENTO DE IMÁGENES DE FLORES")
    print("="*60 + "\n")
    
    # Buscar una imagen de flor
    flower_files = [f for f in os.listdir(REAL_FLOWERS_DIR) 
                   if f.lower().endswith('.png') and 'flor' in f.lower()]
    
    if not flower_files:
        print("Error: No se encontraron imágenes de flores en fotos_flores_proyecto/")
        print("Asegúrate de tener imágenes llamadas 'flor 1.png', 'flor 2.png', etc.")
        return
    
    # Usar la primera imagen encontrada
    test_image = os.path.join(REAL_FLOWERS_DIR, flower_files[0])
    
    print(f"Usando imagen: {test_image}\n")
    print("Este demo mostrará:")
    print("  1. Todas las técnicas de procesamiento aplicadas")
    print("  2. Métricas de calidad para cada técnica")
    print("  3. Comparación específica de ecualizaciones\n")
    
    input("Presiona Enter para continuar...")
    
    # Demo completo
    print("\n[1/2] Demostrando todas las técnicas...")
    demo_image_processing(test_image)
    
    # Comparación de ecualizaciones
    print("\n[2/2] Comparando técnicas de ecualización...")
    compare_histogram_equalization(test_image)
    
    print("\n" + "="*60)
    print("DEMO COMPLETADO")
    print("="*60)
    print("\nSe han generado dos imágenes:")
    print("  - demo_procesamiento_flores.png")
    print("  - comparacion_ecualizacion.png")
    print("\nEstas técnicas se aplican automáticamente durante el")
    print("entrenamiento del modelo para mejorar su robustez.\n")


if __name__ == "__main__":
    main()
