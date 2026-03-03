<script setup>
defineProps({
  currentWeatherInfo: Object,
  currentCode: Number,
  convertTemp: Function,
  getTempUnit: Function,
  iconHtml: Function,
})
</script>

<template>
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
</template>
