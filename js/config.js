/**
 * Archivo de Configuración Central
 * TecnicoAngeles
 * 
 * Cambiar aquí la URL del servidor según el entorno
 */

const CONFIG = {
    // ========== AMBIENTE DE DESARROLLO ==========
    // Usar "development" para desarrollo local
    // Usar "production" para producción
    ENVIRONMENT: "development",
    
    // ========== URLS DEL SERVIDOR ==========
    SERVERS: {
        // Servidor local (desarrollo)
        development: "http://localhost:5000",
        
        // Servidor con ngrok (acceso público)
        production: "https://tu-url-ngrok.ngrok-free.dev"
    },
    
    // ========== CONFIGURACIÓN DE LA APP ==========
    APP_NAME: "TecnicoAngeles",
    APP_VERSION: "1.0.0",
    
    // Timeout para peticiones (en milisegundos)
    TIMEOUT: 10000,
    
    // Clave de almacenamiento local
    STORAGE_KEY: "tecnico_angel_auth",
    
    // ========== RUTAS ==========
    ROUTES: {
        HOME: "index.html",
        LOGIN: "login.html",
        REGISTER: "registro.html"
    },
    
    // ========== VALIDACIÓN ==========
    VALIDATION: {
        USERNAME_MIN: 3,
        USERNAME_MAX: 20,
        PASSWORD_MIN: 6,
        PASSWORD_PATTERN: /^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z0-9]{6,}$/
    },
    
    // ========== MÉTODOS AUXILIARES ==========
    
    /**
     * Obtiene la URL del servidor según el ambiente
     */
    getServerUrl() {
        return this.SERVERS[this.ENVIRONMENT] || this.SERVERS.development;
    },
    
    /**
     * Obtiene la URL completa de un endpoint
     */
    getEndpointUrl(endpoint) {
        return this.getServerUrl() + endpoint;
    },
    
    /**
     * Valida si el email es correcto
     */
    isValidEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    },
    
    /**
     * Valida si la contraseña cumple requisitos
     */
    isValidPassword(password) {
        return password.length >= this.VALIDATION.PASSWORD_MIN &&
               /[a-zA-Z]/.test(password) &&
               /\d/.test(password);
    }
};

// Exportar para uso en otros archivos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
