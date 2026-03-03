<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { login, setToken } from '../api'

const router = useRouter()
const route = useRoute()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function onSubmit() {
  error.value = ''
  if (!username.value.trim() || !password.value) {
    error.value = 'Введіть логін та пароль'
    return
  }
  loading.value = true
  try {
    await login(username.value.trim(), password.value)
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (e) {
    error.value = e.message || 'Помилка входу'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-card">
      <h1>Вхід в адмінку</h1>
      <p class="subtitle">WORLD OF Santehnika</p>
      <form @submit.prevent="onSubmit">
        <div class="field">
          <label>Логін</label>
          <input v-model="username" type="text" autocomplete="username" />
        </div>
        <div class="field">
          <label>Пароль</label>
          <input v-model="password" type="password" autocomplete="current-password" />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" :disabled="loading">Увійти</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1e293b;
}
.login-card {
  background: #334155;
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 360px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}
.login-card h1 {
  margin: 0 0 0.25rem 0;
  color: #f1f5f9;
  font-size: 1.5rem;
}
.subtitle {
  color: #94a3b8;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}
.field {
  margin-bottom: 1rem;
}
.field label {
  display: block;
  color: #cbd5e1;
  font-size: 0.875rem;
  margin-bottom: 0.35rem;
}
.field input {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 1px solid #475569;
  border-radius: 8px;
  background: #1e293b;
  color: #f1f5f9;
  box-sizing: border-box;
}
.field input:focus {
  outline: none;
  border-color: #3b82f6;
}
.error {
  color: #f87171;
  font-size: 0.875rem;
  margin-bottom: 0.75rem;
}
button {
  width: 100%;
  padding: 0.75rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}
button:hover:not(:disabled) {
  background: #2563eb;
}
button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
