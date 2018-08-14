import Vue from 'vue'
import Router from 'vue-router'
import Homepage from '@/userviews/homepage/index'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/admin',
      name: 'AdminNavBar',
      component: () => import('@/adminviews/components/navbar')
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/userviews/components/login')
    },
    {
      path: '/',
      name: 'Homepage',
      component: Homepage
    },
    {
      path: '/personal',
      name: 'PersonalCenter',
      component: () => import('@/userviews/personal/personalCenter')
    },
    {
      path: '/admin/message',
      name: 'MessageManagement',
      component: () => import('@/adminviews/message/management')
    },
    {
      path: '/admin/admin/changecode',
      name: 'ChangeCode',
      component: () => import('@/adminviews/admin/changecode')
    }
  ]
})
