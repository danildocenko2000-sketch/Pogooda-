<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getProducts, deleteProduct } from '../api'

const router = useRouter()
const products = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    products.value = await getProducts()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

async function remove(id, name) {
  if (!confirm(`Видалити товар «${name}»?`)) return
  try {
    await deleteProduct(id)
    products.value = products.value.filter((p) => p.id !== id)
  } catch (e) {
    alert(e.message)
  }
}

function toEdit(id) {
  router.push({ name: 'product-edit', params: { id } })
}
</script>

<template>
  <div class="page">
    <div class="top">
      <h1>Товари</h1>
      <router-link to="/products/new" class="btn btn-primary">+ Додати товар</router-link>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <div v-else-if="loading" class="loading">Завантаження...</div>
    <div v-else class="table-wrap">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Назва</th>
            <th>Категорія</th>
            <th>Ціна</th>
            <th>В наявності</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in products" :key="p.id">
            <td>{{ p.id }}</td>
            <td>
              <button type="button" class="link" @click="toEdit(p.id)">{{ p.name }}</button>
            </td>
            <td>{{ p.category }} / {{ p.subcategory }}</td>
            <td>{{ p.price }} грн</td>
            <td>{{ p.in_stock ? 'Так' : 'Ні' }}</td>
            <td>
              <button type="button" class="btn btn-sm btn-danger" @click="remove(p.id, p.name)">Видалити</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="products.length === 0" class="empty">Товарів немає</p>
    </div>
  </div>
</template>

<style scoped>
.page { padding: 1rem 1.5rem; }
.top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.top h1 { margin: 0; color: #f1f5f9; font-size: 1.5rem; }
.error { color: #f87171; }
.loading { color: #94a3b8; }
.table-wrap { overflow-x: auto; }
.table {
  width: 100%;
  border-collapse: collapse;
  background: #334155;
  border-radius: 8px;
  overflow: hidden;
}
.table th, .table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #475569;
}
.table th { background: #1e293b; color: #94a3b8; font-weight: 600; }
.table td { color: #e2e8f0; }
.link {
  background: none;
  border: none;
  color: #60a5fa;
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
}
.link:hover { color: #93c5fd; }
.btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  text-decoration: none;
  border: none;
  cursor: pointer;
}
.btn-primary { background: #3b82f6; color: white; }
.btn-primary:hover { background: #2563eb; }
.btn-sm { padding: 0.35rem 0.65rem; font-size: 0.875rem; }
.btn-danger { background: #dc2626; color: white; }
.btn-danger:hover { background: #b91c1c; }
.empty { color: #94a3b8; padding: 1rem; }
</style>
