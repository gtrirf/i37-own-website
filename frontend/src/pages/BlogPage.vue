<template>
  <div class="blog-page">
    <div class="container">
      <!-- Header -->
      <header class="blog-page__header">
        <h1 class="blog-page__title">Articles</h1>
        <p class="blog-page__subtitle">
          Thoughts, tutorials, and insights on software development and technology.
        </p>
      </header>

      <!-- Filters -->
      <div class="blog-page__filters">
        <!-- Category pills -->
        <div class="blog-page__categories" role="group" aria-label="Filter by category">
          <CategoryPill
            label="All"
            :active="selectedType === null"
            @click="selectType(null)"
          />
          <CategoryPill
            v-for="bt in blogStore.blogTypes"
            :key="bt.id"
            :label="bt.type_name"
            :active="selectedType === bt.id"
            @click="selectType(bt.id)"
          />
        </div>

        <!-- Search -->
        <div class="blog-page__search">
          <label for="blog-search" class="visually-hidden">Search articles</label>
          <div class="search-wrap">
            <svg class="search-wrap__icon" viewBox="0 0 20 20" fill="none" aria-hidden="true">
              <circle cx="9" cy="9" r="6" stroke="currentColor" stroke-width="1.5"/>
              <path d="m14 14 3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            <input
              id="blog-search"
              v-model="searchQuery"
              type="search"
              placeholder="Search articles…"
              class="search-wrap__input"
              @input="onSearchInput"
            />
          </div>
        </div>
      </div>

      <!-- Error -->
      <div v-if="blogStore.error" class="blog-page__error" role="alert">
        <p>{{ blogStore.error }}</p>
        <button @click="loadBlogs" class="retry-btn">Try again</button>
      </div>

      <!-- Loading skeleton -->
      <div v-else-if="blogStore.loading" class="blog-page__skeleton" aria-busy="true" aria-live="polite">
        <div v-for="n in 5" :key="n" class="skeleton-card">
          <div class="skeleton skeleton--thumb"></div>
          <div class="skeleton-card__body">
            <div class="skeleton skeleton--meta"></div>
            <div class="skeleton skeleton--title"></div>
            <div class="skeleton skeleton--text"></div>
            <div class="skeleton skeleton--text skeleton--short"></div>
          </div>
        </div>
      </div>

      <!-- Article List -->
      <div v-else-if="blogStore.blogs.length" class="blog-page__list">
        <ArticleCard
          v-for="article in blogStore.blogs"
          :key="article.id"
          :article="article"
        />
      </div>

      <!-- Empty state -->
      <div v-else class="blog-page__empty">
        <p>No articles found{{ searchQuery ? ` for "${searchQuery}"` : '' }}.</p>
      </div>

      <!-- Pagination -->
      <Pagination
        :current-page="currentPage"
        :total-pages="totalPages"
        aria-label="Article pagination"
        @change="goToPage"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useBlogStore } from '@/stores/blog.js'
import ArticleCard from '@/components/ui/ArticleCard.vue'
import CategoryPill from '@/components/ui/CategoryPill.vue'
import Pagination from '@/components/ui/Pagination.vue'

const blogStore = useBlogStore()
const selectedType = ref(null)
const searchQuery = ref('')
const currentPage = ref(1)

let searchTimer = null

const PAGE_SIZE = 10

const totalPages = computed(() => {
  return Math.ceil((blogStore.pagination.count || 0) / PAGE_SIZE)
})

async function loadBlogs() {
  await blogStore.fetchBlogs({
    page: currentPage.value,
    search: searchQuery.value.trim(),
    type: selectedType.value
  })
}

function selectType(typeId) {
  selectedType.value = typeId
  currentPage.value = 1
  loadBlogs()
}

function onSearchInput() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    currentPage.value = 1
    loadBlogs()
  }, 400)
}

function goToPage(page) {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  loadBlogs()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(async () => {
  await blogStore.fetchBlogTypes()
  await loadBlogs()
})
</script>

<style scoped>
.blog-page {
  padding: 56px 0 80px;
}

/* Header */
.blog-page__header {
  margin-bottom: 36px;
}

.blog-page__title {
  font-size: clamp(1.875rem, 4vw, 2.5rem);
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--text);
  margin-bottom: 10px;
}

.blog-page__subtitle {
  font-size: 1.0625rem;
  color: var(--text-secondary);
  max-width: 540px;
}

/* Filters */
.blog-page__filters {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.blog-page__categories {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* Search */
.blog-page__search {
  flex-shrink: 0;
}

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
  width: 240px;
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

/* Error */
.blog-page__error {
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

/* Skeleton */
.blog-page__skeleton {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.skeleton-card {
  display: flex;
  gap: 20px;
  padding: 20px 0;
  border-bottom: 1px solid var(--border);
}

.skeleton-card__body {
  flex: 1;
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

.skeleton--thumb {
  width: 140px;
  height: 100px;
  border-radius: 8px;
  flex-shrink: 0;
}

.skeleton--meta {
  height: 16px;
  width: 120px;
}

.skeleton--title {
  height: 22px;
  width: 85%;
}

.skeleton--text {
  height: 14px;
  width: 100%;
}

.skeleton--short {
  width: 65%;
}

@keyframes shimmer {
  to { background-position: -200% 0; }
}

/* Empty */
.blog-page__empty {
  text-align: center;
  padding: 80px 0;
  color: var(--text-secondary);
  font-size: 1.0625rem;
}


@media (max-width: 640px) {
  .blog-page__filters {
    flex-direction: column;
  }

  .search-wrap__input {
    width: 100%;
  }

  .blog-page__search {
    width: 100%;
  }
}
</style>
