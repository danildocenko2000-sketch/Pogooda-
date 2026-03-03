<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getProduct, createProduct, updateProduct } from '../api'

const router = useRouter()
const route = useRoute()
const id = computed(() => route.params.id)
const isNew = computed(() => !id.value || id.value === 'new')

const form = ref({
  name: '',
  category: 'other',
  subcategory: 'other',
  sub_subcategory: '',
  price: 0,
  oldPrice: null,
  image: '🚿',
  badge: '',
  description: '',
  in_stock: true,
  quantity: 0,
  sort_order: 0,
})
const loading = ref(false)
const loadError = ref('')
const submitError = ref('')

onMounted(async () => {
  if (isNew.value) return
  try {
    const p = await getProduct(id.value)
    form.value = {
      name: p.name,
      category: p.category || 'other',
      subcategory: p.subcategory || 'other',
      sub_subcategory: p.sub_subcategory || '',
      price: p.price ?? 0,
      oldPrice: p.oldPrice ?? null,
      image: p.image || '🚿',
      badge: p.badge || '',
      description: p.description || '',
      in_stock: p.in_stock !== false,
      quantity: p.quantity ?? 0,
      sort_order: p.sort_order ?? 0,
    }
  } catch (e) {
    loadError.value = e.message
  }
})

async function onSubmit() {
  submitError.value = ''
  if (!form.value.name.trim()) {
    submitError.value = 'Назва обов\'язкова'
    return
  }
  loading.value = true
  try {
    const payload = { ...form.value }
    if (payload.oldPrice === '' || payload.oldPrice == null) payload.oldPrice = null
    if (isNew.value) {
      await createProduct(payload)
      router.push({ name: 'products' })
    } else {
      await updateProduct(id.value, payload)
      router.push({ name: 'products' })
    }
  } catch (e) {
    submitError.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">
    <h1>{{ isNew ? 'Новий товар' : 'Редагувати товар' }}</h1>
    <p v-if="loadError" class="error">{{ loadError }}</p>
    <form v-else @submit.prevent="onSubmit" class="form">
      <div class="grid">
        <div class="field">
          <label>Назва *</label>
          <input v-model="form.name" type="text" required />
        </div>
        <div class="field">
          <label>Категорія</label>
          <input v-model="form.category" type="text" />
        </div>
        <div class="field">
          <label>Підкатегорія</label>
          <input v-model="form.subcategory" type="text" />
        </div>
        <div class="field">
          <label>Під-підкатегорія</label>
          <input v-model="form.sub_subcategory" type="text" />
        </div>
        <div class="field">
          <label>Ціна (грн)</label>
          <input v-model.number="form.price" type="number" min="0" />
        </div>
        <div class="field">
          <label>Стара ціна (грн)</label>
          <input v-model.number="form.oldPrice" type="number" min="0" placeholder="не вказано" />
        </div>
        <div class="field">
          <label>Зображення (emoji або URL)</label>
          <input v-model="form.image" type="text" />
        </div>
        <div class="field">
          <label>Бейдж</label>
          <input v-model="form.badge" type="text" placeholder="Хіт, Знижка..." />
        </div>
        <div class="field">
          <label>В наявності</label>
          <label class="checkbox">
            <input v-model="form.in_stock" type="checkbox" />
            Так
          </label>
        </div>
        <div class="field">
          <label>Кількість</label>
          <input v-model.number="form.quantity" type="number" min="0" />
        </div>
        <div class="field">
          <label>Порядок сортування</label>
          <input v-model.number="form.sort_order" type="number" min="0" />
        </div>
      </div>
      <div class="field full">
        <label>Опис</label>
        <textarea v-model="form.description" rows="4"></textarea>
      </div>
      <p v-if="submitError" class="error">{{ submitError }}</p>
      <div class="actions">
        <button type="submit" :disabled="loading">Зберегти</button>
        <router-link to="/products" class="btn btn-secondary">Скасувати</router-link>
      </div>
    </form>
  </div>
</template>

<style scoped>
.page { padding: 1rem 1.5rem; max-width: 720px; }
.page h1 { margin: 0 0 1rem 0; color: #f1f5f9; font-size: 1.5rem; }
.form .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.field { margin-bottom: 0.5rem; }
.field.full { grid-column: 1 / -1; }
.field label { display: block; color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.25rem; }
.field input, .field textarea {
  width: 100%;
  padding: 0.5rem 0.6rem;
  border: 1px solid #475569;
  border-radius: 6px;
  background: #1e293b;
  color: #f1f5f9;
  box-sizing: border-box;
}
.field textarea { resize: vertical; min-height: 80px; }
.checkbox { display: flex; align-items: center; gap: 0.5rem; cursor: pointer; }
.checkbox input { width: auto; }
.error { color: #f87171; margin-bottom: 0.5rem; }
.actions { display: flex; gap: 0.75rem; margin-top: 1rem; }
.actions button, .actions .btn {
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  text-decoration: none;
}
.actions button { background: #3b82f6; color: white; }
.actions button:hover:not(:disabled) { background: #2563eb; }
.actions button:disabled { opacity: 0.7; }
.btn-secondary { background: #475569; color: white; }
.btn-secondary:hover { background: #64748b; }
</style>
