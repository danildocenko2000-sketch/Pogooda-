<script setup>
import { ref, onMounted } from 'vue'
import { getSettings, patchSettings } from '../api'

const form = ref({
  store_name: '',
  phone: '',
  hero_title: '',
  hero_subtitle: '',
})
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const message = ref('')

onMounted(async () => {
  try {
    const s = await getSettings()
    form.value = { ...s }
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

async function onSubmit() {
  message.value = ''
  saving.value = true
  try {
    await patchSettings(form.value)
    message.value = 'Збережено'
  } catch (e) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="page">
    <h1>Налаштування сайту</h1>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="message" class="message">{{ message }}</p>
    <div v-if="loading" class="loading">Завантаження...</div>
    <form v-else @submit.prevent="onSubmit" class="form">
      <div class="field">
        <label>Назва магазину</label>
        <input v-model="form.store_name" type="text" />
      </div>
      <div class="field">
        <label>Телефон</label>
        <input v-model="form.phone" type="text" />
      </div>
      <div class="field">
        <label>Заголовок hero</label>
        <input v-model="form.hero_title" type="text" />
      </div>
      <div class="field">
        <label>Підзаголовок hero</label>
        <textarea v-model="form.hero_subtitle" rows="3"></textarea>
      </div>
      <button type="submit" :disabled="saving">Зберегти</button>
    </form>
  </div>
</template>

<style scoped>
.page { padding: 1rem 1.5rem; max-width: 560px; }
.page h1 { margin: 0 0 1rem 0; color: #f1f5f9; font-size: 1.5rem; }
.error { color: #f87171; }
.message { color: #4ade80; }
.loading { color: #94a3b8; }
.form .field { margin-bottom: 1rem; }
.form label { display: block; color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.25rem; }
.form input, .form textarea {
  width: 100%;
  padding: 0.5rem 0.6rem;
  border: 1px solid #475569;
  border-radius: 6px;
  background: #1e293b;
  color: #f1f5f9;
  box-sizing: border-box;
}
.form textarea { resize: vertical; }
.form button {
  padding: 0.6rem 1.2rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
}
.form button:hover:not(:disabled) { background: #2563eb; }
.form button:disabled { opacity: 0.7; }
</style>
