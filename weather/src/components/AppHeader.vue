<script setup>
defineProps({
  todayString: { type: String, default: '' },
  searchOnlyUkraine: { type: Boolean, default: false },
  searchQuery: { type: String, default: '' },
  searchResultsVisible: { type: Boolean, default: false },
  searchResults: { type: Array, default: () => [] },
  searchDropdownPosition: { type: Object, default: () => ({ top: 0, left: 0, width: 0 }) },
  unit: { type: String, default: 'celsius' },
})
const emit = defineEmits(['update:searchOnlyUkraine', 'update:searchQuery', 'selectCity', 'setUnit', 'getGeolocation', 'focusResults'])
</script>

<template>
  <header class="max-w-5xl mx-auto mb-6">
    <h1 class="text-3xl md:text-4xl font-extrabold text-white text-center drop-shadow-lg mb-1 tracking-tight">
      🌤️ Прогноз погоди
    </h1>
    <p class="text-white/90 text-center text-lg font-semibold mb-6 drop-shadow-sm">{{ todayString }}</p>
    <div class="card-glass rounded-2xl p-4 md:p-5 shadow-xl">
      <div class="flex flex-col gap-4">
        <div class="flex flex-wrap items-center gap-3">
          <label class="flex items-center gap-2 cursor-pointer text-white font-medium">
            <input
              :checked="searchOnlyUkraine"
              type="checkbox"
              class="w-4 h-4 rounded border-white/50 bg-white/20 text-blue-600 focus:ring-2 focus:ring-white"
              @change="emit('update:searchOnlyUkraine', ($event.target).checked)"
            />
            <span>Тільки Україна (міста, села, ПГТ)</span>
          </label>
          <span class="text-white/70 text-sm">— або пошук по всьому світу</span>
        </div>
        <div class="flex flex-col md:flex-row gap-4">
          <div class="flex-1 relative search-input-wrap">
            <input
              :value="searchQuery"
              type="text"
              :placeholder="searchOnlyUkraine ? 'Місто, село або ПГТ в Україні...' : 'Місто або країна (весь світ)...'"
              class="w-full px-4 py-3 rounded-xl bg-white/95 text-gray-800 placeholder-gray-500 outline-none focus:ring-2 focus:ring-amber-300 focus:border-amber-400 transition shadow-inner"
              @input="emit('update:searchQuery', ($event.target).value)"
              @focus="emit('focusResults')"
            />
            <Teleport to="body">
              <div
                v-show="searchResultsVisible"
                class="search-results-dropdown fixed bg-white rounded-xl shadow-2xl overflow-hidden border border-gray-100 max-h-[min(70vh,400px)] overflow-y-auto"
                :style="{
                  top: searchDropdownPosition.top + 'px',
                  left: searchDropdownPosition.left + 'px',
                  width: searchDropdownPosition.width + 'px',
                  zIndex: 99999
                }"
              >
                <div
                  v-for="city in searchResults"
                  :key="city.lat + ',' + city.lon"
                  class="search-result p-3 hover:bg-amber-50 cursor-pointer border-b border-gray-100 last:border-b-0 transition"
                  @click="emit('selectCity', city)"
                >
                  <div class="font-semibold text-gray-800">{{ city.name }}</div>
                  <div class="text-sm text-gray-500">
                    {{ city.admin1 ? city.admin1 + ', ' : '' }}{{ city.country || '' }}
                  </div>
                </div>
                <div
                  v-if="searchResults.length === 0 && searchQuery.length >= 2"
                  class="p-3 text-gray-500"
                >
                  Нічого не знайдено
                </div>
              </div>
            </Teleport>
          </div>
          <button
            type="button"
            class="btn-glass px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-bold rounded-xl hover:from-blue-600 hover:to-blue-700 flex items-center justify-center gap-2 shadow-lg"
            @click="emit('getGeolocation')"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span class="hidden md:inline">Моя геолокація</span>
          </button>
          <div class="flex bg-white/25 rounded-xl p-1 border border-white/20">
            <button
              type="button"
              class="px-4 py-2 rounded-lg font-bold transition"
              :class="unit === 'celsius' ? 'text-white bg-white/40' : 'text-white/70 hover:text-white'"
              @click="emit('setUnit', 'celsius')"
            >
              °C
            </button>
            <button
              type="button"
              class="px-4 py-2 rounded-lg font-bold transition"
              :class="unit === 'fahrenheit' ? 'text-white bg-white/40' : 'text-white/70 hover:text-white'"
              @click="emit('setUnit', 'fahrenheit')"
            >
              °F
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>
