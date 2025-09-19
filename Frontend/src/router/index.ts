import { createRouter, createWebHistory } from 'vue-router';
import ProductView from '../views/ProductView.vue';

const routes = [
  { path: '/', component: ProductView }
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
