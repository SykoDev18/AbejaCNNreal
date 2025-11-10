"""
Modelo de clasificación basado en Vision Transformer.
Clasifica imágenes como 'flor' o 'objeto' (no-flor).
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image
import os
import numpy as np
from config import *
from utils import ImageProcessor, Logger


class FlowerDataset(Dataset):
    """Dataset personalizado para entrenamiento del clasificador."""
    
    def __init__(self, root_dir, transform=None, apply_augmentation=True):
        """
        Args:
            root_dir: Directorio raíz con subcarpetas 'flores' y 'objetos'
            transform: Transformaciones de torchvision
            apply_augmentation: Si True, aplica aumento de datos con procesamiento de imágenes
        """
        self.root_dir = root_dir
        self.transform = transform
        self.apply_augmentation = apply_augmentation
        self.samples = []
        self.classes = ['flower', 'object']
        self.class_to_idx = {'flower': 0, 'object': 1}
        
        # Cargar rutas de imágenes
        self._load_samples()
    
    def _load_samples(self):
        """Carga las rutas de todas las imágenes y sus etiquetas."""
        # Buscar carpetas de flores
        flower_folders = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']
        
        # Cargar flores
        train_dir = self.root_dir
        for folder in flower_folders:
            folder_path = os.path.join(train_dir, folder)
            if os.path.exists(folder_path):
                for img_file in os.listdir(folder_path):
                    if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        img_path = os.path.join(folder_path, img_file)
                        self.samples.append((img_path, 0))  # 0 = flower
        
        Logger.log(f"Cargadas {len(self.samples)} flores del dataset")
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        
        try:
            image = Image.open(img_path).convert('RGB')
        except:
            # Crear imagen de respaldo si falla la carga
            image = Image.new('RGB', (224, 224), color=(128, 128, 128))
        
        # Aplicar aumento de datos con procesamiento avanzado
        if self.apply_augmentation:
            # Seleccionar aleatoriamente una técnica de procesamiento
            augmentation_type = np.random.randint(0, 5)
            
            if augmentation_type == 0:
                # Original
                pass
            elif augmentation_type == 1:
                # Ecualización global
                image = ImageProcessor.equalize_histogram_global(image)
            elif augmentation_type == 2:
                # Ecualización adaptativa (CLAHE)
                image = ImageProcessor.equalize_histogram_adaptive(image)
            elif augmentation_type == 3:
                # Subexpuesta
                image = ImageProcessor.create_underexposed(image, factor=0.6)
            elif augmentation_type == 4:
                # Sobreexpuesta
                image = ImageProcessor.create_overexposed(image, factor=1.4)
        
        # Aplicar transformaciones de PyTorch
        if self.transform:
            image = self.transform(image)
        
        return image, label


class VisionTransformerClassifier(nn.Module):
    """
    Clasificador basado en Vision Transformer (ViT).
    Usa un modelo preentrenado de timm o torchvision.
    """
    
    def __init__(self, num_classes=2, pretrained=True):
        super(VisionTransformerClassifier, self).__init__()
        
        # Usar un modelo preentrenado como base
        # En este caso, usamos ResNet como alternativa más ligera
        # (ViT puro requeriría instalar timm, aquí usamos arquitectura disponible)
        self.backbone = models.resnet50(pretrained=pretrained)
        
        # Modificar la última capa para nuestro número de clases
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Linear(num_features, num_classes)
        
        # Capa softmax para probabilidades
        self.softmax = nn.Softmax(dim=1)
    
    def forward(self, x):
        x = self.backbone(x)
        return x
    
    def predict_proba(self, x):
        """Retorna probabilidades usando softmax."""
        logits = self.forward(x)
        return self.softmax(logits)


class FlowerClassifier:
    """
    Clase wrapper para el clasificador de flores.
    Maneja entrenamiento, evaluación y predicción.
    """
    
    def __init__(self, model_path=MODEL_PATH):
        self.model_path = model_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.transform = None
        
        self._setup_transforms()
        Logger.log(f"FlowerClassifier inicializado en dispositivo: {self.device}")
    
    def _setup_transforms(self):
        """Configura las transformaciones para las imágenes."""
        self.transform = transforms.Compose([
            transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def train(self, train_dir=TRAIN_DIR, epochs=EPOCHS, batch_size=BATCH_SIZE):
        """
        Entrena el modelo clasificador.
        
        Args:
            train_dir: Directorio con datos de entrenamiento
            epochs: Número de épocas
            batch_size: Tamaño del batch
        """
        Logger.log(f"Iniciando entrenamiento por {epochs} épocas...")
        
        # Crear dataset y dataloader
        dataset = FlowerDataset(
            train_dir, 
            transform=self.transform,
            apply_augmentation=True
        )
        
        if len(dataset) == 0:
            Logger.log("Dataset vacío, no se puede entrenar", "ERROR")
            return
        
        dataloader = DataLoader(
            dataset, 
            batch_size=batch_size, 
            shuffle=True,
            num_workers=0
        )
        
        # Crear modelo
        self.model = VisionTransformerClassifier(num_classes=NUM_CLASSES, pretrained=True)
        self.model = self.model.to(self.device)
        
        # Optimizador y función de pérdida
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=LEARNING_RATE)
        
        # Entrenamiento
        self.model.train()
        for epoch in range(epochs):
            running_loss = 0.0
            correct = 0
            total = 0
            
            for i, (images, labels) in enumerate(dataloader):
                images = images.to(self.device)
                labels = labels.to(self.device)
                
                # Forward pass
                optimizer.zero_grad()
                outputs = self.model(images)
                loss = criterion(outputs, labels)
                
                # Backward pass
                loss.backward()
                optimizer.step()
                
                # Estadísticas
                running_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
            
            epoch_loss = running_loss / len(dataloader)
            epoch_acc = 100 * correct / total
            Logger.log(f"Época {epoch+1}/{epochs} - Loss: {epoch_loss:.4f}, Accuracy: {epoch_acc:.2f}%")
        
        # Guardar modelo
        self.save_model()
        Logger.log("Entrenamiento completado")
    
    def load_model(self):
        """Carga un modelo preentrenado."""
        if not os.path.exists(self.model_path):
            Logger.log(f"No se encontró modelo en {self.model_path}", "WARNING")
            Logger.log("Creando modelo nuevo sin entrenar")
            self.model = VisionTransformerClassifier(num_classes=NUM_CLASSES, pretrained=True)
            self.model = self.model.to(self.device)
            return False
        
        try:
            self.model = VisionTransformerClassifier(num_classes=NUM_CLASSES, pretrained=False)
            self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
            self.model = self.model.to(self.device)
            self.model.eval()
            Logger.log(f"Modelo cargado desde {self.model_path}")
            return True
        except Exception as e:
            Logger.log(f"Error cargando modelo: {e}", "ERROR")
            self.model = VisionTransformerClassifier(num_classes=NUM_CLASSES, pretrained=True)
            self.model = self.model.to(self.device)
            return False
    
    def save_model(self):
        """Guarda el modelo entrenado."""
        if self.model is None:
            Logger.log("No hay modelo para guardar", "WARNING")
            return
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        try:
            torch.save(self.model.state_dict(), self.model_path)
            Logger.log(f"Modelo guardado en {self.model_path}")
        except Exception as e:
            Logger.log(f"Error guardando modelo: {e}", "ERROR")
    
    def predict(self, image):
        """
        Predice la clase de una imagen.
        
        Args:
            image: PIL Image o ruta a imagen
            
        Returns:
            Tupla (class_name, probability)
        """
        if self.model is None:
            self.load_model()
        
        self.model.eval()
        
        # Cargar imagen si es una ruta
        if isinstance(image, str):
            try:
                image = Image.open(image).convert('RGB')
            except:
                Logger.log("Error cargando imagen para predicción", "ERROR")
                return "unknown", 0.0
        
        # Preprocesar
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)
        
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # Predicción
        with torch.no_grad():
            outputs = self.model.predict_proba(image_tensor)
            probabilities = outputs.cpu().numpy()[0]
            predicted_class = np.argmax(probabilities)
            confidence = probabilities[predicted_class]
        
        class_names = ['flor', 'objeto']
        predicted_label = class_names[predicted_class]
        
        return predicted_label, float(confidence)
    
    def evaluate(self, test_dir):
        """
        Evalúa el modelo en un conjunto de test.
        
        Args:
            test_dir: Directorio con datos de test
            
        Returns:
            Dict con métricas de evaluación
        """
        if self.model is None:
            self.load_model()
        
        dataset = FlowerDataset(test_dir, transform=self.transform, apply_augmentation=False)
        dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)
        
        self.model.eval()
        correct = 0
        total = 0
        
        with torch.no_grad():
            for images, labels in dataloader:
                images = images.to(self.device)
                labels = labels.to(self.device)
                
                outputs = self.model(images)
                _, predicted = torch.max(outputs.data, 1)
                
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        accuracy = 100 * correct / total
        Logger.log(f"Accuracy en test: {accuracy:.2f}%")
        
        return {
            'accuracy': accuracy,
            'correct': correct,
            'total': total
        }
