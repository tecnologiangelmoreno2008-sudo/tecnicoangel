# TecnicoAngeles - Sitio Web Profesional

Sistema completo de autenticación y registro de usuarios para TecnicoAngeles.

## 📋 Contenido del Proyecto

```
TecnicoAngel/
├── index.html                      # Página principal
├── login.html                      # Página de login
├── registro.html                   # Página de registro
├── styles/
│   └── styles.css                  # Estilos del sitio
├── js/
│   ├── auth.js                     # Módulo de autenticación
│   ├── config.js                   # Configuración centralizada
│   ├── logR.js                     # Script antiguo (opcional)
│   └── script.js                   # Script principal
├── docs/                           # Documentación
├── imgA/                           # Imágenes y logo
├── server/                         # Servidor Flask
│   ├── app.py                      # Aplicación principal
│   ├── usuarios.db                 # Base de datos (se crea automáticamente)
│   ├── requirements.txt            # Dependencias Python
│   ├── start.bat                   # Iniciar en Windows
│   ├── start.sh                    # Iniciar en Linux/Mac
│   ├── setup.bat                   # Instalación en Windows
│   ├── setup.sh                    # Instalación en Linux/Mac
│   ├── README.md                   # Documentación del servidor
│   └── INSTRUCCIONES.md            # Instrucciones detalladas
└── README.md                       # Este archivo
```

## 🚀 Inicio Rápido

### 1. Instalar y Ejecutar el Servidor

**Windows:**
```bash
cd server
start.bat
```

**Linux/Mac:**
```bash
cd server
chmod +x start.sh
./start.sh
```

El servidor estará disponible en: `http://localhost:5000`

### 2. Abrir el Sitio Web

Simplemente abre `index.html` en tu navegador.

## ✨ Características

### Frontend
- ✅ Interfaz moderna y responsive
- ✅ Login y registro con validación en tiempo real
- ✅ Indicadores visuales de validación
- ✅ Spinner de carga durante peticiones
- ✅ Manejo de errores amigable
- ✅ Sesiones almacenadas localmente
- ✅ Animaciones suaves

### Backend
- ✅ API REST con Flask
- ✅ Base de datos SQLite
- ✅ Contraseñas hasheadas
- ✅ Sistema de tokens de sesión
- ✅ CORS habilitado
- ✅ Logs de acceso
- ✅ Validación de datos
- ✅ Protección contra inyección SQL

## 📱 Flujo de Uso

### Registro
1. Usuario accede a `/registro.html`
2. Completa el formulario con validación en tiempo real
3. El servidor valida y guarda el usuario
4. Se redirige automáticamente a login

### Login
1. Usuario accede a `/login.html`
2. Ingresa usuario y contraseña
3. El servidor verifica credenciales
4. Se genera un token de sesión
5. Se guarda el token localmente
6. Se redirige a la página principal

### Sesión Activa
- El token se guarda en `localStorage`
- Se envía en cada petición al servidor
- Expira después de 7 días
- El usuario puede cerrar sesión en cualquier momento

## 🔧 Configuración

### Cambiar URL del Servidor

Abrir `js/config.js`:

```javascript
// Desarrollo local
CONFIG.ENVIRONMENT = "development";
// O
CONFIG.SERVERS.development = "http://localhost:5000";

// Producción con ngrok
CONFIG.ENVIRONMENT = "production";
CONFIG.SERVERS.production = "https://tu-url.ngrok-free.dev";
```

### Variables del Servidor

En `server/app.py`:

```python
# Cambiar puerto
app.run(port=5001)

# Cambiar de debug a producción
app.run(debug=False)

# Cambiar contraseña secreta
app.config['SECRET_KEY'] = 'tu-clave-super-secreta'
```

## 📊 Endpoints API

### POST /api/auth/register
Registrar nuevo usuario

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -d "username=juan&email=juan@example.com&password=Pass123&confirm_password=Pass123"
```

### POST /api/auth/login
Iniciar sesión

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -d "username=juan&password=Pass123"
```

### GET /api/auth/verify
Verificar token

```bash
curl -H "Authorization: Bearer TOKEN" http://localhost:5000/api/auth/verify
```

### GET /api/auth/profile
Obtener perfil del usuario

```bash
curl -H "Authorization: Bearer TOKEN" http://localhost:5000/api/auth/profile
```

### POST /api/auth/logout
Cerrar sesión

```bash
curl -X POST -H "Authorization: Bearer TOKEN" http://localhost:5000/api/auth/logout
```

### GET /api/health
Verificar estado del servidor

```bash
curl http://localhost:5000/api/health
```

## 🔐 Seguridad

- Contraseñas hasheadas con PBKDF2
- Tokens únicos por sesión
- CORS restringido
- Validación en cliente y servidor
- Logs de acceso
- Protección contra inyección SQL

## 📝 Validaciones

### Usuario
- Mínimo 3 caracteres
- Máximo 20 caracteres
- Único en la base de datos

### Email
- Formato válido
- Único en la base de datos

### Contraseña
- Mínimo 6 caracteres
- Debe contener letras
- Debe contener números
- Coincidir con confirmación

## 🛠️ Troubleshooting

### Puerto 5000 en uso
```bash
# Cambiar puerto en app.py
app.run(port=5001)

# Luego actualizar en config.js
CONFIG.SERVERS.development = "http://localhost:5001";
```

### Error: "No module named 'flask'"
```bash
cd server
pip install -r requirements.txt
```

### CORS bloqueado
- Asegúrate que Flask-CORS está instalado
- Verifica que el servidor está corriendo
- Revisa la consola del navegador para más detalles

### Base de datos bloqueada
- Cierra todas las conexiones al servidor
- Elimina `server/usuarios.db`
- Reinicia el servidor (se creará una nueva base de datos)

## 📚 Recursos

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/)
- [Bootstrap 5](https://getbootstrap.com/)
- [JavaScript Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

## 📄 Licencia

© 2024 TecnicoAngeles - Todos los derechos reservados

## 👨‍💼 Contacto

**Técnico:** Ángel A.R.M  
**Teléfono:** 3175702147 o 3217633207  
**Empresa:** TécnicoAngeles  
**Lema:** "Tu equipo queda funcionando correctamente para el mejor rendimiento"

---

**Última actualización:** Mayo 31, 2024
