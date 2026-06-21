@echo off
REM Script para iniciar el servidor TecnicoAngeles en Windows

setlocal enabledelayedexpansion

echo.
echo ========================================
echo SERVIDOR TECNICOANGELES - INICIANDO
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado
    echo Descarga Python desde: https://www.python.org
    pause
    exit /b 1
)

REM Verificar si existe requirements.txt
if not exist "requirements.txt" (
    echo Error: requirements.txt no encontrado
    pause
    exit /b 1
)

REM Instalar dependencias si es necesario
echo Verificando dependencias...
pip install -q -r requirements.txt

if errorlevel 1 (
    echo Error al instalar dependencias
    pause
    exit /b 1
)

echo.
echo ========================================
echo INFORMACIÓN DEL SERVIDOR
echo ========================================
echo URL Local:        http://localhost:5000
echo Base de datos:    usuarios.db
echo ========================================
echo.
echo Iniciando servidor...
echo.

REM Ejecutar servidor
python app.py 


pause
