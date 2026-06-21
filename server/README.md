# Servidor Backend - TecnicoAngeles

Servidor Flask para autenticación y gestión de usuarios.

## Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
# Ejecutar servidor
python app.py
```

El servidor se ejecutará en `http://localhost:5000`

## Con ngrok (para exponer públicamente)

```bash
# En otra terminal
ngrok http 5000
```

## Endpoints

### Registro
- **POST** `/api/auth/register`
- Parámetros: `username`, `email`, `password`, `confirm_password`

### Login
- **POST** `/api/auth/login`
- Parámetros: `username`, `password`
- Retorna: `token`, `username`

### Logout
- **POST** `/api/auth/logout`
- Headers: `Authorization: Bearer {token}`

### Verificar Token
- **GET** `/api/auth/verify`
- Headers: `Authorization: Bearer {token}`

### Obtener Perfil
- **GET** `/api/auth/profile`
- Headers: `Authorization: Bearer {token}`

### Health Check
- **GET** `/api/health`

## Base de Datos

SQLite - archivo `usuarios.db` en la carpeta del servidor

Tablas:
- `usuarios` - Registro de usuarios
- `sesiones` - Sesiones activas
- `logs_acceso` - Registro de accesos

## Seguridad

- Contraseñas hasheadas con PBKDF2
- Tokens de sesión únicos
- CORS habilitado para múltiples orígenes
- Validación de email y contraseña
- Logs de acceso registrados
