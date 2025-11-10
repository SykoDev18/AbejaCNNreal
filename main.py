"""
MAIN - Simulador de Abeja Inteligente
Integra Pygame, Tkinter, algoritmos de búsqueda y clasificación con Transformers.

Este es el archivo principal que orquesta todo el sistema.
"""
import os
import pygame
import sys
import threading
import time
from config import *
from grid_world import GridWorld
from search_algorithms import PathFinder
from bee_agent import BeeAgent
from flower_classifier import FlowerClassifier
from gui_controller import ControlPanel, MetricsComparator
from utils import Logger, load_random_flower_photo


class BeeSimulator:
    """
    Clase principal que integra todos los componentes del simulador.
    Maneja la lógica de Pygame, Tkinter y la coordinación entre módulos.
    """
    
    def __init__(self):
        """Inicializa el simulador."""
        Logger.log("=" * 60)
        Logger.log("Iniciando Simulador de Abeja Inteligente")
        Logger.log("=" * 60)
        
        # Inicializar Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🐝 Simulador de Abeja Inteligente - Pygame")
        self.clock = pygame.time.Clock()
        
        # Componentes principales
        self.grid_world = GridWorld(GRID_SIZE)
        self.classifier = FlowerClassifier()
        self.bee_agent = BeeAgent(self.grid_world, self.classifier)
        self.pathfinder = PathFinder(self.grid_world)
        
        # Panel de control (Tkinter)
        self.control_panel = ControlPanel(
            on_start_callback=self.start_simulation,
            on_reload_callback=self.reload_world,
            on_position_change_callback=self.update_positions
        )
        
        # Comparador de métricas
        self.metrics_comparator = MetricsComparator()
        
        # Estado de la simulación
        self.running = True
        self.simulation_active = False
        self.current_path = []
        self.explored_nodes = set()
        self.animation_step = 0
        
        # Configuración inicial
        self.current_config = {
            'bee_pos': (0, 0),
            'hive_pos': (GRID_SIZE-1, GRID_SIZE-1),
            'algorithm': 'BFS',
            'mode': 'exploration'
        }
        
        Logger.log("Simulador inicializado correctamente")
    
    def initialize(self):
        """Inicializa el mundo y los componentes."""
        # Intentar cargar modelo clasificador
        try:
            model_loaded = self.classifier.load_model()
            if not model_loaded:
                Logger.log("Modelo no encontrado. Se usará modelo sin entrenar.", "WARNING")
                self.control_panel.update_metrics(
                    "⚠ Advertencia: Modelo de clasificación no entrenado.\n"
                    "Para mejores resultados, entrena el modelo primero.\n\n"
                    "Presiona 'Iniciar Simulación' para continuar con el modelo base."
                )
        except Exception as e:
            Logger.log(f"Error cargando clasificador: {e}", "ERROR")
        
        # Inicializar mundo
        self.reload_world()
    
    def reload_world(self):
        """Recarga el mundo con nuevas posiciones aleatorias."""
        Logger.log("Recargando mundo...")
        
        bee_pos = self.current_config['bee_pos']
        hive_pos = self.current_config['hive_pos']
        
        self.grid_world.initialize_world(bee_pos, hive_pos)
        self.bee_agent.set_position(bee_pos)
        self.bee_agent.reset_statistics()
        
        self.current_path = []
        self.explored_nodes = set()
        self.simulation_active = False
        
        Logger.log("Mundo recargado exitosamente")
        
        if self.control_panel.root:
            self.control_panel.update_metrics(
                f"🌍 Mundo recargado\n"
                f"Tamaño: {GRID_SIZE}x{GRID_SIZE}\n"
                f"Abeja: {bee_pos}\n"
                f"Colmena: {hive_pos}\n"
                f"Obstáculos: {len(self.grid_world.obstacles)}\n"
                f"Flores: {len(self.grid_world.flowers)}\n"
                f"Objetos: {len(self.grid_world.objects)}\n\n"
                f"Presiona 'Iniciar Simulación' para comenzar."
            )
    
    def update_positions(self, bee_pos, hive_pos):
        """
        Actualiza las posiciones de la abeja y la colmena.
        
        Args:
            bee_pos: Nueva posición de la abeja
            hive_pos: Nueva posición de la colmena
        """
        self.current_config['bee_pos'] = bee_pos
        self.current_config['hive_pos'] = hive_pos
        
        # Si no hay simulación activa, actualizar inmediatamente
        if not self.simulation_active:
            self.grid_world.bee_pos = bee_pos
            self.grid_world.hive_pos = hive_pos
            self.bee_agent.set_position(bee_pos)
            Logger.log(f"Posiciones actualizadas: Abeja={bee_pos}, Colmena={hive_pos}")
    
    def start_simulation(self, config):
        """
        Inicia la simulación con la configuración dada.
        
        Args:
            config: Dict con configuración (bee_pos, hive_pos, algorithm, mode)
        """
        if self.simulation_active:
            Logger.log("Ya hay una simulación en curso", "WARNING")
            return
        
        self.current_config = config
        Logger.log(f"Iniciando simulación con: {config}")
        
        # Actualizar métricas
        self.control_panel.update_metrics(
            f"🚀 INICIANDO SIMULACIÓN\n"
            f"{'='*40}\n"
            f"Algoritmo: {config['algorithm']}\n"
            f"Modo: {config['mode']}\n"
            f"Inicio: {config['bee_pos']}\n"
            f"Meta: {config['hive_pos']}\n"
            f"{'='*40}\n\n"
            f"Buscando camino...\n"
        )
        
        # Configurar algoritmo
        self.pathfinder.set_algorithm(config['algorithm'])
        
        # Reiniciar estadísticas
        self.bee_agent.reset_statistics()
        self.bee_agent.set_position(config['bee_pos'])
        
        self.simulation_active = True
        self.animation_step = 0
        
        if config['mode'] == 'exploration':
            # Animar exploración paso a paso
            self.animate_exploration(config['bee_pos'], config['hive_pos'], config['mode'])
        else:
            # Encontrar path óptimo y animar movimiento
            start_time = time.time()
            
            path, explored, steps = self.pathfinder.find_path(
                config['bee_pos'],
                config['hive_pos'],
                mode=config['mode']
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            self.current_path = path
            self.explored_nodes = explored
            
            if not path:
                Logger.log("No se encontró camino a la meta", "ERROR")
                self.control_panel.append_metrics(
                    "❌ ERROR: No se encontró camino a la meta.\n"
                    "Verifica que no haya obstáculos bloqueando el camino."
                )
                self.simulation_active = False
                return
            
            Logger.log(f"Camino encontrado: {len(path)} pasos, {len(explored)} nodos explorados")
            
            # Actualizar métricas iniciales
            self.control_panel.append_metrics(
                f"✓ Camino encontrado!\n"
                f"  Longitud del camino: {len(path)} pasos\n"
                f"  Nodos explorados: {len(explored)}\n"
                f"  Tiempo de búsqueda: {execution_time:.3f}s\n\n"
                f"Iniciando movimiento de la abeja...\n"
            )
            
            # Ejecutar animación de movimiento
            threading.Thread(target=self.animate_path, daemon=True).start()
    
    def animate_path(self):
        """Anima el movimiento de la abeja a lo largo del camino."""
        if not self.current_path:
            return
        
        for i, position in enumerate(self.current_path):
            if not self.simulation_active or not self.running:
                break
            
            # Verificar el tipo de celda ANTES de mover la abeja
            cell_type = self.grid_world.get_cell_type(position)
            
            # Mover abeja
            self.bee_agent.move_to(position)
            
            # Solo detectar si hay flor u objeto (verificamos el tipo que tenía antes de moverse)
            detected = False
            if cell_type in [CELL_FLOWER, CELL_OBJECT]:
                _, classification, confidence, analyzed_image = self.bee_agent.detect_cell_content(cell_type)
                detected = True
                image_name = os.path.basename(analyzed_image) if analyzed_image else 'N/A'
                confidence_text = f"{confidence:.2f}" if isinstance(confidence, (int, float)) else 'N/A'
                
                metrics_text = (
                    f"🔍 ANÁLISIS DE CONTENIDO\n"
                    f"Paso {i+1}/{len(self.current_path)}\n"
                    f"Posición: {position}\n"
                    f"Tipo de celda: {'Flor' if cell_type == CELL_FLOWER else 'Objeto'}\n"
                    f"Imagen analizada: {image_name}\n"
                    f"Predicción: {classification if classification else 'N/A'}\n"
                    f"Confianza: {confidence_text}\n"
                    f"{'='*40}\n"
                )
                
                self.control_panel.root.after(
                    0,
                    lambda text=metrics_text: self.control_panel.append_metrics(text)
                )
            
            # Delay para visualización (más tiempo si detectó)
            delay = ANALYSIS_DELAY if detected else SEARCH_DELAY
            time.sleep(delay)
        
        # Simulación completada
        self.on_simulation_complete()
    
    def animate_exploration(self, start, goal, mode):
        """Anima la exploración paso a paso del algoritmo."""
        Logger.log(f"Iniciando animación de exploración en modo {mode}")
        
        # Obtener generador de exploración
        exploration_generator = self.pathfinder.find_path_animated(start, goal, mode)
        
        explored_nodes = set()
        path_found = []
        found = False
        
        for current_pos, explored, found_flag, path in exploration_generator:
            if not self.simulation_active or not self.running:
                break
            
            # Verificar el tipo de celda ANTES de mover la abeja
            cell_type = self.grid_world.get_cell_type(current_pos)
            
            # Mover abeja a la posición actual
            self.bee_agent.move_to(current_pos)
            
            # Detectar si es celda con contenido
            detected = False
            if cell_type in [CELL_FLOWER, CELL_OBJECT]:
                _, classification, confidence, analyzed_image = self.bee_agent.detect_cell_content(cell_type)
                detected = True
            
            # Actualizar nodos explorados
            explored_nodes = explored
            if found_flag:
                found = True
                path_found = path
            
            # Actualizar visualización (resaltar nodos explorados)
            self.explored_nodes = list(explored_nodes)
            
            # Actualizar métricas
            last_detection = self.bee_agent.detection_log[-1] if self.bee_agent.detection_log else None
            image_name = os.path.basename(last_detection['image_path']) if last_detection and last_detection.get('image_path') else 'N/A'
            prediction = last_detection.get('prediction') if last_detection else None
            confidence_value = last_detection.get('confidence') if last_detection else None
            confidence_text = f"{confidence_value:.2f}" if isinstance(confidence_value, (int, float)) else 'N/A'
            metrics_text = (
                f"Explorando...\n"
                f"Nodo actual: {current_pos}\n"
                f"Imagen analizada: {image_name}\n"
                f"Predicción: {prediction if prediction else 'N/A'}\n"
                f"Confianza: {confidence_text}\n"
                f"Nodos explorados: {len(explored_nodes)}\n"
                f"Meta encontrada: {'Sí' if found else 'No'}\n"
            )
            
            if self.control_panel.root:
                self.control_panel.root.after(
                    0,
                    lambda text=metrics_text: self.control_panel.append_metrics(text)
                )
            
            # Delay para visualización (más tiempo si detectó)
            delay = ANALYSIS_DELAY if detected else SEARCH_DELAY
            time.sleep(delay)
        
        # Exploración completada
        if found:
            Logger.log(f"Meta encontrada durante exploración. Camino: {len(path_found)} pasos")
            self.current_path = path_found
            self.control_panel.append_metrics(
                f"\n✓ Meta encontrada!\n"
                f"Camino óptimo: {len(path_found)} pasos\n"
                f"Total explorados: {len(explored_nodes)}\n"
            )
        else:
            Logger.log("Exploración completada sin encontrar meta")
            self.current_path = []
            self.control_panel.append_metrics(
                f"\n✓ Exploración completada\n"
                f"Total nodos explorados: {len(explored_nodes)}\n"
                f"Meta no encontrada (posiblemente inaccesible)\n"
            )
        
        # Completar simulación
        self.on_simulation_complete()
    
    def on_simulation_complete(self):
        """Callback cuando la simulación se completa."""
        Logger.log("Simulación completada")
        
        # Obtener estadísticas
        stats = self.bee_agent.get_statistics()
        
        # Crear reporte
        report = (
            f"\n{'='*40}\n"
            f"🏁 SIMULACIÓN COMPLETADA\n"
            f"{'='*40}\n\n"
            f"📊 ESTADÍSTICAS FINALES:\n"
            f"  Algoritmo: {self.current_config['algorithm']}\n"
            f"  Modo: {self.current_config['mode']}\n"
        )
        
        if self.current_config['mode'] == 'exploration':
            report += (
                f"  Nodos explorados: {len(self.explored_nodes)}\n"
                f"  Meta encontrada: {'Sí' if self.current_path else 'No'}\n"
                f"  Longitud del camino: {len(self.current_path)} pasos\n"
                f"\n✓ Exploración completada!\n"
            )
        else:
            report += (
                f"  Longitud del camino: {len(self.current_path)} pasos\n"
                f"  Nodos explorados: {len(self.explored_nodes)}\n"
                f"  Celdas visitadas: {stats['cells_visited']}\n"
                f"  Flores detectadas: {stats['flowers_detected']}\n"
                f"  Objetos detectados: {stats['objects_detected']}\n"
                f"  Precisión de detección: {stats['detection_accuracy']:.2f}%\n"
                f"\n✓ La abeja ha llegado a la colmena!\n"
            )
        
        self.control_panel.append_metrics(report)
        
        # Guardar métricas para comparación
        metrics = {
            'path_length': len(self.current_path),
            'explored_count': len(self.explored_nodes),
            'flowers_detected': stats['flowers_detected'] if self.current_config['mode'] != 'exploration' else 0,
            'objects_detected': stats['objects_detected'] if self.current_config['mode'] != 'exploration' else 0,
            'detection_accuracy': stats['detection_accuracy'] if self.current_config['mode'] != 'exploration' else 0.0,
            'execution_time': 0  # Se calcularía en la animación
        }
        
        self.metrics_comparator.add_result(
            self.current_config['algorithm'],
            self.current_config['mode'],
            metrics
        )
        
        self.simulation_active = False
    
    def handle_events(self):
        """Maneja eventos de Pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                elif event.key == pygame.K_r:
                    # Recargar mundo
                    self.reload_world()
                
                elif event.key == pygame.K_SPACE:
                    # Toggle simulación
                    if not self.simulation_active:
                        self.start_simulation(self.current_config)
    
    def render(self):
        """Renderiza el mundo en Pygame."""
        self.grid_world.render(
            self.screen,
            path=self.current_path,
            explored=self.explored_nodes
        )
        
        # Dibujar información en pantalla
        font = pygame.font.Font(None, 24)
        
        info_texts = [
            f"Algoritmo: {self.current_config['algorithm']} - {self.current_config['mode']}",
            f"Posición: {self.bee_agent.position}",
            f"Flores: {self.bee_agent.flowers_detected} | Objetos: {self.bee_agent.objects_detected}"
        ]
        
        y_offset = 5
        for text in info_texts:
            text_surface = font.render(text, True, COLOR_BLACK, COLOR_WHITE)
            self.screen.blit(text_surface, (5, y_offset))
            y_offset += 25
        
        pygame.display.flip()
    
    def run(self):
        """Loop principal del simulador."""
        Logger.log("Iniciando loop principal")
        
        # Inicializar
        self.initialize()
        
        # Crear y ejecutar ventana de control en un hilo separado
        def run_tkinter():
            self.control_panel.create_window()
            self.control_panel.run()  # Esto ejecuta mainloop()
        
        control_thread = threading.Thread(target=run_tkinter, daemon=True)
        control_thread.start()
        
        # Esperar a que se cree la ventana
        time.sleep(0.5)
        
        # Loop principal de Pygame
        while self.running:
            self.handle_events()
            self.render()
            
            self.clock.tick(FPS)
        
        # Cleanup
        self.cleanup()
    
    def cleanup(self):
        """Limpia recursos al cerrar."""
        Logger.log("Cerrando simulador...")
        
        # Guardar reporte comparativo
        if len(self.metrics_comparator.results) > 0:
            report = self.metrics_comparator.save_report()
            Logger.log("Reporte de métricas guardado")
            print("\n" + report)
        
        pygame.quit()
        sys.exit()


def main():
    """Función principal."""
    try:
        simulator = BeeSimulator()
        simulator.run()
    except Exception as e:
        Logger.log(f"Error fatal: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()
