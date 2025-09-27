// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8001',
  TIMEOUT: parseInt(process.env.REACT_APP_API_TIMEOUT || '10000'),
  ENDPOINTS: {
    HEALTH: '/health',
    BLOG_POSTS: '/api/blog-posts',
    KNOWLEDGE_VAULTS: '/api/knowledge-vaults',
    USERS: '/api/users',
  },
};

// API Client utility
export class ApiClient {
  private baseUrl: string;
  private timeout: number;

  constructor(
    baseUrl: string = API_CONFIG.BASE_URL,
    timeout: number = API_CONFIG.TIMEOUT,
  ) {
    this.baseUrl = baseUrl;
    this.timeout = timeout;
  }

  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...defaultOptions,
        ...options,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(
          `API request failed: ${response.status} ${response.statusText}`,
        );
      }

      return response.json();
    } catch (error) {
      clearTimeout(timeoutId);

      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          throw new Error('Request timeout');
        }
        if (error.message.includes('Failed to fetch')) {
          throw new Error('Network error: Unable to connect to backend server');
        }
      }

      throw error;
    }
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async put<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

// Default API client instance
export const apiClient = new ApiClient();
