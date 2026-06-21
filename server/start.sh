#!/bin/bash

# Script para iniciar el servidor TecnicoAngeles en Linux/Mac

echo ""
echo "========================================"
echo "SERVIDOR TECNICOANGELES - INICIANDO"
echo "========================================"
echo ""

# Verificar si Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado"
    echo "Instala Python desde: https://www.python.org"
    exit 1
fi

# Verificar si existe requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt no encontrado"
    exit 1
fi

# Instalar dependencias si es necesario
echo "Verificando dependencias..."
pip3 install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error al instalar dependencias"
    exit 1
fi

echo ""
echo "========================================"
echo "INFORMACIÓN DEL SERVIDOR"
echo "========================================"
echo "URL Local:        http://localhost:5000"
echo "Base de datos:    usuarios.db"
echo "========================================"
echo ""
echo "Iniciando servidor..."
echo ""

# Ejecutar servidor
python3 app.py
