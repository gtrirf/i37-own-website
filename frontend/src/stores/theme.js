import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(false)

  function init() {
    const stored = localStorage.getItem('theme')
    if (stored === 'dark') {
      isDark.value = true
      document.documentElement.classList.add('dark')
    } else if (stored === 'light') {
      isDark.value = false
      document.documentElement.classList.remove('dark')
    } else {
      // Default to system preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      isDark.value = prefersDark
      if (prefersDark) {
        document.documentElement.classList.add('dark')
      }
    }
  }

  function toggle() {
    isDark.value = !isDark.value
    if (isDark.value) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('theme', 'light')
    }
  }

  return { isDark, init, toggle }
})
