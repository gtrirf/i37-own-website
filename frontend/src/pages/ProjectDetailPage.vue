<template>
  <div class="project-detail">
    <div class="container">
      <!-- Back button -->
      <RouterLink to="/portfolio" class="back-link" aria-label="Back to portfolio">
        <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
          <path d="M12 4l-6 6 6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Back to Portfolio
      </RouterLink>

      <!-- Loading -->
      <div v-if="portfolioStore.loading" class="project-detail__loading" aria-live="polite" aria-busy="true">
        <div class="skeleton skeleton--cover"></div>
        <div class="skeleton skeleton--title-lg"></div>
        <div class="skeleton skeleton--meta"></div>
        <div class="skeleton skeleton--body"></div>
        <div class="skeleton skeleton--body"></div>
        <div class="skeleton skeleton--body skeleton--short"></div>
      </div>

      <!-- Error -->
      <div v-else-if="portfolioStore.error" class="project-detail__error" role="alert">
        <p>{{ portfolioStore.error }}</p>
        <RouterLink to="/portfolio" class="back-link">← Back to Portfolio</RouterLink>
      </div>

      <!-- Project -->
      <article v-else-if="project" class="project-detail__article">
        <!-- Cover image -->
        <div
          v-if="coverImage"
          class="project-detail__cover"
          @click="lightbox.open(sortedImages, 0)"
        >
          <img
            :src="coverImage.photo"
            :alt="coverImage.alt_txt || project.title"
            class="project-detail__cover-img"
            loading="eager"
          />
        </div>

        <!-- Header -->
        <header class="project-detail__header">
          <div class="project-detail__meta">
            <time :datetime="project.created_at" class="project-detail__date">
              {{ formattedDate }}
            </time>
            <span class="project-detail__dot" aria-hidden="true">·</span>
            <span class="project-detail__views" aria-label="Views">
              <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
                <path d="M10 4.5C5.5 4.5 2 10 2 10s3.5 5.5 8 5.5 8-5.5 8-5.5-3.5-5.5-8-5.5z" stroke="currentColor" stroke-width="1.5"/>
                <circle cx="10" cy="10" r="2.5" stroke="currentColor" stroke-width="1.5"/>
              </svg>
              {{ project.view_counts ?? 0 }} views
            </span>
          </div>

          <h1 class="project-detail__title">{{ project.title }}</h1>

          <!-- Technologies -->
          <div v-if="technologies.length" class="project-detail__techs" aria-label="Technologies used">
            <TechTag
              v-for="tech in technologies"
              :key="tech.id"
              :name="tech.name"
              :color="tech.color"
            />
          </div>

          <!-- External link -->
          <div v-if="project.url_link" class="project-detail__actions">
            <a
              :href="project.url_link"
              target="_blank"
              rel="noopener noreferrer"
              class="project-detail__ext-btn"
              :aria-label="`Open ${project.title} project`"
            >
              <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
                <path d="M11 3h6v6M17 3l-9 9M8 5H4a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1v-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              View Live Project
            </a>
          </div>
        </header>

        <!-- Content -->
        <div class="project-detail__content">
          <p
            v-for="(paragraph, i) in paragraphs"
            :key="i"
            class="project-detail__paragraph"
          >
            {{ paragraph }}
          </p>
        </div>

        <!-- Images gallery -->
        <div v-if="galleryImages.length" class="project-detail__gallery">
          <h2 class="project-detail__gallery-title">Gallery</h2>
          <div class="project-detail__images">
            <figure
              v-for="(img, i) in galleryImages"
              :key="img.id"
              class="project-detail__figure"
              @click="lightbox.open(sortedImages, i + 1)"
            >
              <img
                :src="img.photo"
                :alt="img.alt_txt || project.title"
                class="project-detail__img"
                loading="lazy"
              />
              <figcaption v-if="img.caption" class="project-detail__caption">
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
import { usePortfolioStore } from '@/stores/portfolio.js'
import TechTag from '@/components/ui/TechTag.vue'
import ImageLightbox from '@/components/ui/ImageLightbox.vue'

const route = useRoute()
const portfolioStore = usePortfolioStore()
const lightbox = ref(null)

const project = computed(() => portfolioStore.currentProject)

const technologies = computed(() => project.value?.technologies || [])

const paragraphs = computed(() => {
  const content = project.value?.content || ''
  return content.split(/\n+/).filter(p => p.trim())
})

const sortedImages = computed(() => {
  return [...(project.value?.images || [])].sort((a, b) => (a.sort_order ?? 0) - (b.sort_order ?? 0))
})

// Cover image is the first image in sort order
const coverImage = computed(() => sortedImages.value[0] ?? null)

// Gallery shows all images after the cover (or all if no cover needed as separate cover)
const galleryImages = computed(() => {
  const imgs = sortedImages.value
  // Show all images in gallery section; cover is already shown above
  return imgs.length > 1 ? imgs.slice(1) : []
})

const formattedDate = computed(() => {
  if (!project.value?.created_at) return ''
  return new Date(project.value.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

async function load() {
  await portfolioStore.fetchProject(route.params.id)
  if (project.value?.title) {
    document.title = `${project.value.title} — i37`
  }
}

onMounted(load)
watch(() => route.params.id, load)
</script>

<style scoped>
.project-detail {
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
.project-detail__loading {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 800px;
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
  border-radius: var(--radius-card);
}

.skeleton--title-lg {
  height: 48px;
  width: 85%;
}

.skeleton--meta {
  height: 18px;
  width: 220px;
}

.skeleton--body {
  height: 16px;
  width: 100%;
}

.skeleton--short {
  width: 68%;
}

@keyframes shimmer {
  to { background-position: -200% 0; }
}

/* Error */
.project-detail__error {
  text-align: center;
  padding: 80px 0;
  color: var(--text-secondary);
}

/* Article */
.project-detail__article {
  max-width: 800px;
}

/* Cover image */
.project-detail__cover {
  width: 100%;
  border-radius: var(--radius-card);
  overflow: hidden;
  border: 1px solid var(--border);
  margin-bottom: 36px;
  aspect-ratio: 16 / 9;
  background-color: var(--bg-secondary);
  cursor: zoom-in;
}

.project-detail__cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Header */
.project-detail__header {
  margin-bottom: 36px;
}

.project-detail__meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 14px;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.project-detail__dot {
  color: var(--border);
}

.project-detail__date {
  color: var(--text-secondary);
}

.project-detail__views {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.project-detail__views svg {
  width: 14px;
  height: 14px;
}

.project-detail__title {
  font-size: clamp(1.75rem, 4vw, 2.375rem);
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.2;
  color: var(--text);
  margin-bottom: 20px;
}

/* Technologies */
.project-detail__techs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 24px;
}

/* External link */
.project-detail__actions {
  margin-top: 4px;
}

.project-detail__ext-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background-color: transparent;
  color: var(--text);
  font-family: inherit;
  font-size: 0.9375rem;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
}

.project-detail__ext-btn:hover {
  background-color: var(--accent);
  border-color: var(--accent);
  color: var(--bg);
  transform: translateY(-1px);
}

.project-detail__ext-btn svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

/* Content */
.project-detail__content {
  margin-bottom: 48px;
}

.project-detail__paragraph {
  font-size: 1.0625rem;
  line-height: 1.8;
  color: var(--text);
  margin-bottom: 20px;
}

.project-detail__paragraph:last-child {
  margin-bottom: 0;
}

/* Gallery */
.project-detail__gallery {
  border-top: 1px solid var(--border);
  padding-top: 40px;
}

.project-detail__gallery-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: var(--text);
}

.project-detail__images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.project-detail__figure {
  border-radius: var(--radius-card);
  overflow: hidden;
  border: 1px solid var(--border);
  cursor: zoom-in;
}

.project-detail__img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  display: block;
}

.project-detail__caption {
  padding: 10px 14px;
  font-size: 0.8125rem;
  color: var(--text-secondary);
  background-color: var(--bg-secondary);
  font-style: italic;
}

@media (max-width: 560px) {
  .project-detail__images {
    grid-template-columns: 1fr;
  }

  .project-detail__cover {
    border-radius: 8px;
  }
}
</style>
