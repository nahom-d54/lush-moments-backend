// API Configuration
export const API_URL =
  (typeof window !== "undefined"
    ? (window as any).ENV?.NEXT_PUBLIC_API_URL
    : undefined) || "http://localhost:8000";

// API Client with authentication
class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private getHeaders(includeAuth = true): HeadersInit {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };

    if (includeAuth) {
      const token = this.getToken();
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }
    }

    return headers;
  }

  private getToken(): string | null {
    if (typeof window !== "undefined") {
      return localStorage.getItem("auth_token");
    }
    return null;
  }

  setToken(token: string) {
    if (typeof window !== "undefined") {
      localStorage.setItem("auth_token", token);
    }
  }

  removeToken() {
    if (typeof window !== "undefined") {
      localStorage.removeItem("auth_token");
      localStorage.removeItem("user");
    }
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {},
    includeAuth = true
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const headers = this.getHeaders(includeAuth);

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          ...headers,
          ...options.headers,
        },
      });

      if (response.status === 401) {
        // Token expired or invalid
        this.removeToken();
        if (typeof window !== "undefined") {
          window.location.href = "/login?redirect=" + window.location.pathname;
        }
        throw new Error("Unauthorized");
      }

      if (!response.ok) {
        const error = await response
          .json()
          .catch(() => ({ detail: "An error occurred" }));
        throw new Error(error.detail || "An error occurred");
      }

      return await response.json();
    } catch (error) {
      console.error("API Error:", error);
      throw error;
    }
  }

  // GET request
  async get<T>(endpoint: string, includeAuth = true): Promise<T> {
    return this.request<T>(endpoint, { method: "GET" }, includeAuth);
  }

  // POST request
  async post<T>(endpoint: string, data?: any, includeAuth = true): Promise<T> {
    return this.request<T>(
      endpoint,
      {
        method: "POST",
        body: data ? JSON.stringify(data) : undefined,
      },
      includeAuth
    );
  }

  // PATCH request
  async patch<T>(endpoint: string, data?: any, includeAuth = true): Promise<T> {
    return this.request<T>(
      endpoint,
      {
        method: "PATCH",
        body: data ? JSON.stringify(data) : undefined,
      },
      includeAuth
    );
  }

  // PUT request
  async put<T>(endpoint: string, data?: any, includeAuth = true): Promise<T> {
    return this.request<T>(
      endpoint,
      {
        method: "PUT",
        body: data ? JSON.stringify(data) : undefined,
      },
      includeAuth
    );
  }

  // DELETE request
  async delete<T>(endpoint: string, includeAuth = true): Promise<T> {
    return this.request<T>(endpoint, { method: "DELETE" }, includeAuth);
  }
}

export const apiClient = new ApiClient(API_URL);
