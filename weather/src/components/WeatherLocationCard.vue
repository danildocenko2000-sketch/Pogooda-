<script setup>
defineProps({
  currentCity: String,
  locationCoordsText: String,
  alerts: Array,
})
</script>

<template>
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
</template>
