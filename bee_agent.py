"""
Clase BeeAgent - Representa la abeja que se mueve por el mundo.
Maneja el movimiento, detección de celdas e interacción con el clasificador.
"""
import time
from config import *
from utils import Logger, load_random_flower_test_image, load_random_object_image


class BeeAgent:
    """
    Representa la abeja autónoma que navega por el mundo cuadriculado.
    Realiza detección de flores y objetos usando el clasificador.
    """
    
    def __init__(self, grid_world, classifier):
        """
        Inicializa el agente abeja.
        
        Args:
            grid_world: Instancia de GridWorld
            classifier: Instancia de FlowerClassifier
        """
        self.grid_world = grid_world
        self.classifier = classifier
        self.position = None
        self.target = None
        
        # Estadísticas de detección
        self.flowers_detected = 0
        self.objects_detected = 0
        self.cells_visited = 0
        self.detection_log = []  # Lista de detecciones (pos, tipo, confianza)
        
        Logger.log("BeeAgent inicializado")
    
    def set_position(self, position):
        """Establece la posición actual de la abeja."""
        self.position = position
        self.grid_world.set_bee_position(position)
    
    def move_to(self, position):
        """
        Mueve la abeja a una nueva posición.
        
        Args:
            position: Tupla (x, y) de la nueva posición
        """
        if self.grid_world.is_walkable(position):
            self.position = position
            self.grid_world.set_bee_position(position)
            self.cells_visited += 1
            Logger.log(f"Abeja movida a {position}")
            return True
        else:
            Logger.log(f"Posición {position} no es transitable", "WARNING")
            return False
    
    def detect_cell_content(self, cell_type=None):
        """
        Detecta y clasifica el contenido de la celda actual.
        
        Args:
            cell_type: Tipo de celda (opcional). Si no se proporciona, se obtiene de la posición actual.
        """
        if self.position is None:
            return None, None, 0.0, None

        # Si no se proporciona el tipo de celda, obtenerlo
        if cell_type is None:
            cell_type = self.grid_world.get_cell_type(self.position)
        
        Logger.log(f"Detectando contenido en {self.position}, tipo de celda: {cell_type}")

        if cell_type not in [CELL_FLOWER, CELL_OBJECT]:
            return cell_type, None, 0.0, None

        # Seleccionar imagen según el tipo real de la celda
        if cell_type == CELL_FLOWER:
            image_path = load_random_flower_test_image(TEST_DIR)
            ground_truth = 'flor'
            Logger.log(f"Celda de FLOR detectada, cargando imagen de test: {image_path}")
        else:
            image_path = load_random_object_image(OBJECTS_DIR)
            ground_truth = 'objeto'
            Logger.log(f"Celda de OBJETO detectada, cargando imagen de objeto: {image_path}")

        classification = None
        confidence = 0.0

        if image_path:
            try:
                Logger.log(f"Clasificando imagen: {image_path}")
                classification, confidence = self.classifier.predict(image_path)
                Logger.log(f"Resultado: {classification} con confianza {confidence:.2f}")
            except Exception as e:
                Logger.log(f"Error clasificando imagen {image_path}: {e}", "ERROR")
                import traceback
                traceback.print_exc()
        else:
            Logger.log("No se encontró imagen para clasificación", "WARNING")

        is_correct = (classification == ground_truth)

        self.detection_log.append({
            'position': self.position,
            'image_path': image_path,
            'ground_truth': ground_truth,
            'prediction': classification,
            'confidence': confidence,
            'correct': is_correct
        })

        if classification is not None:
            if is_correct:
                if ground_truth == 'flor':
                    self.flowers_detected += 1
                else:
                    self.objects_detected += 1
                Logger.log(
                    f"✓ Análisis en {self.position} -> {classification} (confianza: {confidence:.2f})"
                )
            else:
                Logger.log(
                    f"✗ Clasificación incorrecta en {self.position}: {classification} frente a {ground_truth}",
                    "WARNING"
                )
        else:
            Logger.log("Clasificación no disponible", "WARNING")

        return cell_type, classification, confidence, image_path
    
    def follow_path(self, path, delay=0.1):
        """
        Sigue un camino paso a paso.
        
        Args:
            path: Lista de posiciones (x, y)
            delay: Tiempo de espera entre pasos (segundos)
            
        Yields:
            Posición actual en cada paso
        """
        for position in path:
            self.move_to(position)
            
            # Detectar contenido si no es inicio ni meta
            if position != path[0] and position != path[-1]:
                self.detect_cell_content()
            
            yield position
            time.sleep(delay)
    
    def get_statistics(self):
        """
        Obtiene estadísticas de la ejecución de la abeja.
        
        Returns:
            Dict con estadísticas
        """
        correct_detections = sum(1 for det in self.detection_log if det['correct'])
        total_detections = len(self.detection_log)
        accuracy = (correct_detections / total_detections * 100) if total_detections > 0 else 0
        
        return {
            'cells_visited': self.cells_visited,
            'flowers_detected': self.flowers_detected,
            'objects_detected': self.objects_detected,
            'total_detections': total_detections,
            'correct_detections': correct_detections,
            'detection_accuracy': accuracy,
            'detection_log': self.detection_log
        }
    
    def reset_statistics(self):
        """Reinicia las estadísticas de detección."""
        self.flowers_detected = 0
        self.objects_detected = 0
        self.cells_visited = 0
        self.detection_log = []
        Logger.log("Estadísticas de la abeja reiniciadas")
    
    def reached_goal(self):
        """Verifica si la abeja llegó a la colmena."""
        return self.position == self.grid_world.hive_pos
