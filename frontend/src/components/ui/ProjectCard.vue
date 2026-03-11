<template>
  <article class="project-card">
    <RouterLink :to="`/portfolio/${project.id}`" class="project-card__inner" :aria-label="`View project: ${project.title}`">
      <!-- Cover Image -->
      <div class="project-card__cover">
        <img
          v-if="project.first_image?.photo"
          :src="project.first_image.photo"
          :alt="project.first_image.alt_txt || project.title"
          class="project-card__img"
          loading="lazy"
        />
        <div v-else class="project-card__img-placeholder" aria-hidden="true">
          <svg viewBox="0 0 48 48" fill="none">
            <rect width="48" height="48" rx="8" fill="currentColor" opacity="0.06"/>
            <path d="M8 36l10-12 7 8 9-11 14 15H8z" fill="currentColor" opacity="0.2"/>
            <circle cx="16" cy="16" r="4" fill="currentColor" opacity="0.2"/>
          </svg>
        </div>
      </div>

      <!-- Body -->
      <div class="project-card__body">
        <h3 class="project-card__title">{{ project.title }}</h3>
        <p class="project-card__desc">{{ excerpt }}</p>

        <!-- Tech Tags -->
        <div v-if="technologies.length" class="project-card__techs" aria-label="Technologies">
          <span class="project-card__tech-list">
            {{ techString }}
          </span>
        </div>

        <!-- Meta -->
        <div class="project-card__footer">
          <time :datetime="project.created_at" class="project-card__date">
            {{ formattedDate }}
          </time>
          <span class="project-card__views" aria-label="Views">
            <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
              <path d="M10 4.5C5.5 4.5 2 10 2 10s3.5 5.5 8 5.5 8-5.5 8-5.5-3.5-5.5-8-5.5z" stroke="currentColor" stroke-width="1.5"/>
              <circle cx="10" cy="10" r="2.5" stroke="currentColor" stroke-width="1.5"/>
            </svg>
            {{ project.view_counts ?? 0 }}
          </span>
        </div>
      </div>
    </RouterLink>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  project: {
    type: Object,
    required: true
  }
})

const excerpt = computed(() => {
  const text = props.project.content || ''
  return text.length > 120 ? text.slice(0, 120).trimEnd() + '…' : text
})

const technologies = computed(() => props.project.technologies || [])

const techString = computed(() => {
  return technologies.value.map(t => t.name?.toUpperCase()).join(' • ')
})

const formattedDate = computed(() => {
  if (!props.project.created_at) return ''
  return new Date(props.project.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
})
</script>

<style scoped>
.project-card {
  border-radius: var(--radius-card);
  border: 1px solid var(--border);
  background-color: var(--card-bg);
  overflow: hidden;
  transition: box-shadow 0.25s ease, transform 0.25s ease;
}

.project-card:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-3px);
}

.project-card__inner {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
  height: 100%;
}

/* Cover */
.project-card__cover {
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background-color: var(--bg-secondary);
}

.project-card__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.35s ease;
}

.project-card:hover .project-card__img {
  transform: scale(1.04);
}

.project-card__img-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.project-card__img-placeholder svg {
  width: 64px;
  height: 64px;
}

/* Body */
.project-card__body {
  padding: 18px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.project-card__title {
  font-size: 1.0625rem;
  font-weight: 700;
  line-height: 1.35;
  color: var(--text);
}

.project-card__inner:hover .project-card__title {
  text-decoration: underline;
  text-underline-offset: 2px;
}

.project-card__desc {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.55;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.project-card__techs {
  margin-top: 4px;
}

.project-card__tech-list {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--text-secondary);
}

.project-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
  padding-top: 8px;
  border-top: 1px solid var(--border);
}

.project-card__date,
.project-card__views {
  font-size: 0.8125rem;
  color: var(--text-secondary);
}

.project-card__views {
  display: flex;
  align-items: center;
  gap: 4px;
}

.project-card__views svg {
  width: 14px;
  height: 14px;
}
</style>
