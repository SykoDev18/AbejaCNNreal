# Script de inicio rápido para el simulador

Write-Host ""
Write-Host "🐝 SIMULADOR DE ABEJA INTELIGENTE 🌸" -ForegroundColor Yellow
Write-Host ""
Write-Host "Selecciona una opción:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Instalar dependencias" -ForegroundColor White
Write-Host "2. Entrenar modelo de clasificación" -ForegroundColor White
Write-Host "3. Ver demo de procesamiento de imágenes" -ForegroundColor White
Write-Host "4. Ejecutar simulador principal" -ForegroundColor White
Write-Host "5. Salir" -ForegroundColor White
Write-Host ""

$opcion = Read-Host "Ingresa el número de opción"

switch ($opcion) {
    "1" {
        Write-Host ""
        Write-Host "Instalando dependencias..." -ForegroundColor Green
        .\install.ps1
    }
    "2" {
        Write-Host ""
        Write-Host "Entrenando modelo..." -ForegroundColor Green
        python train_model.py
    }
    "3" {
        Write-Host ""
        Write-Host "Ejecutando demo de procesamiento..." -ForegroundColor Green
        python demo_procesamiento_flores.py
    }
    "4" {
        Write-Host ""
        Write-Host "Iniciando simulador..." -ForegroundColor Green
        python main.py
    }
    "5" {
        Write-Host ""
        Write-Host "¡Hasta luego! 👋" -ForegroundColor Yellow
        exit 0
    }
    default {
        Write-Host ""
        Write-Host "Opción no válida" -ForegroundColor Red
        exit 1
    }
}
