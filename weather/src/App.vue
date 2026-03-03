<script setup>
import { onMounted, onUnmounted, ref, watch, nextTick } from 'vue'
import WeatherAnimation from './components/WeatherAnimation.vue'
import AppHeader from './components/AppHeader.vue'
import WeatherLoading from './components/WeatherLoading.vue'
import WeatherError from './components/WeatherError.vue'
import WeatherLocationCard from './components/WeatherLocationCard.vue'
import WeatherCurrentCard from './components/WeatherCurrentCard.vue'
import WeatherDailyForecast from './components/WeatherDailyForecast.vue'
import WeatherHourlyForecast from './components/WeatherHourlyForecast.vue'
import WeatherInitialState from './components/WeatherInitialState.vue'
import AppFooter from './components/AppFooter.vue'
import { useWeather } from './composables/useWeather.js'

const weather = useWeather()
const headerRef = ref(null)
const hourlyRef = ref(null)

// Прив’язка ref до елементів у дочірніх компонентах
onMounted(() => {
  document.addEventListener('click', weather.onDocumentClick)
  if (!weather.geoRequested.value) {
    weather.geoRequested.value = true
    setTimeout(() => weather.getGeolocation(true), 300)
  }
  nextTick(() => {
    const searchEl = headerRef.value?.$el?.querySelector('.search-input-wrap')
    if (searchEl) weather.searchInputWrapRef.value = searchEl
  })
})
watch(
  () => weather.weatherData.value?.hourly,
  () => {
    nextTick(() => {
      const scrollEl = hourlyRef.value?.$el?.querySelector('.hours-scroll')
      if (scrollEl && !scrollEl._hoursWheel) {
        scrollEl._hoursWheel = true
        scrollEl.addEventListener('wheel', weather.onHoursWheel, { passive: false })
      }
    })
  },
  { flush: 'post' }
)
onUnmounted(() => {
  document.removeEventListener('click', weather.onDocumentClick)
})
</script>

<template>
  <div
    class="h-full overflow-auto transition-all duration-1000"
    :class="weather.weatherClass"
  >
    <WeatherAnimation :key="weather.selectedDayIndex" :type="weather.currentWeatherType" />
    <div class="relative z-10 min-h-full p-4 md:p-8">
      <AppHeader
        ref="headerRef"
        :today-string="weather.todayString"
        :search-only-ukraine="weather.searchOnlyUkraine"
        :search-query="weather.searchQuery"
        :search-results-visible="weather.searchResultsVisible"
        :search-results="weather.searchResults"
        :search-dropdown-position="weather.searchDropdownPosition"
        :unit="weather.unit"
        @update:search-only-ukraine="weather.setSearchOnlyUkraine($event)"
        @update:search-query="weather.setSearchQuery($event)"
        @focus-results="weather.searchQuery.length >= 2 && weather.setSearchResultsVisible(true)"
        @select-city="weather.selectCity($event)"
        @set-unit="weather.setUnit($event)"
        @get-geolocation="weather.getGeolocation()"
      />

      <WeatherLoading :show="weather.loading" />
      <WeatherError :show="weather.showError && !weather.loading" :message="weather.errorMessage" />

      <main v-show="weather.showContent && !weather.loading" class="max-w-5xl mx-auto">
        <WeatherLocationCard
          :current-city="weather.currentCity"
          :location-coords-text="weather.locationCoordsText"
          :alerts="weather.alerts"
        />
        <WeatherCurrentCard
          :current-weather-info="weather.currentWeatherInfo"
          :current-code="weather.currentCode"
          :convert-temp="weather.convertTemp"
          :get-temp-unit="weather.getTempUnit"
          :icon-html="weather.iconHtml"
        />
        <WeatherDailyForecast
          :daily="weather.weatherData?.daily"
          :selected-day-index="weather.selectedDayIndex"
          :short-day-names="weather.shortDayNames"
          :format-day-date="weather.formatDayDate"
          :convert-temp="weather.convertTemp"
          :icon-html="weather.iconHtml"
          @select-day="weather.selectDay($event)"
        />
        <WeatherHourlyForecast
          ref="hourlyRef"
          :hourly="weather.weatherData?.hourly"
          :day-hours="weather.dayHours"
          :selected-day-name="weather.selectedDayName"
          :convert-temp="weather.convertTemp"
          :icon-html="weather.iconHtml"
        />
      </main>

      <WeatherInitialState :show="weather.showInitial && !weather.loading" />
      <AppFooter />
    </div>
  </div>
</template>
