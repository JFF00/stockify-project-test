import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, 
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  timeout: 10000,
 
});

export const getProducts  = () => api.get('/products/');
export const getProduct   = (id: number) => api.get(`/products/${id}/`);
export const createProduct = (data: any) => api.post('/products/', data);
export const updateProduct = (id: number, data: any) => api.put(`/products/${id}/`, data);
export const deleteProduct = (id: number) => api.delete(`/products/${id}/`);
