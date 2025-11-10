# 📘 Documentación Técnica - Simulador de Abeja Inteligente

## Índice

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Módulos y Clases](#módulos-y-clases)
3. [Algoritmos Implementados](#algoritmos-implementados)
4. [Modelo de Machine Learning](#modelo-de-machine-learning)
5. [Procesamiento de Imágenes](#procesamiento-de-imágenes)
6. [Flujo de Ejecución](#flujo-de-ejecución)
7. [API y Referencia](#api-y-referencia)

---

## Arquitectura del Sistema

El sistema está diseñado con una arquitectura modular que separa responsabilidades:

```
┌─────────────────────────────────────────────────────────┐
│                    MAIN (main.py)                       │
│                   BeeSimulator Class                    │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ Pygame   │  │ Tkinter  │  │  Logic   │
  │ Renderer │  │   GUI    │  │  Engine  │
  └──────────┘  └──────────┘  └──────────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
        ┌──────────────┼──────────────┬─────────────┐
        │              │              │             │
        ▼              ▼              ▼             ▼
  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │GridWorld │  │PathFinder│  │BeeAgent  │  │Classifier│
  └──────────┘  └──────────┘  └──────────┘  └──────────┘
```

### Componentes Principales

1. **main.py (BeeSimulator)**
   - Orquesta todos los componentes
   - Maneja el loop principal de Pygame
   - Coordina la sincronización entre Pygame y Tkinter

2. **grid_world.py (GridWorld)**
   - Representa el mundo cuadriculado
   - Maneja la generación de obstáculos, flores y objetos
   - Renderiza el mundo en Pygame

3. **search_algorithms.py (PathFinder, BFSSearch, DFSSearch)**
   - Implementa algoritmos de búsqueda
   - Proporciona generadores para animación paso a paso

4. **bee_agent.py (BeeAgent)**
   - Representa la abeja autónoma
   - Gestiona el movimiento y la detección de contenido

5. **flower_classifier.py (FlowerClassifier)**
   - Modelo de clasificación basado en Deep Learning
   - Preprocesamiento y predicción de imágenes

6. **gui_controller.py (ControlPanel, MetricsComparator)**
   - Interfaz gráfica con Tkinter
   - Comparación de métricas entre ejecuciones

---

## Módulos y Clases

### config.py

Configuración global del sistema.

```python
# Variables clave
GRID_SIZE = 20              # Tamaño del grid
CELL_SIZE = 40              # Píxeles por celda
OBSTACLE_PERCENTAGE = 0.15  # % de obstáculos
FLOWER_PERCENTAGE = 0.12    # % de flores
OBJECT_PERCENTAGE = 0.08    # % de objetos
IMAGE_SIZE = 224            # Tamaño para el modelo
```

### utils.py

#### Clase ImageProcessor

Procesamiento avanzado de imágenes.

**Métodos principales:**

- `equalize_histogram_global(image)`: Ecualización global de histograma
- `equalize_histogram_adaptive(image, clip_limit, tile_grid_size)`: CLAHE
- `apply_gaussian_blur(image, kernel_size)`: Filtro Gaussiano
- `apply_median_blur(image, kernel_size)`: Filtro de mediana
- `enhance_contrast(image, factor)`: Mejora de contraste
- `calculate_metrics(image)`: Calcula contraste, entropía y brillo

**Ejemplo de uso:**

```python
from utils import ImageProcessor
from PIL import Image

# Cargar imagen
img = Image.open('flor.png')

# Aplicar ecualización adaptativa
img_enhanced = ImageProcessor.equalize_histogram_adaptive(img)

# Calcular métricas
metrics = ImageProcessor.calculate_metrics(img_enhanced)
print(f"Contraste: {metrics['contrast']}")
```

#### Clase Logger

Sistema de logging con timestamps.

```python
from utils import Logger

Logger.log("Mensaje informativo")
Logger.log("Error crítico", "ERROR")
Logger.log_metrics({"accuracy": 95.5}, "metrics.txt")
```

### grid_world.py

#### Clase GridWorld

**Atributos:**
- `size`: Tamaño del grid (NxN)
- `grid`: Diccionario {(x,y): tipo_celda}
- `bee_pos`: Posición actual de la abeja
- `hive_pos`: Posición de la colmena
- `flowers`: Lista de posiciones de flores
- `objects`: Lista de posiciones de objetos
- `obstacles`: Lista de posiciones de obstáculos

**Métodos principales:**

```python
def initialize_world(self, bee_pos=None, hive_pos=None):
    """Genera el mundo con elementos aleatorios."""

def is_walkable(self, position):
    """Verifica si una posición es transitable."""

def get_neighbors(self, position):
    """Obtiene vecinos transitables de una posición."""

def render(self, screen, path=None, explored=None):
    """Renderiza el mundo en Pygame."""
```

**Tipos de celdas:**
- `CELL_EMPTY = 0`: Celda vacía
- `CELL_OBSTACLE = 1`: Obstáculo
- `CELL_FLOWER = 2`: Flor
- `CELL_OBJECT = 3`: Objeto
- `CELL_BEE = 4`: Abeja
- `CELL_HIVE = 5`: Colmena

### search_algorithms.py

#### Clase BFSSearch

Búsqueda en amplitud (Breadth-First Search).

**Características:**
- Explora nivel por nivel
- Garantiza el camino más corto
- Complejidad: O(V + E)

```python
def search(self, start, goal, mode='exploration'):
    """
    Ejecuta BFS desde start hasta goal.
    
    Args:
        start: Posición inicial (x, y)
        goal: Posición objetivo (x, y)
        mode: 'exploration' o 'optimal'
    
    Returns:
        Tupla (path, explored, steps)
    """
```

#### Clase DFSSearch

Búsqueda en profundidad (Depth-First Search).

**Características:**
- Explora profundamente antes de retroceder
- No garantiza el camino más corto
- Complejidad: O(V + E)

```python
def search(self, start, goal, mode='exploration'):
    """
    Ejecuta DFS desde start hasta goal.
    
    Similar a BFS pero con estrategia de exploración diferente.
    """
```

#### Clase PathFinder

Wrapper unificado para algoritmos de búsqueda.

```python
pathfinder = PathFinder(grid_world)
pathfinder.set_algorithm('BFS')  # o 'DFS'
path, explored, steps = pathfinder.find_path(start, goal, mode='optimal')
```

### bee_agent.py

#### Clase BeeAgent

Representa la abeja autónoma.

**Atributos de estadísticas:**
- `flowers_detected`: Número de flores detectadas correctamente
- `objects_detected`: Número de objetos detectados correctamente
- `cells_visited`: Total de celdas visitadas
- `detection_log`: Log detallado de todas las detecciones

**Métodos principales:**

```python
def move_to(self, position):
    """Mueve la abeja a una posición."""

def detect_cell_content(self):
    """
    Detecta y clasifica el contenido de la celda actual.
    
    Returns:
        Tupla (cell_type, classification, confidence)
    """

def get_statistics(self):
    """
    Retorna estadísticas completas de la ejecución.
    
    Returns:
        Dict con todas las métricas
    """
```

### flower_classifier.py

#### Clase FlowerClassifier

Clasificador basado en Deep Learning.

**Arquitectura del modelo:**
- Base: ResNet50 preentrenado (adaptable a ViT)
- Capa de salida: 2 clases (flor, objeto)
- Función de activación: Softmax para probabilidades

**Pipeline de entrenamiento:**

```python
classifier = FlowerClassifier()

# Entrenar modelo
classifier.train(
    train_dir='fotos_flores_proyecto/flores/train',
    epochs=10,
    batch_size=16
)

# Guardar modelo
classifier.save_model()
```

**Pipeline de predicción:**

```python
# Cargar modelo entrenado
classifier.load_model()

# Predecir
label, confidence = classifier.predict('imagen.jpg')
print(f"Clase: {label}, Confianza: {confidence:.2f}")
```

### gui_controller.py

#### Clase ControlPanel

Interfaz gráfica con Tkinter.

**Componentes:**
- Spinboxes para configurar posiciones
- ComboBoxes para algoritmo y modo
- Botones de control (Iniciar, Recargar)
- Panel de métricas en tiempo real
- Ventanas emergentes para flores detectadas

**Callbacks:**

```python
control_panel = ControlPanel(
    on_start_callback=start_simulation,
    on_reload_callback=reload_world,
    on_position_change_callback=update_positions
)
```

#### Clase MetricsComparator

Compara métricas entre diferentes ejecuciones.

```python
comparator = MetricsComparator()

# Añadir resultado
comparator.add_result('BFS', 'optimal', {
    'path_length': 25,
    'flowers_detected': 5,
    'detection_accuracy': 95.0
})

# Generar reporte
report = comparator.generate_comparison_report()
comparator.save_report('metrics_results.txt')
```

---

## Algoritmos Implementados

### BFS (Breadth-First Search)

**Pseudocódigo:**

```
función BFS(inicio, meta):
    cola = nueva_cola()
    visitados = conjunto_vacío()
    padres = diccionario_vacío()
    
    cola.encolar(inicio)
    visitados.añadir(inicio)
    
    mientras cola no esté vacía:
        actual = cola.desencolar()
        
        si actual == meta:
            retornar reconstruir_camino(padres, inicio, meta)
        
        para cada vecino en obtener_vecinos(actual):
            si vecino no en visitados:
                visitados.añadir(vecino)
                padres[vecino] = actual
                cola.encolar(vecino)
    
    retornar camino_vacío  # No hay solución
```

**Propiedades:**
- **Completo**: Sí, si existe solución la encuentra
- **Óptimo**: Sí, para grafos no ponderados
- **Complejidad temporal**: O(V + E)
- **Complejidad espacial**: O(V)

### DFS (Depth-First Search)

**Pseudocódigo:**

```
función DFS(inicio, meta):
    pila = nueva_pila()
    visitados = conjunto_vacío()
    padres = diccionario_vacío()
    
    pila.apilar(inicio)
    
    mientras pila no esté vacía:
        actual = pila.desapilar()
        
        si actual en visitados:
            continuar
        
        visitados.añadir(actual)
        
        si actual == meta:
            retornar reconstruir_camino(padres, inicio, meta)
        
        para cada vecino en obtener_vecinos(actual):
            si vecino no en visitados:
                padres[vecino] = actual
                pila.apilar(vecino)
    
    retornar camino_vacío
```

**Propiedades:**
- **Completo**: Sí, en grafos finitos
- **Óptimo**: No, no garantiza el camino más corto
- **Complejidad temporal**: O(V + E)
- **Complejidad espacial**: O(V)

---

## Modelo de Machine Learning

### Arquitectura

```
Input (224x224x3)
    ↓
ResNet50 Backbone (Preentrenado en ImageNet)
    ↓
Global Average Pooling
    ↓
Fully Connected (2048 → 2)
    ↓
Softmax
    ↓
Output [P(flor), P(objeto)]
```

### Entrenamiento

**Hiperparámetros:**
- Learning rate: 1e-4
- Optimizer: Adam
- Loss function: CrossEntropyLoss
- Batch size: 16
- Epochs: 10

**Data Augmentation:**
- Ecualización global de histograma
- CLAHE (Ecualización adaptativa)
- Ajuste de brillo (subexpuesta/sobreexpuesta)
- Mejora de contraste
- Redimensionamiento con LANCZOS

**Normalización:**
```python
mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]
```

### Evaluación

**Métricas:**
- Accuracy: (TP + TN) / Total
- Confidence: Probabilidad de la clase predicha
- Confusion Matrix: Para análisis detallado

---

## Procesamiento de Imágenes

### Técnicas Implementadas

#### 1. Ecualización Global de Histograma

```python
# Mejora el contraste global
img_eq = cv2.equalizeHist(img_gray)
```

**Cuándo usar**: Imágenes con bajo contraste general

#### 2. CLAHE (Contrast Limited Adaptive Histogram Equalization)

```python
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
img_clahe = clahe.apply(img_gray)
```

**Cuándo usar**: Imágenes subexpuestas o con contraste local pobre

#### 3. Filtros de Suavizado

**Gaussiano**: Reduce ruido gaussiano
```python
img_blur = cv2.GaussianBlur(img, (5,5), 0)
```

**Mediana**: Elimina ruido de sal y pimienta
```python
img_median = cv2.medianBlur(img, 5)
```

**Promedio**: Suavizado general
```python
img_avg = cv2.blur(img, (5,5))
```

#### 4. Mejora de Contraste y Brillo

```python
enhancer = ImageEnhance.Contrast(img)
img_contrast = enhancer.enhance(1.5)  # Factor > 1 aumenta
```

### Métricas de Calidad

**Contraste (Desviación Estándar)**
```python
contrast = np.std(img_gray)
```

**Entropía (Información)**
```python
histogram = cv2.calcHist([img_gray], [0], None, [256], [0,256])
prob = histogram / histogram.sum()
entropy = -np.sum(prob * np.log2(prob + 1e-7))
```

**Brillo Promedio**
```python
brightness = np.mean(img_gray)
```

---

## Flujo de Ejecución

### Diagrama de Flujo Principal

```
INICIO
  ↓
Inicializar Pygame
  ↓
Crear GridWorld
  ↓
Cargar FlowerClassifier
  ↓
Crear BeeAgent
  ↓
Inicializar PathFinder
  ↓
Crear ControlPanel (Tkinter) en hilo separado
  ↓
╔═══════════════════════════╗
║   LOOP PRINCIPAL          ║
║                           ║
║  1. Procesar eventos      ║
║  2. Actualizar Tkinter    ║
║  3. Renderizar Pygame     ║
║  4. Tick del reloj        ║
╚═══════════════════════════╝
  ↑                          │
  └──────── while running ───┘
  ↓
Guardar métricas
  ↓
Cleanup
  ↓
FIN
```

### Secuencia de Simulación

```
Usuario presiona "Iniciar Simulación"
  ↓
Callback: start_simulation(config)
  ↓
PathFinder.find_path(start, goal, mode)
  ↓
BFS/DFS busca el camino
  ↓
Retorna: (path, explored, steps)
  ↓
Iniciar animación en hilo separado
  ↓
Para cada posición en path:
  │
  ├─ BeeAgent.move_to(position)
  │
  ├─ BeeAgent.detect_cell_content()
  │   │
  │   ├─ FlowerClassifier.predict(cell_image)
  │   │
  │   └─ Actualizar estadísticas
  │
  ├─ Mostrar detalle si es flor
  │
  └─ Actualizar panel de métricas
  ↓
Simulación completada
  ↓
Mostrar estadísticas finales
  ↓
Guardar en MetricsComparator
```

---

## API y Referencia

### Funciones Principales

#### main.py

```python
class BeeSimulator:
    def __init__(self)
    def initialize(self)
    def reload_world(self)
    def start_simulation(self, config: dict)
    def handle_events(self)
    def render(self)
    def run(self)
```

#### grid_world.py

```python
class GridWorld:
    def __init__(self, size: int)
    def initialize_world(self, bee_pos: tuple, hive_pos: tuple)
    def is_walkable(self, position: tuple) -> bool
    def get_cell_type(self, position: tuple) -> int
    def get_neighbors(self, position: tuple) -> list
    def render(self, screen, path: list, explored: set)
```

#### search_algorithms.py

```python
class PathFinder:
    def set_algorithm(self, algorithm_type: str)
    def find_path(self, start: tuple, goal: tuple, mode: str) -> tuple
```

#### flower_classifier.py

```python
class FlowerClassifier:
    def train(self, train_dir: str, epochs: int, batch_size: int)
    def load_model(self) -> bool
    def save_model(self)
    def predict(self, image) -> tuple  # (label, confidence)
    def evaluate(self, test_dir: str) -> dict
```

#### bee_agent.py

```python
class BeeAgent:
    def move_to(self, position: tuple) -> bool
    def detect_cell_content(self) -> tuple  # (cell_type, classification, confidence)
    def get_statistics(self) -> dict
    def reset_statistics(self)
```

---

## Ejemplos de Uso

### Ejemplo 1: Ejecutar Simulación Básica

```python
from main import BeeSimulator

simulator = BeeSimulator()
simulator.run()
```

### Ejemplo 2: Usar PathFinder Manualmente

```python
from grid_world import GridWorld
from search_algorithms import PathFinder

# Crear mundo
world = GridWorld(20)
world.initialize_world()

# Crear pathfinder
pathfinder = PathFinder(world)
pathfinder.set_algorithm('BFS')

# Buscar camino
path, explored, steps = pathfinder.find_path(
    start=(0, 0),
    goal=(19, 19),
    mode='optimal'
)

print(f"Camino encontrado: {len(path)} pasos")
```

### Ejemplo 3: Entrenar Modelo Personalizado

```python
from flower_classifier import FlowerClassifier

classifier = FlowerClassifier()

# Entrenar con configuración personalizada
classifier.train(
    train_dir='mi_dataset/train',
    epochs=20,
    batch_size=32
)

# Evaluar
metrics = classifier.evaluate('mi_dataset/test')
print(f"Accuracy: {metrics['accuracy']:.2f}%")
```

### Ejemplo 4: Procesar Imágenes

```python
from utils import ImageProcessor
from PIL import Image

img = Image.open('flor.jpg')

# Aplicar pipeline completo
processed_images = ImageProcessor.preprocess_for_model(
    img, 
    apply_augmentation=True
)

# Calcular métricas para cada versión
for i, processed_img in enumerate(processed_images):
    metrics = ImageProcessor.calculate_metrics(processed_img)
    print(f"Imagen {i}: Contraste={metrics['contrast']:.2f}")
```

---

## Conclusión

Este documento proporciona una referencia técnica completa del simulador. Para más información sobre uso y configuración, consulta el [README.md](README.md).

**Versión**: 1.0  
**Fecha**: Octubre 2025  
**Autor**: Sistema de IA Avanzado
