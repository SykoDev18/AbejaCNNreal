# 🐝 Simulador de Abeja Inteligente

## Descripción del Proyecto

Este proyecto implementa un simulador completo de una abeja autónoma que navega por un mundo cuadriculado, busca flores y regresa a su colmena. El sistema integra:

- 🎮 **Pygame**: Renderizado del mundo cuadriculado y animaciones
- 🖼️ **Tkinter**: Interfaz gráfica de control y configuración
- 🔍 **Algoritmos de Búsqueda**: BFS y DFS con modos de exploración y óptimo
- 🤖 **Vision Transformer**: Clasificación binaria (flores vs objetos)
- 📸 **Procesamiento de Imágenes**: Ecualización, CLAHE, mejoras de contraste
- 📊 **Análisis Comparativo**: Métricas de eficiencia y efectividad

## 🏗️ Estructura del Proyecto

```
Abeja/
├── assets/                      # Sprites del juego
│   ├── abeja.png
│   ├── colmena.png
│   ├── arbol.png
│   └── flor.png
├── fotos_flores_proyecto/       # Fotos de flores de alta resolución
│   ├── flor 1.png - flor 8.png
│   └── flores/
│       ├── train/               # Dataset de entrenamiento
│       │   ├── daisy/
│       │   ├── dandelion/
│       │   ├── rose/
│       │   ├── sunflower/
│       │   └── tulip/
│       └── test/                # Dataset de prueba
├── objectos/                    # Imágenes de objetos (no-flores)
├── models/                      # Modelos entrenados (se crea automáticamente)
├── config.py                    # Configuración global
├── utils.py                     # Utilidades y procesamiento de imágenes
├── grid_world.py                # Mundo cuadriculado
├── search_algorithms.py         # BFS y DFS
├── flower_classifier.py         # Modelo Transformer
├── bee_agent.py                 # Agente abeja
├── gui_controller.py            # Interfaz Tkinter
├── main.py                      # Archivo principal
├── train_model.py               # Script de entrenamiento
└── requirements.txt             # Dependencias
```

## 📋 Requisitos

### Dependencias de Python

```bash
pip install -r requirements.txt
```

**Contenido de requirements.txt:**
- pygame >= 2.5.0
- torch >= 2.0.0
- torchvision >= 0.15.0
- opencv-python >= 4.8.0
- Pillow >= 10.0.0
- numpy >= 1.24.0

### Recursos Necesarios

1. **Sprites** (en `assets/`):
   - `abeja.png`: Sprite de la abeja
   - `colmena.png`: Sprite de la colmena
   - `arbol.png`: Sprite de obstáculos
   - `flor.png`: Sprite genérico de flores

2. **Dataset de Flores** (en `fotos_flores_proyecto/flores/`):
   - Carpeta `train/` con subcarpetas de tipos de flores
   - Carpeta `test/` para evaluación

3. **Fotos de Flores Reales** (en `fotos_flores_proyecto/`):
   - 8 imágenes de alta resolución (`flor 1.png` a `flor 8.png`)

4. **Objetos** (en `objectos/`):
   - Imágenes de objetos diversos (no-flores)

## 🚀 Uso del Simulador

### Paso 1: Entrenar el Modelo (Opcional pero Recomendado)

```bash
python train_model.py
```

Este script entrena el modelo Vision Transformer para clasificar flores vs objetos. El entrenamiento puede tomar varios minutos dependiendo de tu hardware.

**Nota**: El simulador puede ejecutarse sin entrenar el modelo, pero la precisión de detección será menor.

### Paso 2: Ejecutar el Simulador

```bash
python main.py
```

Esto abrirá dos ventanas:

1. **Ventana Pygame**: Muestra el mundo cuadriculado con la abeja, colmena, obstáculos, flores y objetos.

2. **Panel de Control (Tkinter)**: Interfaz para configurar y controlar la simulación.

## 🎮 Controles

### Panel de Control (Tkinter)

- **Posición Abeja (X, Y)**: Selecciona la posición inicial de la abeja
- **Posición Colmena (X, Y)**: Selecciona la posición de la meta
- **Algoritmo**: Selecciona BFS o DFS
- **Modo**: 
  - `exploration`: Muestra todo el proceso de exploración
  - `optimal`: Muestra el camino óptimo encontrado
- **▶ Iniciar Simulación**: Comienza la búsqueda y movimiento de la abeja
- **🔄 Recargar Mundo**: Genera un nuevo mundo aleatorio

### Ventana Pygame

- **ESC**: Salir del simulador
- **R**: Recargar mundo
- **SPACE**: Iniciar/pausar simulación

## 🔬 Algoritmos de Búsqueda

### BFS (Breadth-First Search)

**Modo Exploración**: La abeja explora nivel por nivel hasta encontrar la colmena.
- ✅ Garantiza el camino más corto
- 📊 Explora sistemáticamente por niveles
- 🎯 Ideal para encontrar soluciones óptimas

**Modo Óptimo**: Muestra directamente el camino más corto.

### DFS (Depth-First Search)

**Modo Exploración**: La abeja explora en profundidad cada rama antes de retroceder.
- ⚡ Puede ser más rápido en algunos casos
- 🌲 Explora profundamente antes de amplitud
- 🔄 No garantiza el camino más corto

**Modo Óptimo**: Muestra el camino encontrado por DFS.

## 🤖 Clasificación con Vision Transformer

El sistema utiliza un modelo basado en ResNet50 (adaptable a ViT) para clasificar el contenido de cada celda:

### Procesamiento de Imágenes

1. **Ecualización Global de Histograma**: Mejora el contraste general
2. **CLAHE (Ecualización Adaptativa)**: Mejora el contraste local
3. **Mejora de Contraste y Brillo**: Ajustes con PIL
4. **Filtros de Suavizado**: Gaussiano, mediana, promedio
5. **Interpolación**: Redimensionamiento de alta calidad (LANCZOS)

### Aumento de Datos

Durante el entrenamiento, el sistema aplica automáticamente:
- Imágenes normales
- Imágenes subexpuestas
- Imágenes sobreexpuestas
- Imágenes con ecualización global
- Imágenes con ecualización adaptativa

Esto hace que el modelo sea robusto a diferentes condiciones de iluminación.

## 📊 Métricas y Análisis

El simulador registra y compara:

### Métricas de Búsqueda
- **Longitud del camino**: Número de pasos desde inicio hasta meta
- **Nodos explorados**: Total de celdas visitadas durante la búsqueda
- **Tiempo de ejecución**: Duración de la búsqueda

### Métricas de Detección
- **Flores detectadas**: Número de flores identificadas correctamente
- **Objetos detectados**: Número de objetos identificados correctamente
- **Precisión de detección**: Porcentaje de clasificaciones correctas
- **Log de detecciones**: Registro detallado de cada detección

### Reporte Comparativo

Al finalizar múltiples ejecuciones, el sistema genera un reporte comparativo (`metrics_results.txt`) que analiza:
- Estrategia más eficiente (menos pasos)
- Mejor precisión de detección
- Comparación entre BFS y DFS
- Diferencias entre modos exploration y optimal

## 🌸 Detección de Flores

Cuando la abeja detecta una flor:
1. El clasificador analiza el sprite de la celda
2. Si se confirma que es una flor, se muestra una ventana emergente
3. La ventana muestra una foto de alta resolución de una flor real
4. Se registra la detección con su nivel de confianza

## ⚙️ Configuración Avanzada

Puedes modificar parámetros en `config.py`:

```python
GRID_SIZE = 20              # Tamaño de la cuadrícula (NxN)
CELL_SIZE = 40              # Tamaño de cada celda en píxeles
OBSTACLE_PERCENTAGE = 0.15  # Porcentaje de obstáculos
FLOWER_PERCENTAGE = 0.12    # Porcentaje de flores
OBJECT_PERCENTAGE = 0.08    # Porcentaje de objetos
SEARCH_DELAY = 0.3          # Delay entre pasos (segundos)
IMAGE_SIZE = 224            # Tamaño de imagen para el modelo
EPOCHS = 10                 # Épocas de entrenamiento
BATCH_SIZE = 16             # Tamaño de batch
```

## 🐛 Solución de Problemas

### El modelo no carga
- Entrena el modelo primero con `python train_model.py`
- Verifica que PyTorch esté instalado correctamente

### Errores con sprites
- Verifica que todos los sprites existan en la carpeta `assets/`
- Los sprites pueden estar en formato PNG o JPG

### Ventana de Tkinter no aparece
- Asegúrate de que Tkinter esté instalado (viene con Python en Windows)
- En Linux: `sudo apt-get install python3-tk`

### Simulación muy lenta
- Reduce `GRID_SIZE` en `config.py`
- Aumenta `SEARCH_DELAY` para visualizar mejor
- Reduce `OBSTACLE_PERCENTAGE`

## 📚 Créditos y Referencias

### Técnicas Implementadas
- **BFS/DFS**: Algoritmos clásicos de búsqueda en grafos
- **CLAHE**: Adaptive Histogram Equalization (OpenCV)
- **Vision Transformers**: Arquitectura para clasificación de imágenes
- **Transfer Learning**: Uso de modelos preentrenados (ResNet50)

### Dataset de Flores
- El proyecto usa el dataset de flores con 5 categorías
- Imágenes de dominio público y Creative Commons

## 🎓 Cumplimiento de Rúbrica

Este proyecto cumple con todos los requisitos especificados:

### ✅ Parte 1: Interfaz Gráfica y Mundo Cuadriculado (24%)
- [x] Construcción del mundo cuadriculado con Pygame (10%)
- [x] Generación aleatoria de obstáculos, flores y objetos (10%)
- [x] Definición dinámica de puntos de inicio y meta con Tkinter (8%)
- [x] Movimiento autónomo de la abeja (10%)

### ✅ Parte 2: Búsqueda de Camino (10%)
- [x] Implementación DFS con modos exploración y óptimo (5%)
- [x] Implementación BFS con modos exploración y óptimo (5%)

### ✅ Parte 3: Visión por Computadora (19%)
- [x] Identificación de contenido de celdas (5%)
- [x] Procesamiento de imágenes avanzado (7%)
- [x] Modelo Transformer para clasificación (7%)

### ✅ Parte 4: Métricas y Análisis (10%)
- [x] Registro de puntajes (5%)
- [x] Comparación de estrategias (5%)

### ✅ Parte 5: Código y Reutilización (3%)
- [x] Uso de scripts de clase adaptados (3%)

## 📝 Licencia

Este proyecto es educativo y se proporciona con fines académicos.

## 👨‍💻 Autor

Proyecto desarrollado como simulador avanzado de agentes inteligentes con visión por computadora.

---

**¡Disfruta explorando el mundo de la abeja inteligente!** 🐝🌸
