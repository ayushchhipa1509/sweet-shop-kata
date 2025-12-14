import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface User {
  id: number;
  username: string;
  email: string;
  role: string;
}

export interface Sweet {
  id: number;
  name: string;
  category: string;
  price: number;
  quantity: number;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export const authAPI = {
  register: async (
    username: string,
    email: string,
    password: string
  ): Promise<User> => {
    const response = await api.post("/auth/register", {
      username,
      email,
      password,
    });
    return response.data;
  },

  login: async (username: string, password: string): Promise<LoginResponse> => {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);
    const response = await api.post("/auth/login", formData, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    return response.data;
  },

  getMe: async (): Promise<User> => {
    const response = await api.get("/auth/me");
    return response.data;
  },
};

export const sweetsAPI = {
  getAll: async (): Promise<Sweet[]> => {
    const response = await api.get("/sweets");
    return response.data;
  },

  create: async (sweet: Omit<Sweet, "id">): Promise<Sweet> => {
    const response = await api.post("/sweets", sweet);
    return response.data;
  },

  purchase: async (id: number): Promise<Sweet> => {
    const response = await api.post(`/sweets/${id}/purchase`);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/sweets/${id}`);
  },
};

export default api;
