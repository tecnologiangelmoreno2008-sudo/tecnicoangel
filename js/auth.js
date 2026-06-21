/**
 * Módulo de Autenticación - TecnicoAngeles
 * Maneja login, registro y gestión de sesiones con servidor
 */

// Configuración de la API
const API_CONFIG = {
    // IMPORTANTE: Cambiar la URL según tu entorno
    // Para desarrollo local: http://localhost:5000
    // Para producción con ngrok: https://tu-url.ngrok-free.dev
    get BASE_URL() {
        return (typeof CONFIG !== 'undefined') ? CONFIG.getServerUrl() : "http://localhost:5000";
    },
    ENDPOINTS: {
        LOGIN: "/api/auth/login",
        REGISTER: "/api/auth/register",
        LOGOUT: "/api/auth/logout",
        VERIFY: "/api/auth/verify",
        PROFILE: "/api/auth/profile"
    },
    TIMEOUT: 10000, // 10 segundos
    STORAGE_KEY: "tecnico_angel_auth"
};

/**
 * Clase para manejar la autenticación
 */
class AuthService {
    constructor() {
        this.token = this.getStoredToken();
        this.user = this.getStoredUser();
    }

    /**
     * Realiza login en el servidor
     */
    async login(username, password) {
        try {
            if (!username?.trim() || !password) {
                return { ok: false, message: "Usuario y contraseña son requeridos" };
            }

            if (password.length < 3) {
                return { ok: false, message: "Contraseña muy corta" };
            }

            const response = await this.fetchWithTimeout(
                API_CONFIG.BASE_URL + API_CONFIG.ENDPOINTS.LOGIN,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: new URLSearchParams({ username, password })
                }
            );

            const data = await response.text();

            if (response.ok) {
                // Guardar token y datos del usuario
                this.setSession({ username, token: data });
                return { ok: true, message: "Sesión iniciada correctamente" };
            } else {
                return { ok: false, message: data || "Error al iniciar sesión" };
            }
        } catch (error) {
            console.error("Error en login:", error);
            return { ok: false, message: this.getErrorMessage(error) };
        }
    }

    /**
     * Realiza registro de nuevo usuario
     */
    async register(username, email, password, confirm_password) {
        try {
            // Validaciones
            if (!username?.trim() || !email?.trim() || !password || !confirm_password) {
                return { ok: false, message: "Todos los campos son requeridos" };
            }

            if (password !== confirm_password) {
                return { ok: false, message: "Las contraseñas no coinciden" };
            }

            if (password.length < 6) {
                return { ok: false, message: "La contraseña debe tener al menos 6 caracteres" };
            }

            if (!this.isValidEmail(email)) {
                return { ok: false, message: "Correo electrónico no válido" };
            }

            const response = await this.fetchWithTimeout(
                API_CONFIG.BASE_URL + API_CONFIG.ENDPOINTS.REGISTER,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: new URLSearchParams({
                        username,
                        email,
                        password,
                        confirm_password
                    })
                }
            );

            const data = await response.text();

            if (response.ok) {
                return { ok: true, message: "Registro exitoso. Puedes iniciar sesión ahora." };
            } else {
                return { ok: false, message: data || "Error al registrar usuario" };
            }
        } catch (error) {
            console.error("Error en registro:", error);
            return { ok: false, message: this.getErrorMessage(error) };
        }
    }

    /**
     * Cierra la sesión del usuario
     */
    logout() {
        this.clearSession();
        return { ok: true, message: "Sesión cerrada correctamente" };
    }

    /**
     * Verifica si el usuario está autenticado
     */
    isAuthenticated() {
        return !!this.token && !!this.user;
    }

    /**
     * Obtiene el usuario actual
     */
    getCurrentUser() {
        return this.user || null;
    }

    /**
     * Obtiene el token de autenticación
     */
    getToken() {
        return this.token || null;
    }

    /**
     * Guarda los datos de sesión en localStorage
     */
    setSession(data) {
        this.token = data.token;
        this.user = { username: data.username };
        localStorage.setItem(API_CONFIG.STORAGE_KEY, JSON.stringify({
            token: this.token,
            user: this.user,
            timestamp: Date.now()
        }));
    }

    /**
     * Obtiene el token guardado de localStorage
     */
    getStoredToken() {
        try {
            const data = JSON.parse(localStorage.getItem(API_CONFIG.STORAGE_KEY));
            return data?.token || null;
        } catch {
            return null;
        }
    }

    /**
     * Obtiene el usuario guardado de localStorage
     */
    getStoredUser() {
        try {
            const data = JSON.parse(localStorage.getItem(API_CONFIG.STORAGE_KEY));
            return data?.user || null;
        } catch {
            return null;
        }
    }

    /**
     * Limpia los datos de sesión
     */
    clearSession() {
        this.token = null;
        this.user = null;
        localStorage.removeItem(API_CONFIG.STORAGE_KEY);
    }

    /**
     * Fetch con timeout
     */
    async fetchWithTimeout(url, options = {}) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.TIMEOUT);

        try {
            const response = await fetch(url, {
                ...options,
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            return response;
        } catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }

    /**
     * Valida formato de email
     */
    isValidEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

    /**
     * Obtiene mensaje de error legible
     */
    getErrorMessage(error) {
        if (error.name === "AbortError") {
            return "Tiempo de conexión agotado. Intenta de nuevo.";
        }
        if (error instanceof TypeError && error.message.includes("fetch")) {
            return "Error de conexión con el servidor. Verifica tu conexión a internet.";
        }
        return error.message || "Error desconocido";
    }
}

// Crear instancia global
const authService = new AuthService();

/**
 * Funciones de compatibilidad con el código antiguo
 */
async function loginUser({ username, password }) {
    return await authService.login(username, password);
}

async function registerUser({ username, email, password, confirm_password }) {
    return await authService.register(username, email, password, confirm_password);
}

function logoutUser() {
    return authService.logout();
}
