<script setup>
defineProps({
  hourly: Object,
  dayHours: Array,
  selectedDayName: String,
  convertTemp: Function,
  iconHtml: Function,
})
</script>

<template>
  <div v-if="hourly" class="card-glass rounded-2xl p-6 shadow-xl">
    <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">⏰ Почасовий прогноз — {{ selectedDayName }}</h3>
    <div class="flex gap-3 overflow-x-auto pb-4 hours-scroll">
      <div
        v-for="{ time, index } in dayHours"
        :key="time"
        class="hour-card flex-shrink-0 w-24 min-w-[6rem] p-3 bg-white/15 rounded-xl text-center cursor-default border border-white/10"
      >
        <p class="font-bold text-white">{{ String(new Date(time).getHours()).padStart(2, '0') }}:00</p>
        <div class="my-2 flex justify-center" v-html="iconHtml(hourly.weather_code[index], 'small')"></div>
        <p class="font-bold text-white text-lg">{{ convertTemp(hourly.temperature_2m[index]) }}°</p>
        <p class="text-white/70 text-xs mt-1">💧 {{ hourly.relative_humidity_2m[index] }}%</p>
        <p class="text-white/70 text-xs">💨 {{ Math.round(hourly.wind_speed_10m[index]) }}</p>
      </div>
    </div>
  </div>
</template>
