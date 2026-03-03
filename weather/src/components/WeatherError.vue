<script setup>
defineProps({
  show: { type: Boolean, default: false },
  message: { type: String, default: '' },
})
</script>

<template>
  <div v-show="show" class="max-w-5xl mx-auto">
    <div class="card-glass rounded-2xl p-8 text-center border-2 border-red-400/40 bg-red-500/20">
      <p class="text-white font-semibold text-lg">⚠️ {{ message }}</p>
    </div>
  </div>
</template>
