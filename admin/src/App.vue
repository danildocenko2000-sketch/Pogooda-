<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { logout, getToken } from './api'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoggedIn = () => !!getToken()

function onLogout() {
  logout()
  router.push('/login')
}
</script>

<template>
  <div class="app">
    <nav v-if="isLoggedIn()" class="nav">
      <router-link to="/products">Товари</router-link>
      <router-link to="/settings">Налаштування</router-link>
      <button type="button" class="nav-btn" @click="onLogout">Вийти</button>
    </nav>
    <main class="main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app { min-height: 100vh; background: #0f172a; }
.nav {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1.5rem;
  background: #1e293b;
  border-bottom: 1px solid #334155;
}
.nav a {
  color: #94a3b8;
  text-decoration: none;
}
.nav a:hover, .nav a.router-link-active { color: #f1f5f9; }
.nav-btn {
  margin-left: auto;
  padding: 0.4rem 0.75rem;
  background: transparent;
  border: 1px solid #475569;
  color: #94a3b8;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
}
.nav-btn:hover { background: #334155; color: #f1f5f9; }
.main { padding: 0; }
</style>
