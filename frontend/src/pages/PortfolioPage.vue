<template>
  <div class="portfolio-page">
    <div class="container">
      <!-- Header -->
      <header class="portfolio-page__header">
        <h1 class="portfolio-page__title">Portfolio</h1>
        <p class="portfolio-page__subtitle">
          A selection of projects I've built — from web apps to tools and experiments.
        </p>
      </header>

      <!-- Search -->
      <div class="portfolio-page__toolbar">
        <div class="search-wrap">
          <label for="portfolio-search" class="visually-hidden">Search projects</label>
          <svg class="search-wrap__icon" viewBox="0 0 20 20" fill="none" aria-hidden="true">
            <circle cx="9" cy="9" r="6" stroke="currentColor" stroke-width="1.5"/>
            <path d="m14 14 3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <input
            id="portfolio-search"
            v-model="searchQuery"
            type="search"
            placeholder="Search projects…"
            class="search-wrap__input"
            @input="onSearchInput"
          />
        </div>
        <p v-if="portfolioStore.pagination.count" class="portfolio-page__count">
          {{ portfolioStore.pagination.count }} project{{ portfolioStore.pagination.count !== 1 ? 's' : '' }}
        </p>
      </div>

      <!-- Error -->
      <div v-if="portfolioStore.error" class="portfolio-page__error" role="alert">
        <p>{{ portfolioStore.error }}</p>
        <button @click="loadProjects" class="retry-btn">Try again</button>
      </div>

      <!-- Loading skeleton -->
      <div v-else-if="portfolioStore.loading" class="portfolio-page__grid" aria-busy="true" aria-live="polite">
        <div v-for="n in 6" :key="n" class="skeleton-project-card">
          <div class="skeleton skeleton--cover"></div>
          <div class="skeleton-project-card__body">
            <div class="skeleton skeleton--title"></div>
            <div class="skeleton skeleton--text"></div>
            <div class="skeleton skeleton--text skeleton--short"></div>
          </div>
        </div>
      </div>

      <!-- Grid -->
      <div v-else-if="portfolioStore.projects.length" class="portfolio-page__grid">
        <ProjectCard
          v-for="project in portfolioStore.projects"
          :key="project.id"
          :project="project"
        />
      </div>

      <!-- Empty state -->
      <div v-else class="portfolio-page__empty">
        <svg viewBox="0 0 64 64" fill="none" aria-hidden="true">
          <rect width="64" height="64" rx="12" fill="currentColor" opacity="0.06"/>
          <path d="M16 44l10-14 8 10 6-8 8 12H16z" fill="currentColor" opacity="0.15"/>
        </svg>
        <p>No projects found{{ searchQuery ? ` for "${searchQuery}"` : '' }}.</p>
      </div>

      <!-- Pagination -->
      <Pagination
        :current-page="currentPage"
        :total-pages="totalPages"
        aria-label="Project pagination"
        @change="goToPage"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { usePortfolioStore } from '@/stores/portfolio.js'
import ProjectCard from '@/components/ui/ProjectCard.vue'
import Pagination from '@/components/ui/Pagination.vue'

const portfolioStore = usePortfolioStore()
const searchQuery = ref('')
const currentPage = ref(1)

const PAGE_SIZE = 9
let searchTimer = null

const totalPages = computed(() => {
  return Math.ceil((portfolioStore.pagination.count || 0) / PAGE_SIZE)
})

async function loadProjects() {
  await portfolioStore.fetchProjects({
    page: currentPage.value,
    search: searchQuery.value.trim()
  })
}

function onSearchInput() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    currentPage.value = 1
    loadProjects()
  }, 400)
}

function goToPage(page) {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  loadProjects()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(loadProjects)
</script>

<style scoped>
.portfolio-page {
  padding: 56px 0 80px;
}

/* Header */
.portfolio-page__header {
  margin-bottom: 36px;
}

.portfolio-page__title {
  font-size: clamp(1.875rem, 4vw, 2.5rem);
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--text);
  margin-bottom: 10px;
}

.portfolio-page__subtitle {
  font-size: 1.0625rem;
  color: var(--text-secondary);
  max-width: 540px;
}

/* Toolbar */
.portfolio-page__toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.portfolio-page__count {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

/* Search */
.search-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.search-wrap__icon {
  position: absolute;
  left: 12px;
  width: 16px;
  height: 16px;
  color: var(--text-secondary);
  pointer-events: none;
}

.search-wrap__input {
  width: 260px;
  padding: 8px 14px 8px 36px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background-color: var(--bg);
  color: var(--text);
  font-family: inherit;
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.15s ease;
}

.search-wrap__input::placeholder {
  color: var(--text-secondary);
}

.search-wrap__input:focus {
  border-color: var(--text);
}

/* Grid */
.portfolio-page__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

/* Skeleton */
.skeleton-project-card {
  border-radius: var(--radius-card);
  border: 1px solid var(--border);
  overflow: hidden;
}

.skeleton-project-card__body {
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--border) 25%,
    var(--bg-secondary) 50%,
    var(--border) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 6px;
}

.skeleton--cover {
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 0;
}

.skeleton--title {
  height: 20px;
  width: 80%;
}

.skeleton--text {
  height: 14px;
  width: 100%;
}

.skeleton--short {
  width: 60%;
}

@keyframes shimmer {
  to { background-position: -200% 0; }
}

/* Error */
.portfolio-page__error {
  text-align: center;
  padding: 48px 0;
  color: var(--text-secondary);
}

.retry-btn {
  margin-top: 12px;
  padding: 8px 20px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: none;
  color: var(--text);
  font-family: inherit;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.retry-btn:hover {
  background-color: var(--bg-secondary);
}

/* Empty */
.portfolio-page__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 80px 0;
  color: var(--text-secondary);
  font-size: 1.0625rem;
}

.portfolio-page__empty svg {
  width: 64px;
  height: 64px;
}


/* Responsive */
@media (max-width: 960px) {
  .portfolio-page__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .portfolio-page__grid {
    grid-template-columns: 1fr;
  }

  .portfolio-page__toolbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-wrap__input {
    width: 100%;
  }

  .search-wrap {
    width: 100%;
  }
}
</style>
