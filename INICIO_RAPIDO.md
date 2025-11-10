# ⚡ INICIO RÁPIDO - 5 MINUTOS

## Opción 1: Automático (Recomendado) 🚀

### Windows (PowerShell)
```powershell
# 1. Navegar al directorio del proyecto
cd Abeja

# 2. Ejecutar script de inicio
python start.py
```

### Linux/macOS
```bash
# 1. Navegar al directorio del proyecto
cd Abeja

# 2. Ejecutar script de inicio
python3 start.py
```

Luego selecciona:
- **Opción 2**: Instalar dependencias
- **Opción 4**: Entrenar modelo (opcional, 10-30 min)
- **Opción 5**: Ejecutar simulador

---

## Opción 2: Manual 🛠️

### Paso 1: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Verificar instalación
```bash
python verify_installation.py
```

Deberías ver: `✓ SISTEMA LISTO PARA USAR`

### Paso 3: Ejecutar simulador
```bash
python main.py
```

---

## ¿Qué esperar? 👀

Al ejecutar `python main.py`:

1. **Se abrirán DOS ventanas:**
   - 🎮 Ventana Pygame: Mundo cuadriculado con la abeja
   - 🖼️ Ventana Tkinter: Panel de control

2. **En el panel de control:**
   - Configura posición de abeja (default: 0, 0)
   - Configura posición de colmena (default: 19, 19)
   - Selecciona algoritmo: BFS o DFS
   - Selecciona modo: exploration u optimal
   - Presiona **[▶ Iniciar Simulación]**

3. **Observa:**
   - La abeja se mueve automáticamente
   - Los nodos explorados se iluminan
   - Aparecen ventanas emergentes cuando detecta flores
   - Las métricas se actualizan en tiempo real

---

## Atajos de Teclado ⌨️

En la ventana de Pygame:
- `ESC`: Salir
- `R`: Recargar mundo (genera nuevo mapa aleatorio)
- `SPACE`: Iniciar/pausar simulación

---

## Problemas Comunes 🔧

### "Import error: No module named pygame"
```bash
pip install pygame
```

### "Import error: No module named torch"
```bash
# CPU only (recomendado para empezar)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### "No se encuentra el archivo config.py"
Asegúrate de estar en el directorio correcto:
```bash
cd Abeja
ls  # Deberías ver: main.py, config.py, etc.
```

### Ventana de Tkinter no aparece (Linux)
```bash
sudo apt-get install python3-tk
```

---

## Primera Simulación Sugerida 🎯

Para tu primera ejecución, te sugerimos:

1. **Configuración simple:**
   - Abeja: (0, 0) - esquina superior izquierda
   - Colmena: (19, 19) - esquina inferior derecha
   - Algoritmo: **BFS**
   - Modo: **exploration**

2. **Observa cómo:**
   - BFS explora nivel por nivel
   - Encuentra el camino más corto
   - La abeja detecta flores en su recorrido

3. **Luego prueba:**
   - Cambiar a **DFS** para comparar
   - Usar modo **optimal** para ver solo el camino final
   - Presionar **[🔄 Recargar]** para generar un mundo diferente

---

## Entrenar el Modelo (Opcional pero Recomendado) 🤖

El simulador funciona sin entrenar el modelo, pero tendrás mejor precisión si lo entrenas:

```bash
python train_model.py
```

**Tiempo estimado:** 10-30 minutos (dependiendo del hardware)

**Nota:** El modelo se guarda en `models/flower_classifier.pth`

---

## Comandos Útiles 📝

```bash
# Ver ayuda del script de inicio
python start.py

# Verificar que todo esté instalado
python verify_installation.py

# Ver demo de procesamiento de imágenes
python demo_procesamiento_flores.py

# Entrenar modelo
python train_model.py

# Ejecutar simulador
python main.py
```

---

## Estructura Mínima Requerida 📁

Para que el simulador funcione, necesitas:

```
Abeja/
├── *.py (todos los archivos Python)
├── config.py ⚠️ REQUERIDO
├── main.py ⚠️ REQUERIDO
├── assets/
│   ├── abeja.png ⚠️ REQUERIDO
│   ├── colmena.png ⚠️ REQUERIDO
│   ├── arbol.png ⚠️ REQUERIDO
│   └── flor.png ⚠️ REQUERIDO
├── fotos_flores_proyecto/ (para fotos HD)
└── objectos/ (para sprites de objetos)
```

---

## ¿Necesitas Ayuda? 🆘

1. **Lee la documentación:**
   - `README.md` - Guía completa
   - `Documentacion/GUIA_VISUAL.md` - Guía visual paso a paso
   - `Documentacion/DOCUMENTACION_TECNICA.md` - Referencia técnica

2. **Verifica tu instalación:**
   ```bash
   python verify_installation.py
   ```

3. **Revisa los errores:**
   - Los mensajes de error suelen ser descriptivos
   - Busca logs en la consola

---

## Después de la Primera Ejecución 🎓

Una vez que funcione, prueba:

1. **Comparar algoritmos:**
   - Ejecuta BFS y DFS con el mismo mundo
   - Compara métricas en `metrics_results.txt`

2. **Experimentar con configuraciones:**
   - Edita `config.py`
   - Cambia `GRID_SIZE`, `SEARCH_DELAY`, etc.

3. **Analizar el código:**
   - El código está bien documentado
   - Lee los comentarios para entender la lógica

---

## 🎉 ¡Listo!

Ahora tienes todo lo necesario para ejecutar el simulador.

**Comando más rápido para empezar:**
```bash
python main.py
```

**¡Disfruta explorando el mundo de la abeja inteligente!** 🐝🌸
