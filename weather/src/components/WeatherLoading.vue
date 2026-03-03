<script setup>
defineProps({
  show: { type: Boolean, default: false },
})
</script>

<template>
  <div v-show="show" class="max-w-5xl mx-auto">
    <div class="card-glass rounded-2xl p-10 text-center">
      <div class="inline-block w-14 h-14 border-4 border-white/30 border-t-white rounded-full animate-spin"></div>
      <p class="text-white font-semibold mt-5">Визначення місця та завантаження погоди...</p>
      <p class="text-white/70 text-sm mt-2">Може зайняти кілька секунд</p>
    </div>
  </div>
</template>
