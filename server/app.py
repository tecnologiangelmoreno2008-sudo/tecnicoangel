"""
Servidor Backend - TecnicoAngeles
Sistema de autenticación con registro, login y gestión de sesiones
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
import os
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-muy-segura-cambiar-en-produccion'

# Habilitar CORS para que funcione con ngrok
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuración de base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'usuarios.db')

def init_db():
    """Inicializa la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de sesiones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sesiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_expiracion TIMESTAMP NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
        )
    ''')
    
    # Tabla de logs de acceso
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs_acceso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            tipo TEXT NOT NULL,
            detalles TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE SET NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db():
    """Obtiene conexión a la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def registrar_log(usuario_id, tipo, detalles=""):
    """Registra acciones en la base de datos"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs_acceso (usuario_id, tipo, detalles)
        VALUES (?, ?, ?)
    ''', (usuario_id, tipo, detalles))
    conn.commit()
    conn.close()

def validar_email(email):
    """Valida formato de email"""
    import re
    patron = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(patron, email) is not None

def validar_contrasena(password):
    """Valida requisitos de contraseña"""
    if len(password) < 6:
        return False, "La contraseña debe tener mínimo 6 caracteres"
    if not any(c.isalpha() for c in password):
        return False, "La contraseña debe contener letras"
    if not any(c.isdigit() for c in password):
        return False, "La contraseña debe contener números"
    return True, "Válida"

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de verificación de salud"""
    return jsonify({"status": "ok", "message": "Servidor funcionando"}), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Endpoint de registro de usuarios"""
    try:
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validaciones
        if not all([username, email, password, confirm_password]):
            return jsonify({"error": "Todos los campos son requeridos"}), 400
        
        if len(username) < 3 or len(username) > 20:
            return jsonify({"error": "El usuario debe tener entre 3 y 20 caracteres"}), 400
        
        if not validar_email(email):
            return jsonify({"error": "Correo electrónico no válido"}), 400
        
        if password != confirm_password:
            return jsonify({"error": "Las contraseñas no coinciden"}), 400
        
        valido, mensaje = validar_contrasena(password)
        if not valido:
            return jsonify({"error": mensaje}), 400
        
        # Verificar si el usuario ya existe
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM usuarios WHERE username = ? OR email = ?', 
                      (username, email))
        if cursor.fetchone():
            registrar_log(None, "registro_fallido", f"Usuario {username} ya existe")
            return jsonify({"error": "El usuario o email ya está registrado"}), 409
        
        # Crear usuario
        hashed_password = generate_password_hash(password)
        try:
            cursor.execute('''
                INSERT INTO usuarios (username, email, password)
                VALUES (?, ?, ?)
            ''', (username, email, hashed_password))
            conn.commit()
            usuario_id = cursor.lastrowid
            
            registrar_log(usuario_id, "registro_exitoso")
            return jsonify({"message": "Registro exitoso. Ya puedes iniciar sesión."}), 201
        
        except sqlite3.IntegrityError:
            conn.rollback()
            return jsonify({"error": "Error al registrar usuario"}), 500
        finally:
            conn.close()
    
    except Exception as e:
        print(f"Error en registro: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Endpoint de login"""
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            return jsonify({"error": "Usuario y contraseña requeridos"}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Buscar usuario
        cursor.execute('SELECT id, username, password FROM usuarios WHERE username = ?', 
                      (username,))
        usuario = cursor.fetchone()
        
        if not usuario or not check_password_hash(usuario['password'], password):
            registrar_log(None, "login_fallido", f"Intento fallido: {username}")
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401
        
        # Crear token de sesión
        token = secrets.token_urlsafe(32)
        fecha_expiracion = datetime.now() + timedelta(days=7)
        
        cursor.execute('''
            INSERT INTO sesiones (usuario_id, token, fecha_expiracion)
            VALUES (?, ?, ?)
        ''', (usuario['id'], token, fecha_expiracion))
        conn.commit()
        conn.close()
        
        registrar_log(usuario['id'], "login_exitoso")
        
        return jsonify({
            "message": "Sesión iniciada correctamente",
            "token": token,
            "username": usuario['username']
        }), 200
    
    except Exception as e:
        print(f"Error en login: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Endpoint de logout"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({"error": "Token requerido"}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM sesiones WHERE token = ?', (token,))
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Sesión cerrada correctamente"}), 200
    
    except Exception as e:
        print(f"Error en logout: {str(e)}")
        return jsonify({"error": "Error al cerrar sesión"}), 500

@app.route('/api/auth/verify', methods=['GET'])
def verify():
    """Verifica si un token es válido"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({"error": "Token requerido"}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.id, u.username, u.email, s.fecha_expiracion
            FROM sesiones s
            JOIN usuarios u ON s.usuario_id = u.id
            WHERE s.token = ? AND s.fecha_expiracion > datetime('now')
        ''', (token,))
        
        sesion = cursor.fetchone()
        conn.close()
        
        if not sesion:
            return jsonify({"error": "Token inválido o expirado"}), 401
        
        return jsonify({
            "valid": True,
            "user": {
                "id": sesion['id'],
                "username": sesion['username'],
                "email": sesion['email']
            }
        }), 200
    
    except Exception as e:
        print(f"Error en verify: {str(e)}")
        return jsonify({"error": "Error al verificar token"}), 500

@app.route('/api/auth/profile', methods=['GET'])
def get_profile():
    """Obtiene perfil del usuario autenticado"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({"error": "No autorizado"}), 401
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.id, u.username, u.email, u.created_at
            FROM sesiones s
            JOIN usuarios u ON s.usuario_id = u.id
            WHERE s.token = ? AND s.fecha_expiracion > datetime('now')
        ''', (token,))
        
        usuario = cursor.fetchone()
        conn.close()
        
        if not usuario:
            return jsonify({"error": "Token inválido"}), 401
        
        return jsonify({
            "user": {
                "id": usuario['id'],
                "username": usuario['username'],
                "email": usuario['email'],
                "created_at": usuario['created_at']
            }
        }), 200
    
    except Exception as e:
        print(f"Error en profile: {str(e)}")
        return jsonify({"error": "Error al obtener perfil"}), 500

@app.errorhandler(404)
def not_found(error):
    """Maneja errores 404"""
    return jsonify({"error": "Endpoint no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Maneja errores 500"""
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    # Inicializar base de datos
    init_db()
    
    # Ejecutar servidor
    print("=" * 60)
    print("Servidor TecnicoAngeles iniciado")
    print("=" * 60)
    print("Base de datos: {}".format(DB_PATH))
    print("Puerto: 5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
