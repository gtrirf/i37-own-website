<template>
  <div class="home">
    <!-- ── Hero Section ──────────────────────────────────────── -->
    <section class="hero container">
      <div class="hero__grid">
        <!-- Avatar -->
        <div class="hero__avatar-wrap">
          <div class="hero__avatar">
            <img
              v-if="mainInfo?.photo"
              :src="mainInfo.photo"
              :alt="mainInfo.name || 'Islombek Ravshanov'"
              class="hero__avatar-img"
            />
            <div v-else class="hero__avatar-placeholder" aria-hidden="true">
              <svg viewBox="0 0 80 80" fill="none">
                <circle cx="40" cy="40" r="40" fill="currentColor" opacity="0.08"/>
                <circle cx="40" cy="32" r="14" fill="currentColor" opacity="0.2"/>
                <path d="M12 72c0-15.464 12.536-28 28-28s28 12.536 28 28" fill="currentColor" opacity="0.15"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- Text content -->
        <div class="hero__content">
          <p class="hero__label">HELLO, I'M</p>
          <h1 class="hero__name">{{ mainInfo?.name || 'Islombek Ravshanov' }}</h1>
          <p class="hero__bio">{{ mainInfo?.text || 'Software engineer and developer based in Uzbekistan.' }}</p>

          <!-- CTA Buttons -->
          <div class="hero__ctas">
            <RouterLink to="/" class="btn btn--filled">Me</RouterLink>
            <RouterLink to="/blog" class="btn btn--outline">Blogs</RouterLink>
            <a
              href="https://team.i37.uz"
              target="_blank"
              rel="noopener noreferrer"
              class="btn btn--outline"
              >
              My Team
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </a>
          </div>

          <!-- Social Links -->
          <div v-if="socialLinks.length" class="hero__socials">
            <a
              v-for="link in visibleSocials"
              :key="link.id"
              :href="link.url"
              target="_blank"
              rel="noopener noreferrer"
              class="hero__social"
            >
              <span class="hero__social-icon" aria-hidden="true" v-html="getSocialSvg(link.app)"></span>
              <span class="hero__social-label">{{ getPlatformLabel(link.app) }}</span>
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Career Section ────────────────────────────────────── -->
    <section v-if="career.length" class="career">
      <div class="container">
        <div class="career__divider">
          <span class="career__divider-label">CAREER, EXPERIENCE &amp; EDUCATION</span>
        </div>
      </div>
      <div class="career__marquee">
        <div class="career__track">
          <a
            v-for="item in carouselItems"
            :key="item._key"
            :href="item.name"
            target="_blank"
            rel="noopener noreferrer"
            class="career__item"
          >
            <img
              v-if="item.logo"
              :src="item.logo"
              :alt="item.name"
              class="career__logo"
              loading="lazy"
            />
            <span v-else class="career__name">{{ item.name }}</span>
          </a>
        </div>
      </div>
    </section>

    <!-- Loading state -->
    <div v-if="loading" class="home__loading container" aria-live="polite">
      <div class="spinner" aria-label="Loading"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getMainInfo, getCareer, getSocialLinks } from '@/api/index.js'

const mainInfo = ref(null)
const career = ref([])
const socialLinks = ref([])
const loading = ref(true)

const carouselItems = computed(() => {
  const items = career.value
  if (!items.length) return []

  const ITEM_WIDTH = 300
  const setWidth = items.length * ITEM_WIDTH
  const viewportWidth = typeof window !== 'undefined' ? window.innerWidth : 1440

  // Half the total track must be wider than the viewport (no gaps)
  // numCopies * setWidth / 2 > viewportWidth  →  numCopies > 2 * viewportWidth / setWidth
  const minCopies = Math.max(4, Math.ceil((viewportWidth * 2) / setWidth) + 1)

  const result = []
  for (let i = 0; i < minCopies; i++) {
    items.forEach(item => result.push({ ...item, _key: `copy${i}-${item.id}` }))
  }
  return result
})

const SOCIAL_ORDER = ['telegram', 'instagram', 'linkedin', 'x', 'youtube', 'github']

const visibleSocials = computed(() => {
  const order = SOCIAL_ORDER
  return [...socialLinks.value].sort(
    (a, b) => order.indexOf(a.app) - order.indexOf(b.app)
  )
})

function getPlatformLabel(app) {
  const labels = {
    telegram: 'Telegram',
    instagram: 'Instagram',
    linkedin: 'LinkedIn',
    x: 'X',
    youtube: 'YouTube',
    github: 'GitHub'
  }
  return labels[app] || app
}

const svgPaths = {
  telegram: '<path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.248-1.97 9.289c-.145.658-.537.818-1.084.508l-3-2.21-1.447 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.12l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.461c.537-.194 1.006.131.833.932z" fill="currentColor"/>',
  instagram: '<path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z" fill="currentColor"/>',
  linkedin: '<path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" fill="currentColor"/>',
  x: '<path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.746l7.73-8.835L1.254 2.25H8.08l4.258 5.63 5.906-5.63zm-1.161 17.52h1.833L7.084 4.126H5.117z" fill="currentColor"/>',
  youtube: '<path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" fill="currentColor"/>',
  github: '<path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" fill="currentColor"/>'
}

function getSocialSvg(app) {
  const path = svgPaths[app] || ''
  return `<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">${path}</svg>`
}

onMounted(async () => {
  loading.value = true
  try {
    const [infoRes, careerRes, socialRes] = await Promise.allSettled([
      getMainInfo(),
      getCareer(),
      getSocialLinks()
    ])

    if (infoRes.status === 'fulfilled') {
      const data = infoRes.value.data
      mainInfo.value = Array.isArray(data) ? data[0] : data
    }
    if (careerRes.status === 'fulfilled') {
      const data = careerRes.value.data
      career.value = Array.isArray(data) ? data : (data?.results ?? [])
    }
    if (socialRes.status === 'fulfilled') {
      const data = socialRes.value.data
      socialLinks.value = Array.isArray(data) ? data : (data?.results ?? [])
    }
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.home {
  padding-bottom: 64px;
}

/* ── Hero ─────────────────────────────────────────────────── */
.hero {
  padding-top: 80px;
  padding-bottom: 64px;
}

.hero__grid {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 56px;
  align-items: center;
}

/* Avatar */
.hero__avatar-wrap {
  display: flex;
  justify-content: center;
}

.hero__avatar {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid var(--border);
  background-color: var(--bg-secondary);
  flex-shrink: 0;
}

.hero__avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.hero__avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.hero__avatar-placeholder svg {
  width: 100px;
  height: 100px;
}

/* Text */
.hero__content {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.hero__label {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #0d7cd6;
}

.hero__name {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.1;
  color: var(--text);
}

.hero__bio {
  font-size: 1.0625rem;
  color: var(--text-secondary);
  line-height: 1.65;
  max-width: 520px;
}

/* CTA Buttons */
.hero__ctas {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 6px;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 22px;
  border-radius: 999px;
  font-size: 0.9375rem;
  font-weight: 600;
  font-family: inherit;
  text-decoration: none;
  cursor: pointer;
  transition:
    background-color 0.3s cubic-bezier(0.4, 0, 0.2, 1),
    color 0.3s cubic-bezier(0.4, 0, 0.2, 1),
    border-color 0.3s cubic-bezier(0.4, 0, 0.2, 1),
    transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn svg {
  transition: stroke 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn:hover {
  transform: translateY(-2px);
}

.btn--filled {
  background-color: var(--accent);
  color: var(--bg);
  border: 1px solid var(--accent);
}

.btn--filled:hover {
  background-color: transparent;
  color: var(--accent);
  border-color: var(--accent);
}

.btn--outline {
  background-color: transparent;
  color: var(--text);
  border: 1px solid var(--border);
}

.btn--outline:hover {
  background-color: var(--accent);
  color: var(--bg);
  border-color: var(--accent);
}

/* Social Links */
.hero__socials {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 6px;
}

.hero__social {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 6px 0;
  transition: color 0.15s ease;
}

.hero__social:hover {
  color: var(--text);
}

.hero__social-icon {
  display: flex;
  align-items: center;
}

.hero__social-icon :deep(svg) {
  width: 18px;
  height: 18px;
}

.hero__social-label {
  line-height: 1;
}
/* ── Career ───────────────────────────────────────────────── */
.career {
  padding: 48px 0;
}

.career__divider {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 36px;
}

.career__divider::before,
.career__divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background-color: var(--border);
}

.career__divider-label {
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: var(--text-secondary);
  white-space: nowrap;
}

/* Carousel */
.career__marquee {
  overflow: hidden;
  background-color: #ffffff;
  padding: 35px 0;
  -webkit-mask-image: linear-gradient(to right, transparent, black 8%, black 92%, transparent);
  mask-image: linear-gradient(to right, transparent, black 8%, black 92%, transparent);
}

:global(.dark) .career__marquee {
  background-color: #ffffff;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}

.career__marquee:hover .career__track {
  animation-play-state: paused;
}

.career__track {
  display: flex;
  align-items: center;
  width: max-content;
  animation: carousel-scroll 50s linear infinite;
  will-change: transform;
}

@keyframes carousel-scroll {
  from { transform: translateX(-50%); }
  to   { transform: translateX(0); }
}

.career__item {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 48px;
  height: 52px;
  text-decoration: none;
  cursor: pointer;
  border-right: 1px solid #e2e8f0;
}

.career__logo {
  height: 100px;
  width: 300px;
  object-fit: contain;
  display: block;
  filter: grayscale(0%) opacity(1);
  transition: filter 0.25s ease;
}

/* .career__item:hover .career__logo {
  filter: grayscale(0%) opacity(1);
} */

.career__name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #94a3b8;
  white-space: nowrap;
}
/* ── Loading ──────────────────────────────────────────────── */
.home__loading {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border);
  border-top-color: var(--text);
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ── Responsive ───────────────────────────────────────────── */
@media (max-width: 768px) {
  .hero__grid {
    grid-template-columns: 1fr;
    gap: 32px;
    text-align: center;
  }

  .hero__avatar-wrap {
    justify-content: center;
  }

  .hero__bio {
    max-width: 100%;
  }

  .hero__ctas {
    justify-content: center;
  }

  .hero__socials {
    justify-content: center;
  }

  .hero__label {
    text-align: center;
  }
}

@media (max-width: 480px) {
  .hero {
    padding-top: 48px;
    padding-bottom: 40px;
  }

  .hero__avatar {
    width: 160px;
    height: 160px;
  }
}
</style>
