<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { weatherCodes, dayNames, shortDayNames } from './data/weatherCodes.js'
import { getWeatherIcon } from './utils/weatherIcons.js'
import WeatherAnimation from './components/WeatherAnimation.vue'

const unit = ref('celsius')
const weatherData = ref(null)
const selectedDayIndex = ref(0)
const currentCity = ref('')
const lat = ref(null)
const lon = ref(null)
const loading = ref(false)
const errorMessage = ref('')
const showError = ref(false)
const showContent = ref(false)
const showInitial = ref(true)
const searchQuery = ref('')
const searchResults = ref([])
const searchResultsVisible = ref(false)
const searchOnlyUkraine = ref(false)
const geoRequested = ref(false)
const hoursScrollRef = ref(null)
const searchInputWrapRef = ref(null)
const searchDropdownPosition = ref({ top: 0, left: 0, width: 0 })

const todayString = computed(() => {
  const d = new Date()
  const days = ['Неділя', 'Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П\'ятниця', 'Субота']
  const months = ['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня', 'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня']
  return `${days[d.getDay()]}, ${d.getDate()} ${months[d.getMonth()]} ${d.getFullYear()}`
})

const weatherClass = computed(() => {
  if (!weatherData.value) return 'weather-sunny'
  const code =
    weatherData.value.daily?.weather_code?.[selectedDayIndex.value] ??
    currentCode.value
  const w = weatherCodes[code] || weatherCodes[0]
  return `weather-${w.type}`
})

const currentCode = computed(() => {
  const data = weatherData.value
  if (!data?.hourly?.weather_code) return 0
  const idx = currentHourIndex.value
  return data.hourly.weather_code[idx] ?? 0
})

const currentWeatherType = computed(() => {
  const data = weatherData.value
  const code =
    data?.daily?.weather_code?.[selectedDayIndex.value] ?? currentCode.value
  const w = weatherCodes[code] || weatherCodes[0]
  return w.type
})

const currentHourIndex = computed(() => {
  const data = weatherData.value
  if (!data?.hourly?.time) return 0
  const currentHour = new Date().getHours()
  const idx = data.hourly.time.findIndex((t) => new Date(t).getHours() === currentHour)
  return idx >= 0 ? idx : 0
})

const currentWeatherInfo = computed(() => {
  const data = weatherData.value
  if (!data?.hourly) return null
  const i = currentHourIndex.value
  const w = weatherCodes[data.hourly.weather_code[i]] || weatherCodes[0]
  return {
    temp: data.hourly.temperature_2m[i],
    feels: data.hourly.apparent_temperature[i],
    humidity: data.hourly.relative_humidity_2m[i],
    wind: data.hourly.wind_speed_10m[i],
    description: w.description,
  }
})

const locationCoordsText = computed(() => {
  if (lat.value == null || lon.value == null) return ''
  const la = Math.abs(lat.value).toFixed(4)
  const lo = Math.abs(lon.value).toFixed(4)
  return `📍 ${la}° ${lat.value >= 0 ? 'N' : 'S'}, ${lo}° ${lon.value >= 0 ? 'E' : 'W'}`
})

const alerts = computed(() => {
  const data = weatherData.value
  if (!data?.daily) return []
  const list = []
  data.daily.temperature_2m_max.forEach((temp) => {
    if (temp > 35) list.push({ text: '🔥 Сильная жара', color: 'bg-red-500' })
    if (temp < -20) list.push({ text: '🥶 Сильный мороз', color: 'bg-blue-600' })
  })
  data.daily.wind_speed_10m_max.forEach((wind) => {
    if (wind > 50) list.push({ text: '💨 Сильный ветер', color: 'bg-yellow-500' })
  })
  data.daily.precipitation_sum.forEach((p) => {
    if (p > 20) list.push({ text: '🌧️ Обильные осадки', color: 'bg-blue-500' })
  })
  data.daily.weather_code.forEach((code) => {
    if (code >= 95) list.push({ text: '⚡ Гроза', color: 'bg-purple-500' })
  })
  return [...new Map(list.map((a) => [a.text, a])).values()]
})

const dayHours = computed(() => {
  const data = weatherData.value
  if (!data?.hourly?.time || !data?.daily?.time) return []
  const selectedDate = data.daily.time[selectedDayIndex.value]
  return data.hourly.time
    .map((time, i) => ({ time, index: i }))
    .filter((item) => item.time.startsWith(selectedDate))
})

const selectedDayName = computed(() => {
  const data = weatherData.value
  if (!data?.daily?.time) return 'Сегодня'
  const d = new Date(data.daily.time[selectedDayIndex.value])
  return selectedDayIndex.value === 0
    ? 'Сегодня'
    : `${dayNames[d.getDay()]}, ${d.getDate()}.${String(d.getMonth() + 1).padStart(2, '0')}`
})

function convertTemp(celsius) {
  if (unit.value === 'fahrenheit') return Math.round((celsius * 9) / 5 + 32)
  return Math.round(celsius)
}

function getTempUnit() {
  return unit.value === 'fahrenheit' ? '°F' : '°C'
}

function iconHtml(code, size) {
  return getWeatherIcon(code, size)
}

async function searchCities() {
  const q = searchQuery.value.trim()
  if (q.length < 2) {
    searchResults.value = []
    searchResultsVisible.value = false
    return
  }
  try {
    const lang = searchOnlyUkraine.value ? 'uk' : 'ru'
    const countryParam = searchOnlyUkraine.value ? '&countryCode=UA' : ''
    const res = await fetch(
      `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(q)}&count=10&language=${lang}&format=json${countryParam}`
    )
    const data = await res.json()
    if (data.results?.length) {
      searchResults.value = data.results.map((city) => ({
        name: city.name,
        admin1: city.admin1,
        country: city.country,
        lat: city.latitude,
        lon: city.longitude,
        displayName: `${city.name}${city.admin1 ? ', ' + city.admin1 : ''}${city.country ? ', ' + city.country : ''}`,
      }))
      searchResultsVisible.value = true
    } else {
      searchResults.value = []
      searchResultsVisible.value = true
    }
  } catch {
    searchResults.value = []
    searchResultsVisible.value = false
  }
}

function selectCity(city) {
  currentCity.value = city.displayName
  searchQuery.value = city.displayName
  searchResultsVisible.value = false
  fetchWeather(city.lat, city.lon, city.displayName)
}

async function fetchWeather(latitude, longitude, cityName) {
  loading.value = true
  showError.value = false
  try {
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,wind_speed_10m_max&timezone=auto&forecast_days=7`
    const res = await fetch(url)
    if (!res.ok) throw new Error('Failed to fetch weather')
    const data = await res.json()
    weatherData.value = data
    currentCity.value = cityName
    lat.value = latitude
    lon.value = longitude
    selectedDayIndex.value = 0
    showContent.value = true
    showInitial.value = false
  } catch (e) {
    errorMessage.value = 'Не вдалося завантажити погоду. Спробуйте ще раз.'
    showError.value = true
  } finally {
    loading.value = false
  }
}

function getGeolocation(silent = false) {
  if (!navigator.geolocation) {
    if (!silent) {
      errorMessage.value = 'Геолокация не поддерживается вашим браузером'
      showError.value = true
    }
    return
  }
  loading.value = true
  if (!silent) showError.value = false
  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const { latitude, longitude } = position.coords
      let placeName = 'Поточна локація'
      try {
        const rev = await fetch(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&accept-language=uk&addressdetails=1`
        )
        if (rev.ok) {
          const d = await rev.json()
          const a = d.address || {}
          placeName =
            a.city ||
            a.town ||
            a.village ||
            a.municipality ||
            a.hamlet ||
            a.county ||
            (a.state && a.country ? `${a.state}, ${a.country}` : a.country) ||
            placeName
        }
      } catch {}
      fetchWeather(latitude, longitude, placeName)
    },
    (err) => {
      loading.value = false
      if (!silent) {
        if (err.code === 1) errorMessage.value = 'Доступ до геолокації заборонено.'
        else if (err.code === 2) errorMessage.value = 'Інформація про місцезнаходження недоступна.'
        else if (err.code === 3) errorMessage.value = 'Час очікування геолокації вийшов.'
        else errorMessage.value = 'Помилка отримання геолокації.'
        showError.value = true
      }
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
  )
}

function setUnit(u) {
  unit.value = u
}

function selectDay(index) {
  selectedDayIndex.value = index
}

function hideSearchResults() {
  searchResultsVisible.value = false
}

function formatDayDate(dateStr) {
  const d = new Date(dateStr)
  return `${d.getDate()}.${String(d.getMonth() + 1).padStart(2, '0')}`
}

function onHoursWheel(e) {
  const el = hoursScrollRef.value
  if (!el) return
  e.preventDefault()
  el.scrollLeft += e.deltaY
}

let searchTimeout
watch(
  () => weatherData.value?.hourly,
  () => {
    nextTick(setupHoursWheel)
  },
  { flush: 'post' }
)
watch(searchQuery, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(searchCities, 300)
})
watch(searchResultsVisible, (visible) => {
  if (visible) {
    nextTick(() => {
      updateSearchDropdownPosition()
      window.addEventListener('scroll', updateSearchDropdownPosition, true)
      window.addEventListener('resize', updateSearchDropdownPosition)
    })
  } else {
    window.removeEventListener('scroll', updateSearchDropdownPosition, true)
    window.removeEventListener('resize', updateSearchDropdownPosition)
  }
})

function onDocumentClick(e) {
  if (!e.target.closest('.search-input-wrap') && !e.target.closest('.search-results-dropdown')) {
    searchResultsVisible.value = false
  }
}

function updateSearchDropdownPosition() {
  const el = searchInputWrapRef.value
  if (!el) return
  const rect = el.getBoundingClientRect()
  searchDropdownPosition.value = {
    top: rect.bottom + 8,
    left: rect.left,
    width: rect.width
  }
}

onMounted(() => {
  document.addEventListener('click', onDocumentClick)
  if (!geoRequested.value) {
    geoRequested.value = true
    setTimeout(() => getGeolocation(true), 300)
  }
})
onUnmounted(() => {
  window.removeEventListener('scroll', updateSearchDropdownPosition, true)
  window.removeEventListener('resize', updateSearchDropdownPosition)
})

function setupHoursWheel() {
  const el = hoursScrollRef.value
  if (!el || el._hoursWheel) return
  el._hoursWheel = true
  el.addEventListener('wheel', onHoursWheel, { passive: false })
}
onUnmounted(() => {
  document.removeEventListener('click', onDocumentClick)
})
</script>

<template>
  <div
    class="h-full overflow-auto transition-all duration-1000"
    :class="weatherClass"
  >
    <WeatherAnimation :key="selectedDayIndex" :type="currentWeatherType" />
    <div class="relative z-10 min-h-full p-4 md:p-8">
      <header class="max-w-5xl mx-auto mb-6">
        <h1 class="text-3xl md:text-4xl font-extrabold text-white text-center drop-shadow-lg mb-1 tracking-tight">
          🌤️ Прогноз погоди
        </h1>
        <p class="text-white/90 text-center text-lg font-semibold mb-6 drop-shadow-sm">{{ todayString }}</p>
        <div class="card-glass rounded-2xl p-4 md:p-5 shadow-xl">
          <div class="flex flex-col gap-4">
            <div class="flex flex-wrap items-center gap-3">
              <label class="flex items-center gap-2 cursor-pointer text-white font-medium">
                <input
                  v-model="searchOnlyUkraine"
                  type="checkbox"
                  class="w-4 h-4 rounded border-white/50 bg-white/20 text-blue-600 focus:ring-2 focus:ring-white"
                />
                <span>Тільки Україна (міста, села, ПГТ)</span>
              </label>
              <span class="text-white/70 text-sm">— або пошук по всьому світу</span>
            </div>
            <div class="flex flex-col md:flex-row gap-4">
              <div ref="searchInputWrapRef" class="flex-1 relative search-input-wrap">
                <input
                  v-model="searchQuery"
                  type="text"
                  :placeholder="searchOnlyUkraine ? 'Місто, село або ПГТ в Україні...' : 'Місто або країна (весь світ)...'"
                  class="w-full px-4 py-3 rounded-xl bg-white/95 text-gray-800 placeholder-gray-500 outline-none focus:ring-2 focus:ring-amber-300 focus:border-amber-400 transition shadow-inner"
                  @focus="searchQuery.length >= 2 && (searchResultsVisible = true)"
                />
                <Teleport to="body">
                  <div
                    v-show="searchResultsVisible"
                    class="search-results-dropdown fixed bg-white rounded-xl shadow-2xl overflow-hidden border border-gray-100 max-h-[min(70vh,400px)] overflow-y-auto"
                    :style="{
                      top: searchDropdownPosition.top + 'px',
                      left: searchDropdownPosition.left + 'px',
                      width: searchDropdownPosition.width + 'px',
                      zIndex: 99999
                    }"
                  >
                    <div
                      v-for="city in searchResults"
                      :key="city.lat + ',' + city.lon"
                      class="search-result p-3 hover:bg-amber-50 cursor-pointer border-b border-gray-100 last:border-b-0 transition"
                      @click="selectCity(city)"
                    >
                      <div class="font-semibold text-gray-800">{{ city.name }}</div>
                      <div class="text-sm text-gray-500">
                        {{ city.admin1 ? city.admin1 + ', ' : '' }}{{ city.country || '' }}
                      </div>
                    </div>
                    <div
                      v-if="searchResults.length === 0 && searchQuery.length >= 2"
                      class="p-3 text-gray-500"
                    >
                      Нічого не знайдено
                    </div>
                  </div>
                </Teleport>
              </div>
              <button
                type="button"
                class="btn-glass px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-bold rounded-xl hover:from-blue-600 hover:to-blue-700 flex items-center justify-center gap-2 shadow-lg"
                @click="getGeolocation"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span class="hidden md:inline">Моя геолокація</span>
              </button>
              <div class="flex bg-white/25 rounded-xl p-1 border border-white/20">
                <button
                  type="button"
                  class="px-4 py-2 rounded-lg font-bold transition"
                  :class="unit === 'celsius' ? 'text-white bg-white/40' : 'text-white/70 hover:text-white'"
                  @click="setUnit('celsius')"
                >
                  °C
                </button>
                <button
                  type="button"
                  class="px-4 py-2 rounded-lg font-bold transition"
                  :class="unit === 'fahrenheit' ? 'text-white bg-white/40' : 'text-white/70 hover:text-white'"
                  @click="setUnit('fahrenheit')"
                >
                  °F
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      <!-- Loading -->
      <div v-show="loading" class="max-w-5xl mx-auto">
        <div class="card-glass rounded-2xl p-10 text-center">
          <div class="inline-block w-14 h-14 border-4 border-white/30 border-t-white rounded-full animate-spin"></div>
          <p class="text-white font-semibold mt-5">Визначення місця та завантаження погоди...</p>
          <p class="text-white/70 text-sm mt-2">Може зайняти кілька секунд</p>
        </div>
      </div>

      <!-- Error -->
      <div v-show="showError && !loading" class="max-w-5xl mx-auto">
        <div class="card-glass rounded-2xl p-8 text-center border-2 border-red-400/40 bg-red-500/20">
          <p class="text-white font-semibold text-lg">⚠️ {{ errorMessage }}</p>
        </div>
      </div>

      <!-- Weather Content -->
      <main v-show="showContent && !loading" class="max-w-5xl mx-auto">
        <div class="card-glass rounded-2xl p-6 md:p-6 mb-6 shadow-xl">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <h2 class="text-2xl md:text-3xl font-bold text-white">{{ currentCity }}</h2>
              <p class="text-white/80 text-sm mt-1">{{ locationCoordsText }}</p>
            </div>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="alert in alerts"
                :key="alert.text"
                class="text-white text-sm font-semibold px-3 py-1 rounded-full"
                :class="alert.color"
              >
                {{ alert.text }}
              </span>
            </div>
          </div>
        </div>

        <div v-if="currentWeatherInfo" class="card-glass rounded-2xl p-6 md:p-8 mb-6 shadow-xl">
          <div class="flex flex-col md:flex-row items-center gap-6">
            <div class="w-32 h-32 flex items-center justify-center" v-html="iconHtml(currentCode, 'large')"></div>
            <div class="text-center md:text-left flex-1">
              <p class="text-6xl md:text-7xl font-extrabold text-white drop-shadow-lg">
                {{ convertTemp(currentWeatherInfo.temp) }}{{ getTempUnit() }}
              </p>
              <p class="text-xl text-white/90 capitalize mt-2">{{ currentWeatherInfo.description }}</p>
              <div class="flex flex-wrap justify-center md:justify-start gap-4 mt-4 text-white/80">
                <span>🌡️ Відчувається: {{ convertTemp(currentWeatherInfo.feels) }}{{ getTempUnit() }}</span>
                <span>💧 Вологість: {{ currentWeatherInfo.humidity }}%</span>
                <span>💨 Вітер: {{ Math.round(currentWeatherInfo.wind) }} км/год</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="weatherData?.daily" class="card-glass rounded-2xl p-6 mb-6 shadow-xl">
          <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">📅 Прогноз на 7 днів</h3>
          <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
            <div
              v-for="(date, i) in weatherData.daily.time"
              :key="date"
              class="day-card cursor-pointer p-4 rounded-xl transition-all duration-300"
              :class="selectedDayIndex === i ? 'bg-white/35 ring-2 ring-white shadow-lg' : 'bg-white/15 hover:bg-white/25 border border-white/10'"
              @click="selectDay(i)"
            >
              <div class="text-center">
                <p class="font-bold text-white text-sm">
                  {{ i === 0 ? 'Сегодня' : shortDayNames[new Date(date).getDay()] }}
                </p>
                <p class="text-white/70 text-xs">{{ formatDayDate(date) }}</p>
                <div class="my-2 flex justify-center" v-html="iconHtml(weatherData.daily.weather_code[i], 'small')"></div>
                <p class="font-bold text-white">{{ convertTemp(weatherData.daily.temperature_2m_max[i]) }}°</p>
                <p class="text-white/70 text-sm">{{ convertTemp(weatherData.daily.temperature_2m_min[i]) }}°</p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="weatherData?.hourly" class="card-glass rounded-2xl p-6 shadow-xl">
          <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">⏰ Почасовий прогноз — {{ selectedDayName }}</h3>
          <div ref="hoursScrollRef" class="flex gap-3 overflow-x-auto pb-4 hours-scroll">
            <div
              v-for="{ time, index } in dayHours"
              :key="time"
              class="hour-card flex-shrink-0 w-24 min-w-[6rem] p-3 bg-white/15 rounded-xl text-center cursor-default border border-white/10"
            >
              <p class="font-bold text-white">{{ String(new Date(time).getHours()).padStart(2, '0') }}:00</p>
              <div class="my-2 flex justify-center" v-html="iconHtml(weatherData.hourly.weather_code[index], 'small')"></div>
              <p class="font-bold text-white text-lg">{{ convertTemp(weatherData.hourly.temperature_2m[index]) }}°</p>
              <p class="text-white/70 text-xs mt-1">💧 {{ weatherData.hourly.relative_humidity_2m[index] }}%</p>
              <p class="text-white/70 text-xs">💨 {{ Math.round(weatherData.hourly.wind_speed_10m[index]) }}</p>
            </div>
          </div>
        </div>
      </main>

      <!-- Initial State -->
      <div v-show="showInitial && !loading" class="max-w-5xl mx-auto">
        <div class="card-glass rounded-2xl p-8 md:p-10 text-center">
          <div class="text-7xl mb-5">🌍</div>
          <h2 class="text-2xl md:text-3xl font-bold text-white mb-3">Ласкаво просимо!</h2>
          <p class="text-white/90 mb-3 leading-relaxed">
            Погода визначається за вашою геолокацією автоматично. Якщо ви відмовили у доступі — введіть місто (Україна або будь-яка країна) або натисніть «Моя геолокація».
          </p>
          <p class="text-white/80 text-sm">Прогноз на 7 днів вперед для будь-якого міста, села чи ПГТ.</p>
        </div>
      </div>

      <footer class="max-w-5xl mx-auto mt-10 pb-8 text-center">
        <p class="text-white/60 text-sm">Прогноз погоди · Open-Meteo · Vue</p>
      </footer>
    </div>
  </div>
</template>
