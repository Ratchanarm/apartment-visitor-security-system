import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth
export const authAPI = {
  login: (email, password) => 
    api.post('/auth/login', new URLSearchParams({ username: email, password }), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }),
  register: (data) => api.post('/auth/register', data),
  getMe: () => api.get('/auth/me'),
};

// Visitors
export const visitorAPI = {
  create: (data) => api.post('/visitors/', data),
  getAll: (params) => api.get('/visitors/', { params }),
  getActive: () => api.get('/visitors/active'),
  getById: (id) => api.get(`/visitors/${id}`),
  checkIn: (data) => api.post('/visitors/check-in', data),
  checkOut: (id) => api.post(`/visitors/${id}/check-out`),
  resendOTP: (id) => api.post(`/visitors/${id}/resend-otp`),
};

// Deliveries
export const deliveryAPI = {
  create: (data) => api.post('/deliveries/', data),
  getAll: (params) => api.get('/deliveries/', { params }),
  getPending: () => api.get('/deliveries/pending'),
  update: (id, data) => api.patch(`/deliveries/${id}`, data),
};

// Emergency
export const emergencyAPI = {
  create: (data) => api.post('/emergency/', data),
  getAll: (activeOnly = true) => api.get('/emergency/', { params: { active_only: activeOnly } }),
  resolve: (id) => api.post(`/emergency/${id}/resolve`),
};

// Apartments
export const apartmentAPI = {
  getAll: () => api.get('/apartments/'),
  getById: (id) => api.get(`/apartments/${id}`),
  create: (data) => api.post('/apartments/', data),
  addResident: (apartmentId, data) => api.post(`/apartments/${apartmentId}/residents`, data),
};

export default api;
