import Vue from 'vue'
import Router from 'vue-router'
import Homepage from '@/userviews/homepage/index'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Homepage',
      component: Homepage
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/userviews/personal/login')
    },
    {
      path: '/personal',
      name: 'PersonalCenter',
      component: () => import('@/userviews/personal/personalCenter')
    },
    {
      path: '/admin',
      name: 'AdminNavBar',
      component: () => import('@/adminviews/components/navbar')
    },
    {
      path: '/admin/message',
      name: 'MessageManagement',
      component: () => import('@/adminviews/message/management')
    },
    {
      path: '/admin/message/detail',
      name: 'Message',
      component: () => import('@/adminviews/message/detail')
    },
    {
      path: '/admin/adminmanagement/changecode',
      name: 'ChangeCode',
      component: () => import('@/adminviews/admin/changecode')
    },
    {
      path: '/admin/adminmanagement/distribution',
      name: 'DistributeAuthority',
      component: () => import('@/adminviews/admin/distributeauthority')
    }
  ]
})
