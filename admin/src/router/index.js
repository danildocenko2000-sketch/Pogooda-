import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '../api'
import LoginView from '../views/LoginView.vue'
import ProductsView from '../views/ProductsView.vue'
import ProductFormView from '../views/ProductFormView.vue'
import SettingsView from '../views/SettingsView.vue'

const routes = [
  { path: '/login', name: 'login', component: LoginView, meta: { public: true } },
  { path: '/', redirect: '/products' },
  { path: '/products', name: 'products', component: ProductsView },
  { path: '/products/new', name: 'product-new', component: ProductFormView },
  { path: '/products/:id', name: 'product-edit', component: ProductFormView, props: true },
  { path: '/settings', name: 'settings', component: SettingsView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const token = getToken()
  if (!to.meta.public && !token) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
