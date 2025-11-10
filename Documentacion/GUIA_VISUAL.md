# 🎮 Guía Visual de Uso - Simulador de Abeja Inteligente

## 🚀 Inicio Rápido

### Paso 1: Instalación

```powershell
# Opción 1: Script automático (Recomendado)
.\install.ps1

# Opción 2: Manual
pip install -r requirements.txt
```

### Paso 2: Verificar Instalación

```powershell
python verify_installation.py
```

Deberías ver:
```
✓ SISTEMA LISTO PARA USAR
```

### Paso 3: Entrenar Modelo (Opcional)

```powershell
python train_model.py
```

**Nota**: Este paso puede tomar 10-30 minutos dependiendo de tu hardware.

### Paso 4: Ejecutar Simulador

```powershell
python main.py
```

---

## 🖥️ Interfaz del Simulador

### Ventana Principal (Pygame)

```
┌────────────────────────────────────────────────┐
│ Algoritmo: BFS - optimal    Pos: (5, 7)       │
│ Flores: 3 | Objetos: 1                        │
├────────────────────────────────────────────────┤
│                                                │
│  🐝 ← Abeja                                    │
│  🏠 ← Colmena                                  │
│  🌳 ← Obstáculo                                │
│  🌸 ← Flor                                     │
│  📦 ← Objeto                                   │
│                                                │
│  [Grid 20x20 con elementos visuales]          │
│                                                │
│  Colores:                                      │
│  - Azul claro: Camino a seguir                │
│  - Rosa claro: Nodos explorados               │
│                                                │
└────────────────────────────────────────────────┘
```

**Controles de Teclado:**
- `ESC`: Salir
- `R`: Recargar mundo
- `SPACE`: Iniciar/pausar simulación

### Panel de Control (Tkinter)

```
┌──────────────────────────────────────┐
│ 🐝 Control de Simulación             │
├──────────────────────────────────────┤
│                                      │
│ 📍 Configuración de Posiciones       │
│ ┌──────────────────────────────────┐ │
│ │ Posición Abeja (X, Y):           │ │
│ │ [↑↓ 0] [↑↓ 0]                    │ │
│ │                                  │ │
│ │ Posición Colmena (X, Y):         │ │
│ │ [↑↓ 19] [↑↓ 19]                  │ │
│ └──────────────────────────────────┘ │
│                                      │
│ 🔍 Configuración de Búsqueda         │
│ ┌──────────────────────────────────┐ │
│ │ Algoritmo: [BFS ▼]               │ │
│ │ Modo:      [exploration ▼]       │ │
│ └──────────────────────────────────┘ │
│                                      │
│ [▶ Iniciar] [🔄 Recargar]           │
│                                      │
│ 📊 Métricas en Tiempo Real           │
│ ┌──────────────────────────────────┐ │
│ │ Sistema inicializado.            │ │
│ │ Presiona 'Iniciar Simulación'    │ │
│ │ para comenzar.                   │ │
│ │                                  │ │
│ │ [Aquí aparecen las métricas]     │ │
│ └──────────────────────────────────┘ │
└──────────────────────────────────────┘
```

---

## 📊 Flujo de Trabajo Típico

### Escenario 1: Primera Ejecución

```
1. Abrir terminal
   │
2. python main.py
   │
3. Se abren dos ventanas:
   ├─ Pygame: Mundo cuadriculado
   └─ Tkinter: Panel de control
   │
4. En Panel de Control:
   ├─ Configurar posición abeja: (0, 0)
   ├─ Configurar posición colmena: (19, 19)
   ├─ Seleccionar algoritmo: BFS
   └─ Seleccionar modo: exploration
   │
5. Presionar [▶ Iniciar Simulación]
   │
6. Observar:
   ├─ Abeja se mueve automáticamente
   ├─ Nodos explorados se iluminan
   ├─ Camino se traza
   └─ Métricas se actualizan
   │
7. Si se detecta flor:
   └─ Aparece ventana emergente con foto HD
   │
8. Al llegar a colmena:
   └─ Se muestran estadísticas finales
```

### Escenario 2: Comparación de Algoritmos

```
Iteración 1: BFS Exploration
├─ Configurar BFS + exploration
├─ Iniciar simulación
└─ Observar métricas

Iteración 2: BFS Optimal
├─ Configurar BFS + optimal
├─ Iniciar simulación
└─ Observar métricas

Iteración 3: DFS Exploration
├─ Configurar DFS + exploration
├─ Iniciar simulación
└─ Observar métricas

Iteración 4: DFS Optimal
├─ Configurar DFS + optimal
├─ Iniciar simulación
└─ Observar métricas

Resultado:
└─ metrics_results.txt con comparación completa
```

---

## 🌸 Detección de Flores

### Proceso Visual

```
Abeja se mueve a celda
         │
         ▼
¿Es flor u objeto?
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  Flor     Objeto
    │         │
    │         └─→ Incrementar contador objetos
    │
    ├─→ Clasificador analiza
    │
    ├─→ Confianza > 0.8?
    │       │
    │   ┌───┴───┐
    │   │       │
    │   ▼       ▼
    │  Sí      No
    │   │       │
    │   │       └─→ Log detección dudosa
    │   │
    │   └─→ Mostrar ventana emergente
    │        │
    │        ├─ Foto HD de flor real
    │        ├─ Métricas de procesamiento
    │        └─ Botón [Cerrar]
    │
    └─→ Incrementar contador flores
```

### Ventana Emergente de Flor

```
┌────────────────────────────────────┐
│  🌸 ¡Flor Detectada!               │
├────────────────────────────────────┤
│                                    │
│   [Imagen HD de flor 350x350px]   │
│                                    │
├────────────────────────────────────┤
│  La abeja ha detectado una flor!  │
│                                    │
│  Procesamiento de imagen aplicado: │
│  - Ecualización de histograma      │
│  - Mejora de contraste             │
│  - Clasificación con Transformer   │
│                                    │
│         [Cerrar]                   │
└────────────────────────────────────┘
```

---

## 📈 Interpretación de Métricas

### Durante la Simulación

```
🚀 INICIANDO SIMULACIÓN
========================================
Algoritmo: BFS
Modo: exploration
Inicio: (0, 0)
Meta: (19, 19)
========================================

Buscando camino...

✓ Camino encontrado!
  Longitud del camino: 38 pasos
  Nodos explorados: 156
  Tiempo de búsqueda: 0.023s

Iniciando movimiento de la abeja...

Paso 1/38
Posición: (0, 1)
Detección: N/A
Confianza: 0.00

Paso 5/38
Posición: (2, 3)
Detección: flor
Confianza: 0.92

[... continúa ...]
```

### Al Finalizar

```
🏁 SIMULACIÓN COMPLETADA
========================================

📊 ESTADÍSTICAS FINALES:
  Algoritmo: BFS
  Modo: exploration
  Longitud del camino: 38 pasos
  Nodos explorados: 156
  Celdas visitadas: 38
  Flores detectadas: 5
  Objetos detectados: 2
  Precisión de detección: 87.50%

✓ La abeja ha llegado a la colmena!
```

---

## 🔧 Configuraciones Comunes

### Configuración 1: Mundo Pequeño y Rápido

```python
# En config.py
GRID_SIZE = 10
SEARCH_DELAY = 0.1
OBSTACLE_PERCENTAGE = 0.10
```

**Uso**: Pruebas rápidas, demos

### Configuración 2: Mundo Grande y Complejo

```python
# En config.py
GRID_SIZE = 30
SEARCH_DELAY = 0.5
OBSTACLE_PERCENTAGE = 0.20
FLOWER_PERCENTAGE = 0.15
```

**Uso**: Análisis detallado, comparaciones exhaustivas

### Configuración 3: Entrenamiento Rápido

```python
# En config.py
EPOCHS = 5
BATCH_SIZE = 32
```

**Uso**: Pruebas del modelo, desarrollo

### Configuración 4: Entrenamiento Completo

```python
# En config.py
EPOCHS = 20
BATCH_SIZE = 16
LEARNING_RATE = 5e-5
```

**Uso**: Producción, máxima precisión

---

## 🐛 Solución de Problemas Comunes

### Problema 1: Ventana Negra en Pygame

**Síntoma**: La ventana de Pygame aparece pero está completamente negra.

**Solución**:
```powershell
# Verificar sprites
ls assets\

# Deberías ver:
# abeja.png, colmena.png, arbol.png, flor.png

# Si faltan, añádelos manualmente
```

### Problema 2: Panel de Control No Aparece

**Síntoma**: Solo se abre Pygame, no Tkinter.

**Solución** (Windows):
```powershell
# Tkinter viene con Python en Windows
# Si no funciona, reinstalar Python con opción tcl/tk
```

**Solución** (Linux):
```bash
sudo apt-get install python3-tk
```

### Problema 3: Modelo No Entrena

**Síntoma**: Error durante `python train_model.py`

**Diagnóstico**:
```powershell
python verify_installation.py
```

**Soluciones comunes**:
```powershell
# Si falta PyTorch
pip install torch torchvision

# Si error de CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Si falta dataset
# Verificar que existe fotos_flores_proyecto/flores/train/
```

### Problema 4: Simulación Muy Lenta

**Causa**: Grid muy grande o hardware limitado

**Soluciones**:
```python
# En config.py, reducir:
GRID_SIZE = 15  # En vez de 20
SEARCH_DELAY = 0.1  # En vez de 0.3
```

### Problema 5: No Se Encuentran Flores

**Causa**: Poca densidad de flores o mala suerte en generación aleatoria

**Solución**:
```python
# En config.py, aumentar:
FLOWER_PERCENTAGE = 0.20  # En vez de 0.12
```

O simplemente presionar `R` o [🔄 Recargar] para regenerar el mundo.

---

## 💡 Tips y Trucos

### Tip 1: Visualización Óptima

Para ver mejor la exploración:
- Usa modo `exploration` en vez de `optimal`
- Aumenta `SEARCH_DELAY` a 0.5 segundos
- Usa un `GRID_SIZE` moderado (15-20)

### Tip 2: Análisis Comparativo

Para un buen análisis:
1. Ejecuta cada combinación (BFS/DFS × exploration/optimal)
2. Usa la misma configuración de mundo
3. Revisa `metrics_results.txt` al final

### Tip 3: Mejor Precisión del Modelo

Para mejorar la detección:
1. Entrena por más épocas (20+)
2. Aumenta el dataset con más imágenes
3. Ajusta `LEARNING_RATE` más bajo (5e-5)

### Tip 4: Debugging

Para ver más información:
```python
# En utils.py, Logger.log() imprime en consola
# Puedes añadir más logs donde necesites
from utils import Logger
Logger.log("Mi mensaje de debug", "DEBUG")
```

### Tip 5: Captura de Pantalla

Durante la simulación:
- Windows: `Win + Shift + S`
- O usar software de captura

---

## 📹 Secuencia de Comandos Completa

```powershell
# 1. Clonar/Descargar proyecto
cd Abeja

# 2. Verificar Python
python --version
# Debe ser 3.8+

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar instalación
python verify_installation.py

# 5. (Opcional) Ver demo de procesamiento
python demo_procesamiento_flores.py

# 6. (Recomendado) Entrenar modelo
python train_model.py

# 7. Ejecutar simulador
python main.py

# 8. En el panel de control:
#    - Configurar posiciones
#    - Seleccionar algoritmo
#    - Presionar "Iniciar Simulación"

# 9. Repetir con diferentes configuraciones

# 10. Ver resultados comparativos
cat metrics_results.txt
```

---

## 🎯 Casos de Uso Educativos

### Caso 1: Aprender BFS vs DFS

1. Ejecutar BFS exploration
2. Observar cómo explora nivel por nivel
3. Ejecutar DFS exploration
4. Observar cómo explora en profundidad
5. Comparar longitud de caminos

### Caso 2: Estudio de Visión por Computadora

1. Ejecutar `demo_procesamiento_flores.py`
2. Analizar las diferentes técnicas
3. Ver cómo afectan las métricas
4. Experimentar con el modelo

### Caso 3: Análisis de Algoritmos

1. Configurar mundo complejo (muchos obstáculos)
2. Ejecutar ambos algoritmos
3. Registrar tiempo, pasos, eficiencia
4. Presentar comparación

---

## 📚 Recursos Adicionales

- **README.md**: Información general del proyecto
- **DOCUMENTACION_TECNICA.md**: Referencia técnica completa
- **config.py**: Todas las configuraciones disponibles
- **requirements.txt**: Lista de dependencias

---

## ✨ ¡Disfruta Explorando!

¿Preguntas o problemas? Revisa la documentación técnica o los comentarios en el código fuente.

**¡Happy Coding!** 🐝🌸
