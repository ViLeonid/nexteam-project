import { createRouter, createWebHistory } from 'vue-router'
import Todos from '../components/Todos.vue'
import Auth from '../components/Auth.vue'
import Landing from '@/components/Landing.vue'
import Schedule from '../components/Schedule.vue'
import MainLayout from '@/components/MainLayout.vue'
import Analytics from '@/components/Analytics.vue'
import Olympiads from '@/components/Olympiads.vue'
import MainPage from '@/components/MainPage.vue'
import Focus from '@/components/Focus.vue'
import Graph from '@/components/Graph.vue'
import Profile from '@/components/Profile.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: MainLayout,
      children: [
        {
          path: '',
          name: 'MainPage',
          component: MainPage,
          meta: { requiresAuth: true }
        },
        {
          path: 'todos',
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
          path: 'olympiads',
          name: 'Olympiads',
          component: Olympiads,
          meta: { requiresAuth: true }
        },
        {
          path: 'analytics',
          name: 'Analytics',
          component: Analytics,
          meta: { requiresAuth: true }
        }
        ,
        {
          path: 'focus',
          name: 'Focus',
          component: Focus,
          meta: { requiresAuth: true }
        },
        {
          path: 'graph',
          name: 'graph',
          component: Graph,
          meta: { requiresAuth: true }
        },
        {
          path: 'profile',
          name: 'profile',
          component: Profile,
          meta: { requiresAuth: true }
        }
      ]
    },
    {
      path: '/auth',
      name: 'Auth',
      component: Auth,
      meta: { requiresGuest: true }
    },
    {
      path: '/landing',
      name: 'Landing',
      component: Landing,
      meta: { requiresGuest: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = sessionStorage.getItem('isLoggedIn') === 'true'

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/landing')
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
