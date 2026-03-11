<template>
  <div class="app-wrapper">
    <NavBar />
    <main class="main-content">
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>
    <Footer />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme.js'
import NavBar from '@/components/layout/NavBar.vue'
import Footer from '@/components/layout/Footer.vue'

const themeStore = useThemeStore()

onMounted(() => {
  themeStore.init()
})
</script>

<style>
/* ── CSS Variables ─────────────────────────────────────────── */
:root {
  --bg: #ffffff;
  --bg-secondary: #f9f9f9;
  --text: #0d0d0d;
  --text-secondary: #6b7280;
  --border: #e5e7eb;
  --accent: #0d0d0d;
  --accent-hover: #2d2d2d;
  --card-bg: #ffffff;
  --shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  --shadow-hover: 0 8px 32px rgba(0, 0, 0, 0.12);
  --radius-card: 12px;
  --radius-pill: 999px;
}

.dark {
  --bg: #111111;
  --bg-secondary: #1a1a1a;
  --text: #f5f5f5;
  --text-secondary: #9ca3af;
  --border: #2d2d2d;
  --accent: #f5f5f5;
  --accent-hover: #d4d4d4;
  --card-bg: #1a1a1a;
  --shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
  --shadow-hover: 0 8px 32px rgba(0, 0, 0, 0.5);
}

/* ── Global Reset ──────────────────────────────────────────── */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  scroll-behavior: smooth;
}

body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background-color: var(--bg);
  color: var(--text);
  line-height: 1.6;
  transition: background-color 0.2s ease, color 0.2s ease;
  min-height: 100vh;
}

a {
  color: inherit;
  text-decoration: none;
}

img {
  max-width: 100%;
  display: block;
}

button {
  font-family: inherit;
  cursor: pointer;
  border: none;
  background: none;
}

ul,
ol {
  list-style: none;
}

/* ── Layout ────────────────────────────────────────────────── */
.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
}

.container {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
}

/* ── Page transitions ──────────────────────────────────────── */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

/* ── Utility ───────────────────────────────────────────────── */
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
}
</style>

<style scoped>
/* No scoped styles needed — layout is handled globally */
</style>
