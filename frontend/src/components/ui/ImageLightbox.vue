<template>
  <Teleport to="body">
    <Transition name="lightbox">
      <div
        v-if="isOpen"
        class="lightbox"
        role="dialog"
        aria-modal="true"
        aria-label="Image viewer"
        @click.self="onBackdropClick"
        @touchstart="onTouchStart"
        @touchmove="onTouchMove"
        @touchend="onTouchEnd"
      >
        <!-- Close -->
        <button class="lightbox__close" @click="close" aria-label="Close">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>

        <!-- Counter -->
        <div v-if="images.length > 1" class="lightbox__counter">
          {{ currentIndex + 1 }} / {{ images.length }}
        </div>

        <!-- Left side zone -->
        <div
          v-if="images.length > 1"
          class="lightbox__side lightbox__side--prev"
          @click.stop="prev"
          aria-label="Previous image"
        >
          <button class="lightbox__nav" tabindex="-1" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>

        <!-- Image -->
        <Transition :name="slideDir" mode="out-in">
          <div :key="currentIndex" class="lightbox__content" @click.stop>
            <img
              :src="images[currentIndex]?.photo"
              :alt="images[currentIndex]?.alt_txt || ''"
              class="lightbox__img"
              :class="{ 'lightbox__img--zoomed': scale > 1, 'lightbox__img--pinching': isPinching, 'lightbox__img--dragging': isDragging }"
              :style="imgStyle"
              draggable="false"
              @mousedown.prevent="onMouseDown"
            />
            <p v-if="images[currentIndex]?.caption" class="lightbox__caption">
              {{ images[currentIndex].caption }}
            </p>
          </div>
        </Transition>

        <!-- Right side zone -->
        <div
          v-if="images.length > 1"
          class="lightbox__side lightbox__side--next"
          @click.stop="next"
          aria-label="Next image"
        >
          <button class="lightbox__nav" tabindex="-1" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const isOpen = ref(false)
const images = ref([])
const currentIndex = ref(0)
const slideDir = ref('slide-next')

// Zoom & pan state
const scale = ref(1)
const panX = ref(0)
const panY = ref(0)
const isPinching = ref(false)
const isDragging = ref(false)

const imgStyle = computed(() => ({
  transform: `scale(${scale.value}) translate(${panX.value / scale.value}px, ${panY.value / scale.value}px)`,
}))

// Touch tracking
let touchStartX = 0
let touchStartY = 0
let touchStartTime = 0
let initialPinchDist = 0
let initialScale = 1
let panOriginX = 0
let panOriginY = 0
let panStartPanX = 0
let panStartPanY = 0
let didSwipe = false

function getTouchDist(touches) {
  const dx = touches[0].clientX - touches[1].clientX
  const dy = touches[0].clientY - touches[1].clientY
  return Math.sqrt(dx * dx + dy * dy)
}

function resetZoom() {
  scale.value = 1
  panX.value = 0
  panY.value = 0
}

function open(imgs, index = 0) {
  images.value = imgs
  currentIndex.value = index
  isOpen.value = true
  resetZoom()
  document.body.style.overflow = 'hidden'
}

function close() {
  isOpen.value = false
  resetZoom()
  document.body.style.overflow = ''
}

function onBackdropClick() {
  if (didSwipe) return
  close()
}

function prev() {
  if (images.value.length < 2) return
  slideDir.value = 'slide-prev'
  currentIndex.value = (currentIndex.value - 1 + images.value.length) % images.value.length
  resetZoom()
}

function next() {
  if (images.value.length < 2) return
  slideDir.value = 'slide-next'
  currentIndex.value = (currentIndex.value + 1) % images.value.length
  resetZoom()
}

// ── Touch handlers ──────────────────────────────────────────
function onTouchStart(e) {
  didSwipe = false

  if (e.touches.length === 2) {
    isPinching.value = true
    initialPinchDist = getTouchDist(e.touches)
    initialScale = scale.value
  } else if (e.touches.length === 1) {
    touchStartX = e.touches[0].clientX
    touchStartY = e.touches[0].clientY
    touchStartTime = Date.now()
    panOriginX = e.touches[0].clientX
    panOriginY = e.touches[0].clientY
    panStartPanX = panX.value
    panStartPanY = panY.value
  }
}

function onTouchMove(e) {
  if (e.touches.length === 2) {
    e.preventDefault()
    const dist = getTouchDist(e.touches)
    scale.value = Math.min(5, Math.max(1, initialScale * (dist / initialPinchDist)))
  } else if (e.touches.length === 1 && scale.value > 1) {
    e.preventDefault()
    panX.value = panStartPanX + (e.touches[0].clientX - panOriginX)
    panY.value = panStartPanY + (e.touches[0].clientY - panOriginY)
  }
}

function onTouchEnd(e) {
  if (isPinching.value) {
    isPinching.value = false
    if (scale.value <= 1.05) resetZoom()
    return
  }

  const endX = e.changedTouches[0].clientX
  const endY = e.changedTouches[0].clientY
  const dx = endX - touchStartX
  const dy = endY - touchStartY
  const dt = Date.now() - touchStartTime

  // Single tap while zoomed → reset zoom
  if (scale.value > 1 && dt < 250 && Math.abs(dx) < 12 && Math.abs(dy) < 12) {
    resetZoom()
    return
  }

  // Swipe navigation (only when not zoomed)
  if (scale.value <= 1 && Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy)) {
    didSwipe = true
    dx < 0 ? next() : prev()
    setTimeout(() => { didSwipe = false }, 300)
  }
}

// ── Keyboard ────────────────────────────────────────────────
function onKeydown(e) {
  if (!isOpen.value) return
  if (e.key === 'Escape') close()
  if (e.key === 'ArrowLeft') prev()
  if (e.key === 'ArrowRight') next()
}

// ── Mouse drag pan (desktop) ─────────────────────────────────
let dragStartX = 0
let dragStartY = 0
let dragStartPanX = 0
let dragStartPanY = 0

function onMouseDown(e) {
  if (scale.value <= 1) return
  isDragging.value = true
  dragStartX = e.clientX
  dragStartY = e.clientY
  dragStartPanX = panX.value
  dragStartPanY = panY.value
  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
}

function onMouseMove(e) {
  if (!isDragging.value) return
  panX.value = dragStartPanX + (e.clientX - dragStartX)
  panY.value = dragStartPanY + (e.clientY - dragStartY)
}

function onMouseUp() {
  isDragging.value = false
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', onMouseUp)
}

// ── Mouse wheel zoom (desktop) ───────────────────────────────
function onWheel(e) {
  if (!isOpen.value) return
  e.preventDefault()

  const oldScale = scale.value
  const delta = e.deltaY > 0 ? -0.15 : 0.15
  const newScale = Math.min(5, Math.max(1, oldScale + delta))

  if (newScale === oldScale) return

  // Mouse position relative to viewport center (image center)
  const mx = e.clientX - window.innerWidth / 2
  const my = e.clientY - window.innerHeight / 2

  // Keep the point under cursor fixed
  panX.value = mx - (mx - panX.value) * (newScale / oldScale)
  panY.value = my - (my - panY.value) * (newScale / oldScale)
  scale.value = newScale

  if (scale.value <= 1) resetZoom()
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
  window.addEventListener('wheel', onWheel, { passive: false })
})
onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
  window.removeEventListener('wheel', onWheel)
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', onMouseUp)
  document.body.style.overflow = ''
})

defineExpose({ open, close })
</script>

<style scoped>
.lightbox {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.78);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  padding: 56px 80px 24px;
  touch-action: none;
}

/* Overlay transition */
.lightbox-enter-active,
.lightbox-leave-active { transition: opacity 0.2s ease; }
.lightbox-enter-from,
.lightbox-leave-to     { opacity: 0; }

/* Slide next */
.slide-next-enter-active,
.slide-next-leave-active { transition: opacity 0.18s ease, transform 0.18s ease; }
.slide-next-enter-from   { opacity: 0; transform: translateX(40px); }
.slide-next-leave-to     { opacity: 0; transform: translateX(-40px); }

/* Slide prev */
.slide-prev-enter-active,
.slide-prev-leave-active { transition: opacity 0.18s ease, transform 0.18s ease; }
.slide-prev-enter-from   { opacity: 0; transform: translateX(-40px); }
.slide-prev-leave-to     { opacity: 0; transform: translateX(40px); }

/* Close button */
.lightbox__close {
  position: absolute;
  top: 14px;
  right: 14px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.12);
  border: none;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s ease;
  z-index: 10;
}
.lightbox__close:hover { background: rgba(255, 255, 255, 0.22); }
.lightbox__close svg   { width: 20px; height: 20px; }

/* Counter */
.lightbox__counter {
  position: absolute;
  top: 18px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.65);
  font-weight: 500;
  letter-spacing: 0.06em;
  pointer-events: none;
  white-space: nowrap;
  z-index: 10;
}

/* Side zones */
.lightbox__side {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 80px;
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.lightbox__side--prev { left: 0; }
.lightbox__side--next { right: 0; }

/* Nav buttons inside side zones */
.lightbox__nav {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s ease;
  pointer-events: none;
}
.lightbox__side:hover .lightbox__nav {
  background: rgba(255, 255, 255, 0.22);
}
.lightbox__nav svg { width: 22px; height: 22px; }

/* Content */
.lightbox__content {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 100%;
  max-height: 100%;
}

/* Image */
.lightbox__img {
  max-width: 100%;
  max-height: calc(100vh - 120px);
  object-fit: contain;
  border-radius: 8px;
  display: block;
  user-select: none;
  transition: transform 0.2s ease;
  will-change: transform;
  touch-action: none;
}
.lightbox__img--pinching {
  transition: none;
}
.lightbox__img--zoomed {
  cursor: grab;
  border-radius: 4px;
}
.lightbox__img--dragging {
  cursor: grabbing;
  transition: none;
}

/* Caption */
.lightbox__caption {
  margin-top: 12px;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.6);
  text-align: center;
  font-style: italic;
  max-width: 600px;
  pointer-events: none;
}

@media (max-width: 600px) {
  .lightbox {
    padding: 52px 0 16px;
  }
  .lightbox__side {
    width: 52px;
  }
  .lightbox__nav {
    width: 36px;
    height: 36px;
  }
}
</style>
