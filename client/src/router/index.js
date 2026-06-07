import { createRouter, createWebHistory } from 'vue-router'
import Todos from '../components/Todos.vue'
import Auth from '../components/Auth.vue'
import Schedule from '../components/Schedule.vue'
import MainLayout from '@/components/MainLayout.vue'
import Analytics from '@/components/Analytics.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: MainLayout,
      children: [
        {
          path: '',
          name: 'Todos',
          component: Todos,
          meta: { requiresAuth: true }
        },
        {
          path: 'schedule',
          name: 'Schedule',
          component: Schedule,
          meta: { requiresAuth: true }
        },
        {
          path: 'analytics',
          name: 'Analytics',
          component: Analytics,
          meta: { requiresAuth: true }
        }
      ]
    },
    {
      path: '/auth', // ИСПРАВЛЕНО: строго /auth вместо /register
      name: 'Auth',
      component: Auth,
      meta: { requiresGuest: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = sessionStorage.getItem('isLoggedIn') === 'true'

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/auth') // ИСПРАВЛЕНО: перенаправление на существующий путь /auth
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
