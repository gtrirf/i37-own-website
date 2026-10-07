import axios from 'axios'

const api = axios.create({
  baseURL: 'https://api.i37.uz/api/v1/',
  timeout: 10000,
  headers: {
    Accept: 'application/json'
  }
})

// ── Kam o'zgaradigan endpointlar uchun xotira keshi ──────────
// Bir vaqtda kelgan bir xil so'rovlar (masalan, Footer + HomePage) bitta so'rovga birlashadi,
// sahifalar orasida o'tganda esa qayta yuklanmaydi.
const CACHE_TTL = 5 * 60 * 1000
const cache = new Map()

function cachedGet(url) {
  const hit = cache.get(url)
  if (hit && Date.now() - hit.time < CACHE_TTL) return hit.promise
  const promise = api.get(url).catch((err) => {
    cache.delete(url)
    throw err
  })
  cache.set(url, { promise, time: Date.now() })
  return promise
}

// ── Main Info ────────────────────────────────────────────────
export function getMainInfo() {
  return cachedGet('main-info/')
}

// ── Career ───────────────────────────────────────────────────
export function getCareer() {
  return cachedGet('career/')
}

// ── Social Links ─────────────────────────────────────────────
export function getSocialLinks() {
  return cachedGet('social-links/')
}

// ── Blog Types ───────────────────────────────────────────────
export function getBlogTypes() {
  return cachedGet('blog-types/')
}

// ── Blog ─────────────────────────────────────────────────────
export function getBlogs({ page = 1, search = '', type = null } = {}) {
  const params = { page }
  if (search) params.search = search
  if (type) params.type = type
  return api.get('blog/', { params })
}

export function getBlog(id) {
  return api.get(`blog/${id}/`)
}

// ── Projects ─────────────────────────────────────────────────
export function getProjects({ page = 1, search = '', tech = null } = {}) {
  const params = { page, page_size: 9 }
  if (search) params.search = search
  if (tech) params.tech = tech
  return api.get('projects/', { params })
}

export function getProject(id) {
  return api.get(`projects/${id}/`)
}

export default api
