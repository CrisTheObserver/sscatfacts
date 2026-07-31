const API_URL = "http://127.0.0.1:8000/api";

async function apiCall(endpoint, options = {}) {
    const token = getAccessToken();
    const headers = {
        ...(options.headers || {}),
    };
    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }
    try {
        const response = await fetch(
            `${API_URL}${endpoint}`,
            {
                ...options,
                headers,
            },
        );
        const data = await response.json();
        return {
            ok: response.ok,
            status: response.status,
            data,
        };
    } catch {
        return {
            ok: false,
            status: 0,
            data: {
                detail: "Unable to connect to the server.",
            },
        };
    }
}