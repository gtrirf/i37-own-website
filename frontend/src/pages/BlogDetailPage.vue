<template>
  <div class="blog-detail">
    <div class="container">
      <!-- Back button -->
      <RouterLink to="/blog" class="back-link" aria-label="Back to articles">
        <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
          <path d="M12 4l-6 6 6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Back to Articles
      </RouterLink>

      <!-- Loading -->
      <div v-if="blogStore.loading" class="blog-detail__loading" aria-live="polite" aria-busy="true">
        <div class="skeleton skeleton--title-lg"></div>
        <div class="skeleton skeleton--meta"></div>
        <div class="skeleton skeleton--body"></div>
        <div class="skeleton skeleton--body"></div>
        <div class="skeleton skeleton--body skeleton--short"></div>
      </div>

      <!-- Error -->
      <div v-else-if="blogStore.error" class="blog-detail__error" role="alert">
        <p>{{ blogStore.error }}</p>
        <RouterLink to="/blog" class="back-link">← Back to Articles</RouterLink>
      </div>

      <!-- Article -->
      <article v-else-if="blog" class="blog-detail__article">
        <!-- Meta -->
        <header class="blog-detail__header">
          <div class="blog-detail__meta">
            <span v-if="blog.blog_type" class="blog-detail__category">
              {{ blog.blog_type.type_name?.toUpperCase() }}
            </span>
            <span class="blog-detail__dot" aria-hidden="true">·</span>
            <time :datetime="blog.created_at" class="blog-detail__date">
              {{ formattedDate }}
            </time>
            <span class="blog-detail__dot" aria-hidden="true">·</span>
            <span class="blog-detail__read-time">{{ readTime }} min read</span>
            <span class="blog-detail__dot" aria-hidden="true">·</span>
            <span class="blog-detail__views" aria-label="Views">
              <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
                <path d="M10 4.5C5.5 4.5 2 10 2 10s3.5 5.5 8 5.5 8-5.5 8-5.5-3.5-5.5-8-5.5z" stroke="currentColor" stroke-width="1.5"/>
                <circle cx="10" cy="10" r="2.5" stroke="currentColor" stroke-width="1.5"/>
              </svg>
              {{ blog.view_counts ?? 0 }} views
            </span>
          </div>

          <h1 class="blog-detail__title">{{ blog.title }}</h1>

          <div v-if="blog.updated_at && blog.updated_at !== blog.created_at" class="blog-detail__updated">
            Updated {{ formattedUpdatedDate }}
          </div>
        </header>

        <!-- Content -->
        <div class="blog-detail__content">
          <p
            v-for="(paragraph, i) in paragraphs"
            :key="i"
            class="blog-detail__paragraph"
          >
            {{ paragraph }}
          </p>
        </div>

        <!-- Images gallery -->
        <div v-if="blog.images && blog.images.length" class="blog-detail__gallery">
          <h2 class="blog-detail__gallery-title">Gallery</h2>
          <div class="blog-detail__images">
            <figure
              v-for="(img, i) in sortedImages"
              :key="img.id"
              class="blog-detail__figure"
              @click="lightbox.open(sortedImages, i)"
            >
              <img
                :src="img.photo"
                :alt="img.alt_txt || blog.title"
                class="blog-detail__img"
                loading="lazy"
              />
              <figcaption v-if="img.caption" class="blog-detail__caption">
                {{ img.caption }}
              </figcaption>
            </figure>
          </div>
        </div>

        <ImageLightbox ref="lightbox" />
      </article>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useBlogStore } from '@/stores/blog.js'
import ImageLightbox from '@/components/ui/ImageLightbox.vue'

const route = useRoute()
const blogStore = useBlogStore()
const lightbox = ref(null)

const blog = computed(() => blogStore.currentBlog)

const paragraphs = computed(() => {
  const content = blog.value?.content || ''
  return content.split(/\n+/).filter(p => p.trim())
})

const sortedImages = computed(() => {
  return [...(blog.value?.images || [])].sort((a, b) => (a.sort_order ?? 0) - (b.sort_order ?? 0))
})

const readTime = computed(() => {
  const words = (blog.value?.content || '').split(/\s+/).filter(Boolean).length
  return Math.max(1, Math.ceil(words / 200))
})

const formattedDate = computed(() => {
  if (!blog.value?.created_at) return ''
  return new Date(blog.value.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

const formattedUpdatedDate = computed(() => {
  if (!blog.value?.updated_at) return ''
  return new Date(blog.value.updated_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

async function load() {
  await blogStore.fetchBlog(route.params.id)
  if (blog.value?.title) {
    document.title = `${blog.value.title} — i37`
  }
}

onMounted(load)
watch(() => route.params.id, load)
</script>

<style scoped>
.blog-detail {
  padding: 40px 0 80px;
}

/* Back link */
.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 6px 0;
  margin-bottom: 32px;
  transition: color 0.15s ease;
}

.back-link:hover {
  color: var(--text);
}

.back-link svg {
  width: 18px;
  height: 18px;
}

/* Loading skeletons */
.blog-detail__loading {
  display: flex;
  flex-direction: column;
  gap: 14px;
  max-width: 720px;
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

.skeleton--title-lg {
  height: 48px;
  width: 90%;
}

.skeleton--meta {
  height: 18px;
  width: 280px;
}

.skeleton--body {
  height: 16px;
  width: 100%;
}

.skeleton--short {
  width: 70%;
}

@keyframes shimmer {
  to { background-position: -200% 0; }
}

/* Error */
.blog-detail__error {
  text-align: center;
  padding: 80px 0;
  color: var(--text-secondary);
}

/* Article */
.blog-detail__article {
  max-width: 720px;
}

.blog-detail__header {
  margin-bottom: 40px;
}

.blog-detail__meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 16px;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.blog-detail__category {
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--text);
  background-color: var(--bg-secondary);
  padding: 3px 10px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--border);
}

.blog-detail__dot {
  color: var(--border);
}

.blog-detail__views {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.blog-detail__views svg {
  width: 14px;
  height: 14px;
}

.blog-detail__title {
  font-size: clamp(1.75rem, 4vw, 2.375rem);
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.2;
  color: var(--text);
  margin-bottom: 8px;
}

.blog-detail__updated {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  font-style: italic;
}

/* Content */
.blog-detail__content {
  margin-bottom: 48px;
}

.blog-detail__paragraph {
  font-size: 1.0625rem;
  line-height: 1.8;
  color: var(--text);
  margin-bottom: 20px;
}

.blog-detail__paragraph:last-child {
  margin-bottom: 0;
}

/* Gallery */
.blog-detail__gallery {
  border-top: 1px solid var(--border);
  padding-top: 40px;
}

.blog-detail__gallery-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: var(--text);
}

.blog-detail__images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.blog-detail__figure {
  border-radius: var(--radius-card);
  overflow: hidden;
  border: 1px solid var(--border);
  cursor: zoom-in;
}

.blog-detail__img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  display: block;
}

.blog-detail__caption {
  padding: 10px 14px;
  font-size: 0.8125rem;
  color: var(--text-secondary);
  background-color: var(--bg-secondary);
  font-style: italic;
}

@media (max-width: 560px) {
  .blog-detail__images {
    grid-template-columns: 1fr;
  }
}
</style>
