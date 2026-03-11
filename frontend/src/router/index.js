import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/HomePage.vue'),
    meta: { title: 'i37 — Islombek Ravshanov' }
  },
  {
    path: '/blog',
    name: 'Blog',
    component: () => import('@/pages/BlogPage.vue'),
    meta: { title: 'Blog — i37' }
  },
  {
    path: '/blog/:id',
    name: 'BlogDetail',
    component: () => import('@/pages/BlogDetailPage.vue'),
    meta: { title: 'Article — i37' }
  },
  {
    path: '/portfolio',
    name: 'Portfolio',
    component: () => import('@/pages/PortfolioPage.vue'),
    meta: { title: 'Portfolio — i37' }
  },
  {
    path: '/portfolio/:id',
    name: 'ProjectDetail',
    component: () => import('@/pages/ProjectDetailPage.vue'),
    meta: { title: 'Project — i37' }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0, behavior: 'smooth' }
  }
})

router.afterEach((to) => {
  if (to.meta?.title) {
    document.title = to.meta.title
  }
})

export default router
