"""
Interfaz gráfica con Tkinter para control del simulador.
Permite configurar inicio, meta, algoritmo y visualizar métricas.
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import threading
from config import *
from utils import Logger, load_random_flower_photo


class ControlPanel:
    """
    Panel de control de Tkinter para el simulador.
    Permite configurar parámetros y visualizar resultados.
    """
    
    def __init__(self, on_start_callback, on_reload_callback, on_position_change_callback):
        """
        Inicializa el panel de control.
        
        Args:
            on_start_callback: Función a llamar cuando se presiona Start
            on_reload_callback: Función a llamar cuando se presiona Reload
            on_position_change_callback: Función a llamar cuando cambian posiciones
        """
        self.on_start_callback = on_start_callback
        self.on_reload_callback = on_reload_callback
        self.on_position_change_callback = on_position_change_callback
        
        self.root = None
        self.running = False
        
        # Variables de control (se inicializarán después de crear root)
        self.bee_x = None
        self.bee_y = None
        self.hive_x = None
        self.hive_y = None
        self.algorithm = None
        self.mode = None
        
        Logger.log("ControlPanel inicializado")
    
    def create_window(self):
        """Crea la ventana de Tkinter."""
        self.root = tk.Tk()
        self.root.title("🐝 Control de Simulación - Abeja Inteligente")
        self.root.geometry("450x700")
        self.root.resizable(False, False)
        
        # Inicializar variables de control DESPUÉS de crear root
        self.bee_x = tk.IntVar(value=0)
        self.bee_y = tk.IntVar(value=0)
        self.hive_x = tk.IntVar(value=GRID_SIZE-1)
        self.hive_y = tk.IntVar(value=GRID_SIZE-1)
        self.algorithm = tk.StringVar(value="BFS")
        self.mode = tk.StringVar(value="exploration")
        
        # Protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self._create_widgets()
        Logger.log("Ventana de control creada")
    
    def _create_widgets(self):
        """Crea todos los widgets de la interfaz."""
        # Título
        title_label = tk.Label(
            self.root, 
            text="🐝 Simulador de Abeja Inteligente",
            font=("Arial", 16, "bold"),
            bg="#FFD700",
            pady=10
        )
        title_label.pack(fill=tk.X)
        
        # Frame de configuración de posiciones
        pos_frame = ttk.LabelFrame(self.root, text="📍 Configuración de Posiciones", padding=10)
        pos_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Posición de la abeja
        ttk.Label(pos_frame, text="Posición Abeja (X, Y):").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        bee_frame = ttk.Frame(pos_frame)
        bee_frame.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Spinbox(
            bee_frame, 
            from_=0, 
            to=GRID_SIZE-1, 
            textvariable=self.bee_x,
            width=8,
            command=self._on_position_change
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Spinbox(
            bee_frame, 
            from_=0, 
            to=GRID_SIZE-1, 
            textvariable=self.bee_y,
            width=8,
            command=self._on_position_change
        ).pack(side=tk.LEFT, padx=2)
        
        # Posición de la colmena
        ttk.Label(pos_frame, text="Posición Colmena (X, Y):").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        hive_frame = ttk.Frame(pos_frame)
        hive_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Spinbox(
            hive_frame, 
            from_=0, 
            to=GRID_SIZE-1, 
            textvariable=self.hive_x,
            width=8,
            command=self._on_position_change
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Spinbox(
            hive_frame, 
            from_=0, 
            to=GRID_SIZE-1, 
            textvariable=self.hive_y,
            width=8,
            command=self._on_position_change
        ).pack(side=tk.LEFT, padx=2)
        
        # Frame de algoritmo
        algo_frame = ttk.LabelFrame(self.root, text="🔍 Configuración de Búsqueda", padding=10)
        algo_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(algo_frame, text="Algoritmo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        algo_combo = ttk.Combobox(
            algo_frame, 
            textvariable=self.algorithm,
            values=["BFS", "DFS"],
            state="readonly",
            width=15
        )
        algo_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(algo_frame, text="Modo:").grid(row=1, column=0, sticky=tk.W, pady=5)
        mode_combo = ttk.Combobox(
            algo_frame,
            textvariable=self.mode,
            values=["exploration", "optimal"],
            state="readonly",
            width=15
        )
        mode_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Frame de controles
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_button = ttk.Button(
            control_frame,
            text="▶ Iniciar Simulación",
            command=self._on_start,
            width=20
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.reload_button = ttk.Button(
            control_frame,
            text="🔄 Recargar Mundo",
            command=self._on_reload,
            width=20
        )
        self.reload_button.pack(side=tk.LEFT, padx=5)
        
        # Frame de métricas
        metrics_frame = ttk.LabelFrame(self.root, text="📊 Métricas en Tiempo Real", padding=10)
        metrics_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.metrics_text = scrolledtext.ScrolledText(
            metrics_frame,
            height=15,
            width=50,
            font=("Courier", 9),
            state=tk.DISABLED
        )
        self.metrics_text.pack(fill=tk.BOTH, expand=True)
        
        # Inicializar métricas
        self.update_metrics("Sistema inicializado. Presiona 'Iniciar Simulación' para comenzar.")
    
    def _on_position_change(self):
        """Callback cuando cambian las posiciones."""
        if self.on_position_change_callback and self.bee_x is not None:
            bee_pos = (self.bee_x.get(), self.bee_y.get())
            hive_pos = (self.hive_x.get(), self.hive_y.get())
            self.on_position_change_callback(bee_pos, hive_pos)
    
    def _on_start(self):
        """Callback para el botón Start."""
        if self.on_start_callback:
            config = {
                'bee_pos': (self.bee_x.get(), self.bee_y.get()),
                'hive_pos': (self.hive_x.get(), self.hive_y.get()),
                'algorithm': self.algorithm.get(),
                'mode': self.mode.get()
            }
            self.on_start_callback(config)
    
    def _on_reload(self):
        """Callback para el botón Reload."""
        if self.on_reload_callback:
            self.on_reload_callback()
    
    def update_metrics(self, text):
        """
        Actualiza el panel de métricas.
        
        Args:
            text: Texto a mostrar (puede ser multi-línea)
        """
        if self.metrics_text:
            self.metrics_text.config(state=tk.NORMAL)
            self.metrics_text.delete(1.0, tk.END)
            self.metrics_text.insert(tk.END, text)
            self.metrics_text.config(state=tk.DISABLED)
            self.metrics_text.see(tk.END)
    
    def append_metrics(self, text):
        """
        Añade texto al panel de métricas.
        
        Args:
            text: Texto a añadir
        """
        if self.metrics_text:
            self.metrics_text.config(state=tk.NORMAL)
            self.metrics_text.insert(tk.END, text + "\n")
            self.metrics_text.config(state=tk.DISABLED)
            self.metrics_text.see(tk.END)
    
    def show_flower_detail(self, flower_image_path):
        """
        Muestra una ventana emergente con detalles de una flor.
        
        Args:
            flower_image_path: Ruta a la imagen de flor de alta resolución
        """
        detail_window = tk.Toplevel(self.root)
        detail_window.title("🌸 Flor Detectada - Vista Detallada")
        detail_window.geometry("400x500")
        
        # Título
        title = tk.Label(
            detail_window,
            text="🌸 ¡Flor Detectada!",
            font=("Arial", 14, "bold"),
            bg="#FFB6C1",
            pady=10
        )
        title.pack(fill=tk.X)
        
        try:
            # Cargar y mostrar imagen
            img = Image.open(flower_image_path)
            img = img.resize((350, 350), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            img_label = tk.Label(detail_window, image=photo)
            img_label.image = photo  # Mantener referencia
            img_label.pack(pady=10)
        except Exception as e:
            Logger.log(f"Error cargando imagen de flor: {e}", "ERROR")
            tk.Label(
                detail_window,
                text="Error cargando imagen",
                font=("Arial", 12)
            ).pack(pady=20)
        
        # Información
        info_text = "La abeja ha detectado una flor!\n"
        info_text += "Procesamiento de imagen aplicado:\n"
        info_text += "- Ecualización de histograma\n"
        info_text += "- Mejora de contraste\n"
        info_text += "- Clasificación con Transformer"
        
        info_label = tk.Label(
            detail_window,
            text=info_text,
            font=("Arial", 10),
            justify=tk.LEFT
        )
        info_label.pack(pady=10)
        
        # Botón cerrar
        close_btn = ttk.Button(
            detail_window,
            text="Cerrar",
            command=detail_window.destroy
        )
        close_btn.pack(pady=10)
        
        # Centrar ventana
        detail_window.transient(self.root)
        detail_window.grab_set()
    
    def on_closing(self):
        """Maneja el cierre de la ventana."""
        if messagebox.askokcancel("Salir", "¿Deseas cerrar el panel de control?"):
            self.running = False
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Inicia el loop principal de Tkinter."""
        if self.root:
            self.running = True
            Logger.log("Iniciando loop de Tkinter")
            self.root.mainloop()
    
    def update(self):
        """Actualiza la ventana (para llamar desde el loop principal)."""
        if self.root and self.running:
            try:
                self.root.update()
            except:
                pass


class MetricsComparator:
    """
    Clase para comparar métricas entre diferentes estrategias de búsqueda.
    """
    
    def __init__(self):
        self.results = []
        Logger.log("MetricsComparator inicializado")
    
    def add_result(self, algorithm, mode, metrics):
        """
        Añade un resultado de ejecución.
        
        Args:
            algorithm: Nombre del algoritmo (BFS/DFS)
            mode: Modo (exploration/optimal)
            metrics: Dict con métricas
        """
        result = {
            'algorithm': algorithm,
            'mode': mode,
            **metrics
        }
        self.results.append(result)
        Logger.log(f"Resultado añadido: {algorithm} - {mode}")
    
    def generate_comparison_report(self):
        """
        Genera un reporte comparativo de todas las ejecuciones.
        
        Returns:
            String con el reporte formateado
        """
        if not self.results:
            return "No hay resultados para comparar."
        
        report = "=" * 60 + "\n"
        report += "REPORTE COMPARATIVO DE ESTRATEGIAS DE BÚSQUEDA\n"
        report += "=" * 60 + "\n\n"
        
        for i, result in enumerate(self.results, 1):
            report += f"Ejecución #{i}: {result['algorithm']} - Modo {result['mode']}\n"
            report += "-" * 50 + "\n"
            report += f"  Pasos del camino: {result.get('path_length', 'N/A')}\n"
            report += f"  Nodos explorados: {result.get('explored_count', 'N/A')}\n"
            report += f"  Flores detectadas: {result.get('flowers_detected', 0)}\n"
            report += f"  Objetos detectados: {result.get('objects_detected', 0)}\n"
            report += f"  Precisión de detección: {result.get('detection_accuracy', 0):.2f}%\n"
            report += f"  Tiempo de ejecución: {result.get('execution_time', 0):.2f}s\n"
            report += "\n"
        
        # Análisis comparativo
        report += "=" * 60 + "\n"
        report += "ANÁLISIS COMPARATIVO\n"
        report += "=" * 60 + "\n\n"
        
        # Encontrar la estrategia más eficiente
        min_steps = min(r.get('path_length', float('inf')) for r in self.results)
        best_efficiency = [r for r in self.results if r.get('path_length') == min_steps]
        
        if best_efficiency:
            report += f"Estrategia más eficiente (menos pasos):\n"
            report += f"  {best_efficiency[0]['algorithm']} - {best_efficiency[0]['mode']}\n"
            report += f"  Pasos: {min_steps}\n\n"
        
        # Mejor precisión de detección
        max_accuracy = max(r.get('detection_accuracy', 0) for r in self.results)
        best_detection = [r for r in self.results if r.get('detection_accuracy') == max_accuracy]
        
        if best_detection:
            report += f"Mejor precisión de detección:\n"
            report += f"  {best_detection[0]['algorithm']} - {best_detection[0]['mode']}\n"
            report += f"  Precisión: {max_accuracy:.2f}%\n\n"
        
        return report
    
    def save_report(self, filename=METRICS_FILE):
        """Guarda el reporte en un archivo."""
        report = self.generate_comparison_report()
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            Logger.log(f"Reporte guardado en {filename}")
        except Exception as e:
            Logger.log(f"Error guardando reporte: {e}", "ERROR")
        
        return report
