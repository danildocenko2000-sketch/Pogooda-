<script setup>
defineProps({
  show: Boolean,
})
</script>

<template>
  <div v-show="show" class="max-w-5xl mx-auto">
    <div class="card-glass rounded-2xl p-8 md:p-10 text-center">
      <div class="text-7xl mb-5">🌍</div>
      <h2 class="text-2xl md:text-3xl font-bold text-white mb-3">Ласкаво просимо!</h2>
      <p class="text-white/90 mb-3 leading-relaxed">
        Погода визначається за вашою геолокацією автоматично. Якщо ви відмовили у доступі — введіть місто (Україна або будь-яка країна) або натисніть «Моя геолокація».
      </p>
      <p class="text-white/80 text-sm">Прогноз на 7 днів вперед для будь-якого міста, села чи ПГТ.</p>
    </div>
  </div>
</template>
