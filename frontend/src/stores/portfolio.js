import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getProjects, getProject } from '@/api/index.js'

export const usePortfolioStore = defineStore('portfolio', () => {
  const projects = ref([])
  const currentProject = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    count: 0,
    next: null,
    previous: null,
    currentPage: 1,
    pageSize: 9
  })

  async function fetchProjects({ page = 1, search = '', tech = null } = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await getProjects({ page, search, tech })
      const data = response.data
      if (data && typeof data === 'object' && 'results' in data) {
        projects.value = data.results
        pagination.value = {
          count: data.count,
          next: data.next,
          previous: data.previous,
          currentPage: page,
          pageSize: pagination.value.pageSize
        }
      } else {
        projects.value = Array.isArray(data) ? data : []
        pagination.value.count = projects.value.length
        pagination.value.currentPage = 1
      }
    } catch (err) {
      error.value = err?.response?.data?.detail || err.message || 'Failed to load projects'
      projects.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchProject(id) {
    loading.value = true
    error.value = null
    currentProject.value = null
    try {
      const response = await getProject(id)
      currentProject.value = response.data
    } catch (err) {
      error.value = err?.response?.data?.detail || err.message || 'Failed to load project'
    } finally {
      loading.value = false
    }
  }

  return {
    projects,
    currentProject,
    loading,
    error,
    pagination,
    fetchProjects,
    fetchProject
  }
})
