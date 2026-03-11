<template>
  <article class="article-card">
    <RouterLink :to="`/blog/${article.id}`" class="article-card__link" :aria-label="`Read: ${article.title}`">
      <!-- Thumbnail -->
      <div class="article-card__thumb">
        <img
          v-if="article.first_image?.photo"
          :src="article.first_image.photo"
          :alt="article.first_image.alt_txt || article.title"
          class="article-card__img"
          loading="lazy"
        />
        <div v-else class="article-card__img-placeholder" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none">
            <rect width="24" height="24" rx="4" fill="currentColor" opacity="0.08"/>
            <path d="M4 16l4-4 3 3 4-5 5 6H4z" fill="currentColor" opacity="0.3"/>
            <circle cx="8.5" cy="8.5" r="1.5" fill="currentColor" opacity="0.3"/>
          </svg>
        </div>
      </div>

      <!-- Content -->
      <div class="article-card__body">
        <div class="article-card__meta">
          <span v-if="article.blog_type" class="article-card__category">
            {{ article.blog_type.type_name?.toUpperCase() }}
          </span>
          <span class="article-card__dot" aria-hidden="true">·</span>
          <span class="article-card__read-time">{{ readTime }} min read</span>
        </div>

        <h3 class="article-card__title">{{ article.title }}</h3>
        <p class="article-card__excerpt">{{ excerpt }}</p>

        <div class="article-card__footer">
          <time :datetime="article.created_at" class="article-card__date">
            {{ formattedDate }}
          </time>
          <span class="article-card__views" aria-label="Views">
            <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
              <path d="M10 4.5C5.5 4.5 2 10 2 10s3.5 5.5 8 5.5 8-5.5 8-5.5-3.5-5.5-8-5.5z" stroke="currentColor" stroke-width="1.5"/>
              <circle cx="10" cy="10" r="2.5" stroke="currentColor" stroke-width="1.5"/>
            </svg>
            {{ article.view_counts ?? 0 }}
          </span>
        </div>
      </div>
    </RouterLink>
    <div class="article-card__divider" aria-hidden="true"></div>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  article: {
    type: Object,
    required: true
  }
})

const excerpt = computed(() => {
  const text = props.article.content || ''
  return text.length > 120 ? text.slice(0, 120).trimEnd() + '…' : text
})

const readTime = computed(() => {
  const words = (props.article.content || '').split(/\s+/).filter(Boolean).length
  return Math.max(1, Math.ceil(words / 200))
})

const formattedDate = computed(() => {
  if (!props.article.created_at) return ''
  return new Date(props.article.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
})
</script>

<style scoped>
.article-card {
  display: flex;
  flex-direction: column;
}

.article-card__link {
  display: flex;
  gap: 20px;
  padding: 20px 0;
  text-decoration: none;
  color: inherit;
  border-radius: var(--radius-card);
  transition: background-color 0.15s ease;
}

.article-card__link:hover .article-card__title {
  text-decoration: underline;
  text-underline-offset: 2px;
}

/* Thumbnail */
.article-card__thumb {
  flex-shrink: 0;
  width: 140px;
  height: 100px;
  border-radius: 8px;
  overflow: hidden;
  background-color: var(--bg-secondary);
}

.article-card__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}

.article-card__link:hover .article-card__img {
  transform: scale(1.03);
}

.article-card__img-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.article-card__img-placeholder svg {
  width: 48px;
  height: 48px;
}

/* Body */
.article-card__body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.article-card__meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
}

.article-card__category {
  font-weight: 600;
  letter-spacing: 0.06em;
  color: var(--text);
  background-color: var(--bg-secondary);
  padding: 2px 8px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--border);
}

.article-card__dot {
  color: var(--text-secondary);
}

.article-card__read-time {
  color: var(--text-secondary);
}

.article-card__title {
  font-size: 1.0625rem;
  font-weight: 700;
  line-height: 1.35;
  color: var(--text);
  white-space: normal;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.article-card__excerpt {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.55;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.article-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
  padding-top: 4px;
}

.article-card__date,
.article-card__views {
  font-size: 0.8125rem;
  color: var(--text-secondary);
}

.article-card__views {
  display: flex;
  align-items: center;
  gap: 4px;
}

.article-card__views svg {
  width: 14px;
  height: 14px;
}

.article-card__divider {
  height: 1px;
  background-color: var(--border);
}

.article-card:last-child .article-card__divider {
  display: none;
}

@media (max-width: 560px) {
  .article-card__link {
    flex-direction: column;
    gap: 14px;
  }

  .article-card__thumb {
    width: 100%;
    height: 180px;
  }
}
</style>
