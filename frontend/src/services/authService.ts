/**
 * authService.ts — Autenticación contra Portfolio backend
 *
 * Responsabilidad: Login/logout con cookie httpOnly (sin localStorage).
 * El backend de Portfolio setea la cookie, el frontend solo la usa.
 * authCore es el Identity Provider central (RS256 + JWKS).
 */

// ── Config ───────────────────────────────────────────────────

const API_BASE = import.meta.env.PUBLIC_API_URL || 'http://localhost:8001';
const AUTH_API = `${API_BASE}/api/v1/auth`;

// ── Interfaces ──────────────────────────────────────────────

export interface LoginRequest {
  username: string;
  password: string;
}

export interface UserInfo {
  id: number;
  username: string;
  email: string;
  full_name: string;
  role: string;
  status: string;
  is_active: boolean;
}

export interface LoginResponse {
  user: UserInfo;
}

export interface AuthState {
  isLoading: boolean;
  error: string | null;
  user: UserInfo | null;
}

// ── Servicio ────────────────────────────────────────────────

class AuthService {
  /**
   * Login: envía credenciales al backend de Portfolio,
   * que las valida contra authCore y setea cookie httpOnly.
   */
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await fetch(`${AUTH_API}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
      credentials: 'include',
    });

    return this._handleResponse<LoginResponse>(response);
  }

  /**
   * Cierra sesión: llama al backend para limpiar la cookie.
   */
  async logout(): Promise<void> {
    await fetch(`${AUTH_API}/logout`, {
      method: 'POST',
      credentials: 'include',
    });
    window.location.href = '/login';
  }

  /**
   * Verifica la sesión contra el backend (lee la cookie httpOnly).
   * Retorna el usuario autenticado o null.
   */
  async isLoggedIn(): Promise<UserInfo | null> {
    try {
      const response = await fetch(`${AUTH_API}/me`, {
        credentials: 'include',
      });
      if (!response.ok) return null;
      return await response.json();
    } catch {
      return null;
    }
  }

  /**
   * Manejador de respuestas HTTP genérico.
   */
  private async _handleResponse<T>(response: Response): Promise<T> {
    const data = await response.json();

    if (!response.ok) {
      const message =
        typeof data.detail === 'string'
          ? data.detail
          : Array.isArray(data.detail)
            ? data.detail[0]?.msg
            : 'Error de autenticación';
      throw new Error(message);
    }

    return data as T;
  }
}

// Singleton
export const authService = new AuthService();
