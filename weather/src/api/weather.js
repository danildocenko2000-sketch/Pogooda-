/**
 * API погоди: запити йдуть на Django (якщо задано VITE_API_URL), Django проксує на Open-Meteo та Nominatim.
 */

const BASE = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')

const OPEN_METEO_FORECAST = 'https://api.open-meteo.com/v1/forecast'
const OPEN_METEO_GEO = 'https://geocoding-api.open-meteo.com/v1/search'
const NOMINATIM_REVERSE = 'https://nominatim.openstreetmap.org/reverse'

function useDjango() {
  return Boolean(BASE)
}

/**
 * Прогноз погоди на 7 днів.
 * Якщо VITE_API_URL задано — запит на Django /api/weather/forecast/, інакше напряму на Open-Meteo.
 */
export async function getForecast(latitude, longitude) {
  if (useDjango()) {
    const params = new URLSearchParams({ latitude: String(latitude), longitude: String(longitude) })
    const res = await fetch(`${BASE}/api/weather/forecast/?${params}`)
    if (!res.ok) throw new Error('Failed to fetch weather')
    return res.json()
  }
  const params = new URLSearchParams({
    latitude: String(latitude),
    longitude: String(longitude),
    hourly: 'temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m',
    daily: 'weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,wind_speed_10m_max',
    timezone: 'auto',
    forecast_days: '7',
  })
  const res = await fetch(`${OPEN_METEO_FORECAST}?${params}`)
  if (!res.ok) throw new Error('Failed to fetch weather')
  return res.json()
}

/**
 * Пошук міст. Якщо VITE_API_URL задано — запит на Django /api/weather/search/.
 */
export async function searchCities(query, { onlyUkraine = false } = {}) {
  const q = query.trim()
  if (q.length < 2) return []
  if (useDjango()) {
    const params = new URLSearchParams({
      q,
      only_ukraine: onlyUkraine ? '1' : '0',
    })
    const res = await fetch(`${BASE}/api/weather/search/?${params}`)
    const data = await res.json().catch(() => ({ results: [] }))
    return data.results || []
  }
  const params = new URLSearchParams({
    name: q,
    count: '10',
    language: onlyUkraine ? 'uk' : 'ru',
    format: 'json',
  })
  if (onlyUkraine) params.set('countryCode', 'UA')
  const res = await fetch(`${OPEN_METEO_GEO}?${params}`)
  const data = await res.json()
  if (!data.results?.length) return []
  return data.results.map((city) => ({
    name: city.name,
    admin1: city.admin1,
    country: city.country,
    lat: city.latitude,
    lon: city.longitude,
    displayName: `${city.name}${city.admin1 ? ', ' + city.admin1 : ''}${city.country ? ', ' + city.country : ''}`,
  }))
}

/**
 * Reverse geocode. Якщо VITE_API_URL задано — запит на Django /api/weather/reverse/.
 */
export async function reverseGeocode(latitude, longitude) {
  if (useDjango()) {
    const params = new URLSearchParams({ lat: String(latitude), lon: String(longitude) })
    const res = await fetch(`${BASE}/api/weather/reverse/?${params}`)
    const data = await res.json().catch(() => ({}))
    return data.name || 'Поточна локація'
  }
  const params = new URLSearchParams({
    format: 'json',
    lat: String(latitude),
    lon: String(longitude),
    'accept-language': 'uk',
    addressdetails: '1',
  })
  const res = await fetch(`${NOMINATIM_REVERSE}?${params}`)
  if (!res.ok) return 'Поточна локація'
  const d = await res.json()
  const a = d.address || {}
  return (
    a.city ||
    a.town ||
    a.village ||
    a.municipality ||
    a.hamlet ||
    a.county ||
    (a.state && a.country ? `${a.state}, ${a.country}` : a.country) ||
    'Поточна локація'
  )
}
