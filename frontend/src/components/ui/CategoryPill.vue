<template>
  <button
    class="category-pill"
    :class="{ 'category-pill--active': active }"
    :aria-pressed="active"
    @click="$emit('click')"
    type="button"
  >
    {{ label }}
  </button>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    required: true
  },
  active: {
    type: Boolean,
    default: false
  }
})

defineEmits(['click'])
</script>

<style scoped>
.category-pill {
  display: inline-flex;
  align-items: center;
  padding: 6px 16px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--border);
  background-color: transparent;
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}

.category-pill:hover {
  color: var(--text);
  border-color: var(--text);
  background-color: var(--bg-secondary);
}

.category-pill--active {
  background-color: var(--accent);
  color: var(--bg);
  border-color: var(--accent);
  font-weight: 600;
}

.category-pill--active:hover {
  background-color: var(--accent-hover);
  border-color: var(--accent-hover);
  color: var(--bg);
}
</style>
