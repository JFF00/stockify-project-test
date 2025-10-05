import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, 
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  timeout: 10000,
 
});

// Productos con bajo stock
export const getLowStockProducts = (threshold: number = 5) =>
  api.get(`/products/low_stock/`);

// Productos más vendidos
export const getTopSoldProducts = (period: 'mes' | 'año' | 'todo' = 'todo') =>
  api.get(`/products/top_sold/?period=${period}`);