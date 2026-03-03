import { ref, computed, watch, nextTick, onUnmounted } from 'vue'
import { weatherCodes, dayNames, shortDayNames } from '../data/weatherCodes.js'
import { getWeatherIcon } from '../utils/weatherIcons.js'

export function useWeather() {
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
      weatherData.value.daily?.weather_code?.[selectedDayIndex.value] ?? currentCode.value
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

  function onDocumentClick(e) {
    if (!e.target.closest('.search-input-wrap') && !e.target.closest('.search-results-dropdown')) {
      searchResultsVisible.value = false
    }
  }

  function setupHoursWheel() {
    const el = hoursScrollRef.value
    if (!el || el._hoursWheel) return
    el._hoursWheel = true
    el.addEventListener('wheel', onHoursWheel, { passive: false })
  }

  function setSearchQuery(v) {
    searchQuery.value = v
  }
  function setSearchOnlyUkraine(v) {
    searchOnlyUkraine.value = v
  }
  function setSearchResultsVisible(v) {
    searchResultsVisible.value = v
  }

  let searchTimeout
  watch(searchQuery, () => {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(searchCities, 300)
  })
  watch(
    () => weatherData.value?.hourly,
    () => {
      nextTick(setupHoursWheel)
    },
    { flush: 'post' }
  )
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

  onUnmounted(() => {
    window.removeEventListener('scroll', updateSearchDropdownPosition, true)
    window.removeEventListener('resize', updateSearchDropdownPosition)
  })

  return {
    unit,
    weatherData,
    selectedDayIndex,
    currentCity,
    lat,
    lon,
    loading,
    errorMessage,
    showError,
    showContent,
    showInitial,
    searchQuery,
    searchResults,
    searchResultsVisible,
    searchOnlyUkraine,
    geoRequested,
    hoursScrollRef,
    searchInputWrapRef,
    searchDropdownPosition,
    todayString,
    weatherClass,
    currentCode,
    currentWeatherType,
    currentWeatherInfo,
    locationCoordsText,
    alerts,
    dayHours,
    selectedDayName,
    shortDayNames,
    dayNames,
    convertTemp,
    getTempUnit,
    iconHtml,
    searchCities,
    selectCity,
    fetchWeather,
    getGeolocation,
    setUnit,
    selectDay,
    formatDayDate,
    onDocumentClick,
    updateSearchDropdownPosition,
    setupHoursWheel,
    setSearchQuery,
    setSearchOnlyUkraine,
    setSearchResultsVisible,
  }
}
