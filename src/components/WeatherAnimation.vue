<script setup>
import { watch, ref, onMounted } from 'vue'

const props = defineProps({
  type: { type: String, default: 'sunny' },
})

const container = ref(null)

function createAnimation() {
  if (!container.value) return
  container.value.innerHTML = ''

  if (props.type === 'rainy') {
    for (let i = 0; i < 50; i++) {
      const drop = document.createElement('div')
      drop.className = 'rain-drop'
      drop.style.left = `${Math.random() * 100}%`
      drop.style.animationDelay = `${Math.random() * 2}s`
      drop.style.animationDuration = `${0.5 + Math.random() * 0.5}s`
      container.value.appendChild(drop)
    }
  } else if (props.type === 'snowy') {
    for (let i = 0; i < 30; i++) {
      const flake = document.createElement('div')
      flake.className = 'snow-flake'
      flake.style.left = `${Math.random() * 100}%`
      flake.style.animationDelay = `${Math.random() * 3}s`
      flake.style.animationDuration = `${2 + Math.random() * 2}s`
      const size = 4 + Math.random() * 6
      flake.style.width = `${size}px`
      flake.style.height = `${size}px`
      container.value.appendChild(flake)
    }
  } else if (props.type === 'sunny') {
    const sunContainer = document.createElement('div')
    sunContainer.className = 'absolute top-10 right-10 w-32 h-32 opacity-30'
    sunContainer.innerHTML = `
      <svg viewBox="0 0 100 100" class="w-full h-full sun-animation">
        <circle cx="50" cy="50" r="30" fill="#fbbf24"/>
        <g class="sun-rays" style="transform-origin: 50px 50px;">
          ${[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330].map(
            (angle) =>
              `<line x1="50" y1="10" x2="50" y2="0" stroke="#fbbf24" stroke-width="4" stroke-linecap="round" transform="rotate(${angle} 50 50)"/>`
          ).join('')}
        </g>
      </svg>`
    container.value.appendChild(sunContainer)
  } else if (props.type === 'cloudy') {
    for (let i = 0; i < 3; i++) {
      const cloud = document.createElement('div')
      cloud.className = 'absolute cloud-animation opacity-20'
      cloud.style.top = `${10 + i * 15}%`
      cloud.style.left = `${10 + i * 30}%`
      cloud.style.animationDelay = `${i * 0.5}s`
      cloud.innerHTML = `
        <svg width="150" height="80" viewBox="0 0 150 80">
          <ellipse cx="75" cy="50" rx="60" ry="25" fill="white"/>
          <ellipse cx="45" cy="45" rx="35" ry="20" fill="white"/>
          <ellipse cx="105" cy="45" rx="30" ry="18" fill="white"/>
        </svg>`
      container.value.appendChild(cloud)
    }
  }
}

onMounted(createAnimation)
watch(() => props.type, createAnimation)
</script>

<template>
  <div ref="container" class="fixed inset-0 pointer-events-none overflow-hidden z-0" aria-hidden="true"></div>
</template>
