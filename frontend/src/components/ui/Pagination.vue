<template>
  <nav v-if="totalPages > 1" class="pagination" :aria-label="ariaLabel">
    <!-- Prev -->
    <button
      class="pagination__btn pagination__btn--arrow"
      :disabled="currentPage <= 1"
      @click="emit('change', currentPage - 1)"
      aria-label="Previous page"
    >
      <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
        <path d="M12 4l-6 6 6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <!-- Page numbers + ellipsis -->
    <template v-for="(item, i) in pages" :key="i">
      <span v-if="item === null" class="pagination__ellipsis" aria-hidden="true">…</span>
      <button
        v-else
        class="pagination__btn pagination__btn--num"
        :class="{ 'pagination__btn--active': item === currentPage }"
        :aria-current="item === currentPage ? 'page' : undefined"
        @click="emit('change', item)"
      >
        {{ item }}
      </button>
    </template>

    <!-- Next -->
    <button
      class="pagination__btn pagination__btn--arrow"
      :disabled="currentPage >= totalPages"
      @click="emit('change', currentPage + 1)"
      aria-label="Next page"
    >
      <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
        <path d="M8 4l6 6-6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </nav>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: { type: Number, required: true },
  totalPages:  { type: Number, required: true },
  ariaLabel:   { type: String, default: 'Pagination' },
})

const emit = defineEmits(['change'])

const pages = computed(() => {
  const total = props.totalPages
  const cur   = props.currentPage

  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }

  // Always include: first, last, current and ±2 neighbours
  const set = new Set(
    [1, total, cur - 2, cur - 1, cur, cur + 1, cur + 2]
      .filter(p => p >= 1 && p <= total)
  )
  const sorted = [...set].sort((a, b) => a - b)

  // Insert null where there are gaps
  const result = []
  for (let i = 0; i < sorted.length; i++) {
    if (i > 0 && sorted[i] - sorted[i - 1] > 1) result.push(null)
    result.push(sorted[i])
  }
  return result
})
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  margin-top: 48px;
  flex-wrap: wrap;
}

.pagination__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  height: 36px;
  padding: 0 10px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: none;
  color: var(--text);
  font-family: inherit;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}

.pagination__btn--arrow {
  padding: 0;
  width: 36px;
  color: var(--text-secondary);
}

.pagination__btn--arrow svg {
  width: 16px;
  height: 16px;
}

.pagination__btn:hover:not(:disabled) {
  color: var(--text);
  border-color: var(--text);
}

.pagination__btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.pagination__btn--active {
  background-color: var(--accent);
  color: var(--bg);
  border-color: var(--accent);
  font-weight: 700;
}

.pagination__btn--active:hover {
  background-color: var(--accent);
  border-color: var(--accent);
  color: var(--bg);
}

.pagination__ellipsis {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  height: 36px;
  font-size: 0.875rem;
  color: var(--text-secondary);
  user-select: none;
}
</style>
