import { weatherCodes } from '../data/weatherCodes.js'

export function getWeatherIcon(code, size = 'large') {
  const weather = weatherCodes[code] || weatherCodes[0]
  const sizeClass = size === 'large' ? 'w-24 h-24' : size === 'medium' ? 'w-16 h-16' : 'w-10 h-10'

  switch (weather.icon) {
    case 'sun':
      return `
        <div class="${sizeClass} relative sun-animation">
          <svg viewBox="0 0 100 100" class="w-full h-full">
            <circle cx="50" cy="50" r="20" fill="#fbbf24"/>
            <g class="sun-rays" style="transform-origin: 50px 50px;">
              ${[0, 45, 90, 135, 180, 225, 270, 315]
                .map(
                  (angle) =>
                    `<line x1="50" y1="15" x2="50" y2="5" stroke="#fbbf24" stroke-width="4" stroke-linecap="round" transform="rotate(${angle} 50 50)"/>`
                )
                .join('')}
            </g>
          </svg>
        </div>`

    case 'cloud-sun':
      return `
        <div class="${sizeClass} relative">
          <svg viewBox="0 0 100 100" class="w-full h-full">
            <circle cx="30" cy="35" r="15" fill="#fbbf24" class="sun-animation"/>
            <ellipse cx="55" cy="60" rx="30" ry="20" fill="#e2e8f0" class="cloud-animation"/>
            <ellipse cx="40" cy="55" rx="20" ry="15" fill="#f1f5f9" class="cloud-animation"/>
            <ellipse cx="70" cy="55" rx="15" ry="12" fill="#e2e8f0" class="cloud-animation"/>
          </svg>
        </div>`

    case 'cloud':
      return `
        <div class="${sizeClass} relative cloud-animation">
          <svg viewBox="0 0 100 100" class="w-full h-full">
            <ellipse cx="50" cy="55" rx="35" ry="22" fill="#94a3b8"/>
            <ellipse cx="30" cy="50" rx="25" ry="18" fill="#cbd5e1"/>
            <ellipse cx="70" cy="50" rx="20" ry="15" fill="#94a3b8"/>
            <ellipse cx="50" cy="45" rx="20" ry="15" fill="#e2e8f0"/>
          </svg>
        </div>`

    case 'fog':
      return `
        <div class="${sizeClass} relative">
          <svg viewBox="0 0 100 100" class="w-full h-full">
            <line x1="15" y1="35" x2="85" y2="35" stroke="#94a3b8" stroke-width="6" stroke-linecap="round" opacity="0.6"/>
            <line x1="20" y1="50" x2="80" y2="50" stroke="#94a3b8" stroke-width="6" stroke-linecap="round" opacity="0.8"/>
            <line x1="15" y1="65" x2="85" y2="65" stroke="#94a3b8" stroke-width="6" stroke-linecap="round"/>
          </svg>
        </div>`

    case 'rain-light':
    case 'rain':
    case 'rain-heavy': {
      const dropCount = weather.icon === 'rain-heavy' ? 5 : weather.icon === 'rain' ? 3 : 2
      return `
        <div class="${sizeClass} relative">
          <svg viewBox="0 0 100 100" class="w-full h-full">
            <ellipse cx="50" cy="35" rx="30" ry="18" fill="#64748b" class="cloud-animation"/>
            <ellipse cx="35" cy="32" rx="18" ry="12" fill="#94a3b8"/>
            <ellipse cx="65" cy="32" rx="15" ry="10" fill="#64748b"/>
            ${Array.from(
              { length: dropCount },
              (_, i) => {
                const x = 25 + i * 15
                return `<line x1="${x}" y1="55" x2="${x - 5}" y2="75" stroke="#60a5fa" stroke-width="3" stroke-linecap="round"/>`
              }
            ).join('')}
          </svg>
        </div>`
    }

    case 'snow-light':
    case 'snow':
    case 'snow-heavy': {
      const flakeCount = weather.icon === 'snow-heavy' ? 6 : weather.icon === 'snow' ? 4 : 2
      return `
        <div class="${sizeClass} relative">
          <svg viewBox="0 0 100 100" class="w-full h-full">
            <ellipse cx="50" cy="35" rx="30" ry="18" fill="#94a3b8" class="cloud-animation"/>
            <ellipse cx="35" cy="32" rx="18" ry="12" fill="#cbd5e1"/>
            <ellipse cx="65" cy="32" rx="15" ry="10" fill="#94a3b8"/>
            ${Array.from(
              { length: flakeCount },
              (_, i) => {
                const x = 20 + i * 12
                const y = 60 + (i % 2) * 10
                return `<circle cx="${x}" cy="${y}" r="4" fill="white"/>`
              }
            ).join('')}
          </svg>
        </div>`
    }

    case 'thunderstorm':
      return `
        <div class="${sizeClass} relative">
          <svg viewBox="0 0 100 100" class="w-full h-full">
            <ellipse cx="50" cy="30" rx="32" ry="18" fill="#374151" class="cloud-animation"/>
            <ellipse cx="32" cy="28" rx="20" ry="14" fill="#4b5563"/>
            <ellipse cx="68" cy="28" rx="16" ry="12" fill="#374151"/>
            <polygon points="45,45 55,45 48,60 58,60 42,80 48,62 38,62" fill="#fbbf24"/>
            <line x1="30" y1="55" x2="25" y2="70" stroke="#60a5fa" stroke-width="2" stroke-linecap="round"/>
            <line x1="70" y1="55" x2="65" y2="70" stroke="#60a5fa" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>`

    default:
      return `
        <div class="${sizeClass} relative sun-animation">
          <svg viewBox="0 0 100 100" class="w-full h-full">
            <circle cx="50" cy="50" r="25" fill="#fbbf24"/>
          </svg>
        </div>`
  }
}
