import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  }
})

// ── Main Info ────────────────────────────────────────────────
export function getMainInfo() {
  return api.get('main-info/')
}

// ── Career ───────────────────────────────────────────────────
export function getCareer() {
  return api.get('career/')
}

// ── Social Links ─────────────────────────────────────────────
export function getSocialLinks() {
  return api.get('social-links/')
}

// ── Blog Types ───────────────────────────────────────────────
export function getBlogTypes() {
  return api.get('blog-types/')
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
