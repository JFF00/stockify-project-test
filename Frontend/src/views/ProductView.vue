<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getProducts, createProduct, deleteProduct } from '../services/productService';

interface Product {
  id_product?: number;     // 👈 viene así del backend
  name: string;
  description: string;
  stock: number;
  unit_price: number;
  created_at?: string;     // lo rellena el backend
  id_category?: number | null; // ahora opcional
}

const products = ref<Product[]>([]);
const newProduct = ref<Product>({
  name: '',
  description: '',
  stock: 0,
  unit_price: 0,
});

const message = ref<string | null>(null);
const error = ref<string | null>(null);

const fetchProducts = async () => {
  try {
    const res = await getProducts();
    products.value = res.data;
  } catch (err) {
    error.value = "Error cargando productos.";
  }
};

const addProduct = async () => {
  try {
    // Enviamos solo los campos que ahora son requeridos
    const payload = {
      name: newProduct.value.name,
      description: newProduct.value.description,
      stock: newProduct.value.stock,
      unit_price: newProduct.value.unit_price,
      // id_category: undefined  // si quieres forzar no enviar nada
    };
    await createProduct(payload);
    message.value = "✅ Producto agregado correctamente.";
    error.value = null;

    newProduct.value = { name: '', description: '', stock: 0, unit_price: 0 };
    fetchProducts();
    setTimeout(() => { message.value = null }, 3000);
  } catch (err: any) {
    if (err.response) {
      error.value = "❌ " + JSON.stringify(err.response.data);
    } else {
      error.value = "❌ Hubo un error al agregar el producto.";
    }
    message.value = null;
  }
};

const removeProduct = async (id: number) => {
  try {
    await deleteProduct(id);
    message.value = "🗑️ Producto eliminado.";
    error.value = null;
    fetchProducts();
    setTimeout(() => { message.value = null }, 3000);
  } catch (err) {
    error.value = "❌ Error al eliminar el producto.";
  }
};

onMounted(fetchProducts);
</script>

<template>
  <div class="max-w-3xl mx-auto p-6">
    <h2 class="text-2xl font-bold mb-4">📦 Gestión de Productos</h2>

    <div v-if="message" class="mb-4 p-2 bg-green-100 text-green-800 rounded">
      {{ message }}
    </div>
    <div v-if="error" class="mb-4 p-2 bg-red-100 text-red-800 rounded">
      {{ error }}
    </div>

    <form @submit.prevent="addProduct" class="form-grid mb-6">
    <!-- Nombre (izquierda) -->
    <div class="field">
        <label>Nombre</label>
        <input v-model="newProduct.name" placeholder="Ej: Producto A" required />
    </div>

    <!-- Descripción (derecha) -->
    <div class="field">
        <label>Descripción</label>
        <textarea v-model="newProduct.description"
                placeholder="Escribe una descripción..."
                rows="4" required></textarea>
    </div>

    <!-- Stock (izquierda fila 2) -->
    <div class="field">
        <label>Stock</label>
        <input v-model.number="newProduct.stock" type="number" placeholder="Cantidad disponible" required />
    </div>

    <!-- Precio (derecha fila 2) -->
    <div class="field">
        <label>Precio Unitario</label>
        <input v-model.number="newProduct.unit_price" type="number" step="0.01" placeholder="Precio" required />
    </div>

    <!-- Botón (ocupa las dos columnas) -->
    <div class="actions">
        <button type="submit">➕ Agregar Producto</button>
    </div>
    </form>



    <table class="w-full border-collapse border border-gray-300">
      <thead class="bg-gray-100">
        <tr>
          <th class="border p-2">ID</th>
          <th class="border p-2">Nombre</th>
          <th class="border p-2">Descripción</th>
          <th class="border p-2">Stock</th>
          <th class="border p-2">Precio</th>
          <th class="border p-2">Fecha</th>
          <th class="border p-2">Categoría</th>
          <th class="border p-2">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in products" :key="p.id_product" class="hover:bg-gray-50">
          <td class="border p-2">{{ p.id_product }}</td>
          <td class="border p-2">{{ p.name }}</td>
          <td class="border p-2">{{ p.description }}</td>
          <td class="border p-2">{{ p.stock }}</td>
          <td class="border p-2">${{ p.unit_price }}</td>
          <td class="border p-2">{{ p.created_at }}</td>
          <td class="border p-2">{{ p.id_category ?? '-' }}</td>
          <td class="border p-2 text-center">
            <button @click="removeProduct(p.id_product!)"
                    class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded">
              Eliminar
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
