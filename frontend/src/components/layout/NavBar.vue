<template>
  <header class="navbar">
    <div class="container navbar__inner">
      <!-- Logo -->
      <RouterLink to="/" class="navbar__logo" aria-label="i37 home">
        <img
          :src="themeStore.isDark ? logoDark : logoLight"
          alt="i37"
          class="navbar__logo-img"
        />
      </RouterLink>

      <!-- Center Navigation -->
      <nav class="navbar__nav" ref="navEl" aria-label="Main navigation">
        <a
          href="https://team.i37.uz"
          target="_blank"
          rel="noopener noreferrer"
          class="navbar__link navbar__link--external"
        >
          Team
          <svg class="navbar__ext-icon" viewBox="0 0 12 12" fill="none" aria-hidden="true">
            <path d="M2 10L10 2M10 2H4M10 2V8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </a>
        <RouterLink
          to="/"
          ref="meLink"
          class="navbar__link"
          :class="{ 'navbar__link--active': isActive('/') }"
        >
          Me
        </RouterLink>
        <RouterLink
          to="/blog"
          ref="blogLink"
          class="navbar__link"
          :class="{ 'navbar__link--active': isActive('/blog') }"
        >
          Blog
        </RouterLink>
        <RouterLink
          to="/portfolio"
          ref="portfolioLink"
          class="navbar__link"
          :class="{ 'navbar__link--active': isActive('/portfolio') }"
        >
          Portfolio
        </RouterLink>

        <!-- Sliding active indicator -->
        <span class="navbar__indicator" :style="indicatorStyle" aria-hidden="true" />
      </nav>

      <!-- Dark Mode Toggle -->
      <button
        class="navbar__theme-btn"
        @click="themeStore.toggle()"
        :aria-label="themeStore.isDark ? 'Switch to light mode' : 'Switch to dark mode'"
        :title="themeStore.isDark ? 'Light mode' : 'Dark mode'"
      >
        <!-- Moon icon (shown in light mode) -->
        <svg v-if="!themeStore.isDark" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path
            d="M21 12.79A9 9 0 1 1 11.21 3a7 7 0 0 0 9.79 9.79z"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
        <!-- Sun icon (shown in dark mode) -->
        <svg v-else viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="2"/>
          <line x1="12" y1="1" x2="12" y2="3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <line x1="12" y1="21" x2="12" y2="23" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <line x1="1" y1="12" x2="3" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <line x1="21" y1="12" x2="23" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useThemeStore } from '@/stores/theme.js'
import logoDark from '@/components/static/logofordark.png'
import logoLight from '@/components/static/logoforlight.png'

const route = useRoute()
const themeStore = useThemeStore()

const navEl = ref(null)
const meLink = ref(null)
const blogLink = ref(null)
const portfolioLink = ref(null)

const indicatorStyle = ref({
  transform: 'translateX(0px)',
  width: '0px',
  opacity: '0',
})

function isActive(path) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

function updateIndicator() {
  if (!navEl.value) return

  const linkMap = {
    '/': meLink.value?.$el,
    '/blog': blogLink.value?.$el,
    '/portfolio': portfolioLink.value?.$el,
  }

  let activePath = null
  if (route.path === '/') activePath = '/'
  else if (route.path.startsWith('/blog')) activePath = '/blog'
  else if (route.path.startsWith('/portfolio')) activePath = '/portfolio'

  const activeEl = activePath ? linkMap[activePath] : null

  if (!activeEl) {
    indicatorStyle.value = { ...indicatorStyle.value, opacity: '0' }
    return
  }

  const navRect = navEl.value.getBoundingClientRect()
  const linkRect = activeEl.getBoundingClientRect()
  const pad = 14

  const left = linkRect.left - navRect.left + pad
  const width = linkRect.width - pad * 2

  indicatorStyle.value = {
    transform: `translateX(${left}px)`,
    width: `${width}px`,
    opacity: '1',
  }
}

let resizeObserver = null

onMounted(() => {
  nextTick(updateIndicator)
  resizeObserver = new ResizeObserver(() => updateIndicator())
  resizeObserver.observe(document.documentElement)
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
})

watch(() => route.path, () => nextTick(updateIndicator))
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: color-mix(in srgb, var(--bg) 75%, transparent);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

.navbar__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.navbar__logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  flex-shrink: 0;
  transition: opacity 0.15s ease;
}

.navbar__logo:hover {
  opacity: 0.7;
}

.navbar__logo-img {
  height: 28px;
  width: auto;
  display: block;
}

.navbar__nav {
  position: relative;
  display: flex;
  align-items: center;
  gap: 4px;
}

.navbar__link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  transition: color 0.15s ease;
}

.navbar__link:hover {
  color: var(--text);
}

.navbar__link--active {
  color: var(--text);
  font-weight: 700;
}

.navbar__indicator {
  position: absolute;
  bottom: -2px;
  left: 0;
  height: 2px;
  background-color: var(--accent);
  border-radius: 1px;
  pointer-events: none;
  will-change: transform, width;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              opacity 0.2s ease;
}

.navbar__link--external {
  color: var(--text-secondary);
}

.navbar__ext-icon {
  width: 10px;
  height: 10px;
  flex-shrink: 0;
  opacity: 0.7;
}

.navbar__theme-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 8px;
  color: var(--text-secondary);
  background: none;
  border: none;
  cursor: pointer;
  flex-shrink: 0;
  transition: color 0.15s ease;
}

.navbar__theme-btn:hover {
  color: var(--text);
}

.navbar__theme-btn svg {
  width: 20px;
  height: 20px;
}

@media (max-width: 600px) {
  .navbar__link {
    padding: 6px 10px;
    font-size: 0.875rem;
  }

  .navbar__logo-img {
    height: 24px;
  }
}

@media (max-width: 440px) {
  .navbar__nav {
    gap: 2px;
  }

  .navbar__link {
    padding: 5px 8px;
    font-size: 0.8125rem;
  }
}
</style>
