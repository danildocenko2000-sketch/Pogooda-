<script setup>
defineProps({
  daily: Object,
  selectedDayIndex: Number,
  shortDayNames: Array,
  formatDayDate: Function,
  convertTemp: Function,
  iconHtml: Function,
})
defineEmits(['selectDay'])
</script>

<template>
  <div v-if="daily" class="card-glass rounded-2xl p-6 mb-6 shadow-xl">
    <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">📅 Прогноз на 7 днів</h3>
    <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
      <div
        v-for="(date, i) in daily.time"
        :key="date"
        class="day-card cursor-pointer p-4 rounded-xl transition-all duration-300"
        :class="selectedDayIndex === i ? 'bg-white/35 ring-2 ring-white shadow-lg' : 'bg-white/15 hover:bg-white/25 border border-white/10'"
        @click="$emit('selectDay', i)"
      >
        <div class="text-center">
          <p class="font-bold text-white text-sm">
            {{ i === 0 ? 'Сегодня' : shortDayNames[new Date(date).getDay()] }}
          </p>
          <p class="text-white/70 text-xs">{{ formatDayDate(date) }}</p>
          <div class="my-2 flex justify-center" v-html="iconHtml(daily.weather_code[i], 'small')"></div>
          <p class="font-bold text-white">{{ convertTemp(daily.temperature_2m_max[i]) }}°</p>
          <p class="text-white/70 text-sm">{{ convertTemp(daily.temperature_2m_min[i]) }}°</p>
        </div>
      </div>
    </div>
  </div>
</template>
