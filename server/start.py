#!/usr/bin/env python3
"""
Starter Script - Inicia el servidor Flask de TecnicoAngeles
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Obtener ruta del proyecto
    server_dir = Path(__file__).parent
    
    print("=" * 70)
    print("SERVIDOR TECNICOANGELES - INICIANDO")
    print("=" * 70)
    print()
    
    # Verificar si requirements.txt existe
    requirements_file = server_dir / "requirements.txt"
    if not requirements_file.exists():
        print("Error: requirements.txt no encontrado")
        sys.exit(1)
    
    # Verificar si Flask está instalado
    try:
        import flask
        print("✓ Flask está instalado")
    except ImportError:
        print("✗ Flask no está instalado")
        print("  Instalando dependencias...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
    
    # Verificar si Flask-CORS está instalado
    try:
        import flask_cors
        print("✓ Flask-CORS está instalado")
    except ImportError:
        print("✗ Flask-CORS no está instalado")
        print("  Instalando dependencias...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
    
    print()
    print("=" * 70)
    print("INFORMACIÓN DEL SERVIDOR")
    print("=" * 70)
    print("URL Local:        http://localhost:5000")
    print("Base de datos:    usuarios.db")
    print("=" * 70)
    print()
    
    # Cambiar a directorio del servidor
    os.chdir(server_dir)
    
    # Ejecutar aplicación Flask
    try:
        import app
        app.app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error al iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
