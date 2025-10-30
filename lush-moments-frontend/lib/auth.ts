import { apiClient } from "./api-client";

// Types
export interface User {
  id: number;
  name: string;
  email: string;
  phone?: string;
  role: string;
  auth_provider: string;
  avatar_url?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface RegisterData {
  name: string;
  email: string;
  password: string;
  phone?: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface OAuthData {
  provider: "google" | "github";
  oauth_id: string;
  email: string;
  name: string;
  avatar_url?: string;
}

// Auth API
export const authApi = {
  register: async (data: RegisterData): Promise<AuthResponse> => {
    // Get chat session ID if exists
    const sessionId =
      typeof window !== "undefined"
        ? localStorage.getItem("lush-moments-chat-session")
        : null;

    const response = await apiClient.post<AuthResponse>(
      "/auth/register",
      {
        ...data,
        session_id: sessionId,
      },
      false
    );
    apiClient.setToken(response.access_token);
    if (typeof window !== "undefined") {
      localStorage.setItem("user", JSON.stringify(response.user));
    }
    return response;
  },

  login: async (data: LoginData): Promise<AuthResponse> => {
    // Get chat session ID if exists
    const sessionId =
      typeof window !== "undefined"
        ? localStorage.getItem("lush-moments-chat-session")
        : null;

    const response = await apiClient.post<AuthResponse>(
      "/auth/login",
      {
        ...data,
        session_id: sessionId,
      },
      false
    );
    apiClient.setToken(response.access_token);
    if (typeof window !== "undefined") {
      localStorage.setItem("user", JSON.stringify(response.user));
    }
    return response;
  },

  oauthCallback: async (data: OAuthData): Promise<AuthResponse> => {
    // Get chat session ID if exists
    const sessionId =
      typeof window !== "undefined"
        ? localStorage.getItem("lush-moments-chat-session")
        : null;

    const response = await apiClient.post<AuthResponse>(
      "/auth/oauth/callback",
      {
        ...data,
        session_id: sessionId,
      },
      false
    );
    apiClient.setToken(response.access_token);
    if (typeof window !== "undefined") {
      localStorage.setItem("user", JSON.stringify(response.user));
    }
    return response;
  },

  logout: () => {
    apiClient.removeToken();
  },

  getCurrentUser: (): User | null => {
    if (typeof window !== "undefined") {
      const userStr = localStorage.getItem("user");
      if (userStr) {
        try {
          return JSON.parse(userStr);
        } catch {
          return null;
        }
      }
    }
    return null;
  },

  isAuthenticated: (): boolean => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("auth_token");
      return !!token;
    }
    return false;
  },
};
