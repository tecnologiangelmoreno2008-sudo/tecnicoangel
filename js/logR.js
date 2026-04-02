const NGROK_BASE_URL = "https://dodie-unarbitrative-maeve.ngrok-free.dev";
const AUTH_BASE_URL = NGROK_BASE_URL + "/api/auth";

async function registerUser({ username, email, password, confirm_password }) {
    try {
        const body = new URLSearchParams({
            username,
            email,
            password,
            confirm_password
        });

        const response = await fetch(AUTH_BASE_URL + "/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: body.toString()
        });

        const text = await response.text();
        return { ok: response.ok, status: response.status, message: text };
    } catch (error) {
        return { ok: false, status: 0, message: "Error de conexion con el backend" };
    }
}

async function loginUser({ username, password }) {
    try {
        const body = new URLSearchParams({ username, password });

        const response = await fetch(AUTH_BASE_URL + "/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: body.toString()
        });

        const text = await response.text();
        return { ok: response.ok, status: response.status, message: text };
    } catch (error) {
        return { ok: false, status: 0, message: "Error de conexion con el backend" };
    }
}