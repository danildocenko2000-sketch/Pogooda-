/**
 * API клієнт для Vue-адмінки. Базовий URL з VITE_API_URL (dev: http://localhost:8000).
 */
const BASE = import.meta.env.VITE_API_URL || ''

function getToken() {
  return localStorage.getItem('admin_token') || ''
}

export function setToken(token) {
  if (token) localStorage.setItem('admin_token', token)
  else localStorage.removeItem('admin_token')
}

function headers(includeAuth = true) {
  const h = { 'Content-Type': 'application/json' }
  if (includeAuth && getToken()) h['Authorization'] = `Bearer ${getToken()}`
  return h
}

async function request(method, path, body) {
  const opt = { method, headers: headers() }
  if (body && (method === 'POST' || method === 'PATCH' || method === 'PUT')) opt.body = JSON.stringify(body)
  const r = await fetch(`${BASE}${path}`, opt)
  if (r.status === 204) return null
  const data = await r.json().catch(() => ({}))
  if (!r.ok) throw new Error(data.error || data.detail || `HTTP ${r.status}`)
  return data
}

export async function login(username, password) {
  const data = await request('POST', '/api/auth/login/', { username, password })
  if (data.token) setToken(data.token)
  return data
}

export async function me() {
  return request('GET', '/api/auth/me/')
}

export async function logout() {
  await request('POST', '/api/auth/logout/').catch(() => {})
  setToken(null)
}

export async function getSettings() {
  return request('GET', '/api/settings/')
}

export async function patchSettings(partial) {
  return request('PATCH', '/api/admin/settings/', partial)
}

export async function getProducts() {
  return request('GET', '/api/products/')
}

export async function getProduct(id) {
  return request('GET', `/api/products/${id}/`)
}

export async function createProduct(product) {
  return request('POST', '/api/admin/products/', product)
}

export async function updateProduct(id, partial) {
  return request('PATCH', `/api/admin/products/${id}/`, partial)
}

export async function deleteProduct(id) {
  return request('DELETE', `/api/admin/products/${id}/delete/`)
}

export { getToken }
