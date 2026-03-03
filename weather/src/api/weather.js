/**
 * API погоди та геокодування.
 * Open-Meteo (прогноз, пошук міст), Nominatim (reverse geocode).
 */

const OPEN_METEO_FORECAST = 'https://api.open-meteo.com/v1/forecast'
const OPEN_METEO_GEO = 'https://geocoding-api.open-meteo.com/v1/search'
const NOMINATIM_REVERSE = 'https://nominatim.openstreetmap.org/reverse'

/**
 * Прогноз погоди на 7 днів (почасовий + денний).
 * @param {number} latitude
 * @param {number} longitude
 * @returns {Promise<object>} Відповідь Open-Meteo (hourly, daily, ...)
 */
export async function getForecast(latitude, longitude) {
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
 * Пошук міст за назвою (Open-Meteo Geocoding).
 * @param {string} query — рядок пошуку (мінімум 2 символи)
 * @param {{ onlyUkraine?: boolean }} options
 * @returns {Promise<Array<{ name, admin1, country, lat, lon, displayName }>>}
 */
export async function searchCities(query, { onlyUkraine = false } = {}) {
  const q = query.trim()
  if (q.length < 2) return []
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
 * Назва місця за координатами (Nominatim reverse geocoding).
 * @param {number} latitude
 * @param {number} longitude
 * @returns {Promise<string>} Назва місця або 'Поточна локація'
 */
export async function reverseGeocode(latitude, longitude) {
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
