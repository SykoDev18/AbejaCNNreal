# Script de instalación rápida para el Simulador de Abeja Inteligente

Write-Host "=" -NoNewline
for ($i = 0; $i -lt 59; $i++) { Write-Host "=" -NoNewline }
Write-Host ""
Write-Host "  INSTALADOR - SIMULADOR DE ABEJA INTELIGENTE"
Write-Host "=" -NoNewline
for ($i = 0; $i -lt 59; $i++) { Write-Host "=" -NoNewline }
Write-Host ""
Write-Host ""

# Verificar Python
Write-Host "[1/5] Verificando instalación de Python..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Error: Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "  Por favor instala Python 3.8 o superior desde https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# Verificar pip
Write-Host ""
Write-Host "[2/5] Verificando pip..." -ForegroundColor Cyan
try {
    $pipVersion = pip --version 2>&1
    Write-Host "  ✓ pip encontrado: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Error: pip no está instalado" -ForegroundColor Red
    exit 1
}

# Actualizar pip
Write-Host ""
Write-Host "[3/5] Actualizando pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip
Write-Host "  ✓ pip actualizado" -ForegroundColor Green

# Instalar dependencias
Write-Host ""
Write-Host "[4/5] Instalando dependencias..." -ForegroundColor Cyan
Write-Host "  Esto puede tomar varios minutos..." -ForegroundColor Yellow
Write-Host ""

pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "  ✓ Dependencias instaladas correctamente" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "  ✗ Error instalando dependencias" -ForegroundColor Red
    Write-Host "  Intenta instalar manualmente con: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Crear carpeta de modelos
Write-Host ""
Write-Host "[5/5] Creando estructura de carpetas..." -ForegroundColor Cyan
if (-not (Test-Path "models")) {
    New-Item -ItemType Directory -Path "models" | Out-Null
    Write-Host "  ✓ Carpeta 'models' creada" -ForegroundColor Green
} else {
    Write-Host "  ✓ Carpeta 'models' ya existe" -ForegroundColor Green
}

# Resumen
Write-Host ""
Write-Host "=" -NoNewline
for ($i = 0; $i -lt 59; $i++) { Write-Host "=" -NoNewline }
Write-Host ""
Write-Host "  INSTALACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "=" -NoNewline
for ($i = 0; $i -lt 59; $i++) { Write-Host "=" -NoNewline }
Write-Host ""
Write-Host ""

Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. [RECOMENDADO] Entrena el modelo de clasificación:" -ForegroundColor Cyan
Write-Host "   python train_model.py" -ForegroundColor White
Write-Host ""
Write-Host "2. Ejecuta el simulador principal:" -ForegroundColor Cyan
Write-Host "   python main.py" -ForegroundColor White
Write-Host ""
Write-Host "3. Lee el README.md para más información" -ForegroundColor Cyan
Write-Host ""

Write-Host "¡Disfruta del simulador! 🐝🌸" -ForegroundColor Green
Write-Host ""
