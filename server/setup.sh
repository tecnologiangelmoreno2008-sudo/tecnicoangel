#!/bin/bash

echo "========================================"
echo "Servidor TecnicoAngeles - Setup"
echo "========================================"

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado"
    exit 1
fi

echo ""
echo "Instalando dependencias..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error al instalar dependencias"
    exit 1
fi

echo ""
echo "========================================"
echo "Instalación completada"
echo "========================================"
echo ""
echo "Para ejecutar el servidor:"
echo "  python3 app.py"
echo ""
echo "Para exponer con ngrok:"
echo "  ngrok http 5000"
echo ""
