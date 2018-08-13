import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/admin',
      name: 'AdminNavBar',
      component: () => import('@/adminviews/components/navbar')
    },
    {
      path: '/',
      name: 'UserNavBar',
      component: () => import('@/userviews/components/navbar')
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
    }
  ]
})
