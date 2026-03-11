import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getBlogs, getBlog, getBlogTypes } from '@/api/index.js'

export const useBlogStore = defineStore('blog', () => {
  const blogs = ref([])
  const blogTypes = ref([])
  const currentBlog = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    count: 0,
    next: null,
    previous: null,
    currentPage: 1,
    pageSize: 10
  })

  async function fetchBlogs({ page = 1, search = '', type = null } = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await getBlogs({ page, search, type })
      const data = response.data
      // Handle both paginated and plain list responses
      if (data && typeof data === 'object' && 'results' in data) {
        blogs.value = data.results
        pagination.value = {
          count: data.count,
          next: data.next,
          previous: data.previous,
          currentPage: page,
          pageSize: pagination.value.pageSize
        }
      } else {
        blogs.value = Array.isArray(data) ? data : []
        pagination.value.count = blogs.value.length
        pagination.value.currentPage = 1
      }
    } catch (err) {
      error.value = err?.response?.data?.detail || err.message || 'Failed to load articles'
      blogs.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchBlog(id) {
    loading.value = true
    error.value = null
    currentBlog.value = null
    try {
      const response = await getBlog(id)
      currentBlog.value = response.data
    } catch (err) {
      error.value = err?.response?.data?.detail || err.message || 'Failed to load article'
    } finally {
      loading.value = false
    }
  }

  async function fetchBlogTypes() {
    try {
      const response = await getBlogTypes()
      const data = response.data
      blogTypes.value = Array.isArray(data) ? data : (data?.results ?? [])
    } catch (err) {
      blogTypes.value = []
    }
  }

  return {
    blogs,
    blogTypes,
    currentBlog,
    loading,
    error,
    pagination,
    fetchBlogs,
    fetchBlog,
    fetchBlogTypes
  }
})
