@echo off
REM Script de instalación del servidor TecnicoAngeles

echo ========================================
echo Servidor TecnicoAngeles - Setup
echo ========================================

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en PATH
    pause
    exit /b 1
)

echo.
echo Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error al instalar dependencias
    pause
    exit /b 1
)

echo.
echo ========================================
echo Instalación completada
echo ========================================
echo.
echo Para ejecutar el servidor:
echo   python app.py
echo.
echo Para exponer con ngrok:
echo   ngrok http 5000
echo.
pause
