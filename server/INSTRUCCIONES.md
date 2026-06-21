# TecnicoAngeles - Servidor Backend

Servidor Flask profesional para autenticación, registro de usuarios y gestión de sesiones.

## 🚀 Inicio Rápido

### Windows
```bash
cd server
start.bat
```

### Linux/Mac
```bash
cd server
chmod +x start.sh
./start.sh
```

### Manual
```bash
cd server
pip install -r requirements.txt
python app.py
```

## 📊 Base de Datos

El servidor usa **SQLite** con las siguientes tablas:

### usuarios
- `id` - ID único
- `username` - Nombre de usuario (único)
- `email` - Correo electrónico (único)
- `password` - Contraseña hasheada
- `created_at` - Fecha de creación
- `updated_at` - Última actualización

### sesiones
- `id` - ID único
- `usuario_id` - Referencia a usuario
- `token` - Token de sesión
- `fecha_creacion` - Fecha de inicio
- `fecha_expiracion` - Fecha de expiración (7 días)

### logs_acceso
- `id` - ID único
- `usuario_id` - Referencia a usuario
- `tipo` - Tipo de acceso (login, registro, logout, etc.)
- `detalles` - Detalles adicionales
- `fecha` - Fecha del evento

## 🔌 Endpoints API

### 1. Registro de Usuario
```
POST /api/auth/register
Content-Type: application/x-www-form-urlencoded

username=usuario&email=correo@example.com&password=Pass123&confirm_password=Pass123
```

**Respuesta exitosa (201):**
```json
{
  "message": "Registro exitoso. Ya puedes iniciar sesión."
}
```

### 2. Login
```
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=usuario&password=Pass123
```

**Respuesta exitosa (200):**
```json
{
  "message": "Sesión iniciada correctamente",
  "token": "token_unico_aqui",
  "username": "usuario"
}
```

### 3. Logout
```
POST /api/auth/logout
Authorization: Bearer {token}
```

**Respuesta exitosa (200):**
```json
{
  "message": "Sesión cerrada correctamente"
}
```

### 4. Verificar Token
```
GET /api/auth/verify
Authorization: Bearer {token}
```

**Respuesta exitosa (200):**
```json
{
  "valid": true,
  "user": {
    "id": 1,
    "username": "usuario",
    "email": "correo@example.com"
  }
}
```

### 5. Obtener Perfil
```
GET /api/auth/profile
Authorization: Bearer {token}
```

**Respuesta exitosa (200):**
```json
{
  "user": {
    "id": 1,
    "username": "usuario",
    "email": "correo@example.com",
    "created_at": "2024-05-31 10:30:00"
  }
}
```

### 6. Health Check
```
GET /api/health
```

**Respuesta (200):**
```json
{
  "status": "ok",
  "message": "Servidor funcionando"
}
```

## 🔐 Seguridad

- ✅ Contraseñas hasheadas con PBKDF2
- ✅ Tokens de sesión únicos con expiración
- ✅ CORS habilitado para desarrollo
- ✅ Validación de email
- ✅ Validación de contraseña
- ✅ Logs de acceso
- ✅ Protección contra inyección SQL

## ⚙️ Configuración

### Variables de Entorno (Opcional)

Crear archivo `.env` en la carpeta `server`:
```
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-aqui
DATABASE=usuarios.db
```

### Cambiar URL del Servidor

En `js/auth.js`:
```javascript
// Desarrollo local
BASE_URL: "http://localhost:5000"

// Con ngrok
BASE_URL: "https://tu-url.ngrok-free.dev"
```

## 📱 Usar con ngrok

Para exponer el servidor públicamente:

```bash
# En otra terminal
ngrok http 5000
```

Usa la URL generada en `js/auth.js`.

## 🛠️ Desarrollo

### Estructura
```
server/
├── app.py              # Aplicación principal Flask
├── requirements.txt    # Dependencias
├── usuarios.db         # Base de datos (se crea automáticamente)
├── start.bat          # Script de inicio Windows
├── start.sh           # Script de inicio Linux/Mac
├── setup.bat          # Script de instalación Windows
├── setup.sh           # Script de instalación Linux/Mac
└── README.md          # Este archivo
```

### Logs

Los logs de acceso se guardan en la tabla `logs_acceso`:
- **registro_exitoso** - Nuevo usuario registrado
- **registro_fallido** - Intento de registro fallido
- **login_exitoso** - Login exitoso
- **login_fallido** - Intento de login fallido

## 🐛 Troubleshooting

### Error: "Port 5000 already in use"
```bash
# Cambiar puerto en app.py
app.run(port=5001)
```

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error de CORS
Asegúrate que Flask-CORS está instalado:
```bash
pip install Flask-CORS
```

## 📝 Licencia

© 2024 TecnicoAngeles - Todos los derechos reservados
