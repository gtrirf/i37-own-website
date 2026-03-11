<template>
  <span class="tech-tag" :style="tagStyle">
    {{ name }}
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  color: {
    type: String,
    default: null
  }
})

function hexToRgb(hex) {
  const clean = hex?.replace('#', '') || ''
  if (clean.length !== 6) return null
  const r = parseInt(clean.slice(0, 2), 16)
  const g = parseInt(clean.slice(2, 4), 16)
  const b = parseInt(clean.slice(4, 6), 16)
  if (isNaN(r) || isNaN(g) || isNaN(b)) return null
  return { r, g, b }
}

const tagStyle = computed(() => {
  if (!props.color) return {}
  const rgb = hexToRgb(props.color)
  if (!rgb) return {}
  return {
    backgroundColor: `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0.15)`,
    color: props.color,
    borderColor: `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0.3)`
  }
})
</script>

<style scoped>
.tech-tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--border);
  background-color: var(--bg-secondary);
  color: var(--text-secondary);
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  white-space: nowrap;
}
</style>
