import Vue from 'vue'
import Router from 'vue-router'
import Homepage from '@/userviews/homepage/index'

Vue.use(Router)

export default new Router({
  mode: 'history',
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
      path: '/coursedetail',
      name: 'CourseDetail',
      component: () => import('@/userviews/coursedetail/index')
    },
    {
      path: '/admin',
      name: 'AdminManagement',
      component: () => import('@/adminviews/admin/management')
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
      path: '/admin/adminmanagement',
      name: 'AdminManagement',
      component: () => import('@/adminviews/admin/management')
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
    },
    {
      path: '/admin/adminmanagement/detail',
      name: 'AdminDetail',
      component: () => import('@/adminviews/admin/detail')
    },
    {
      path: '/admin/adminmanagement/creation',
      name: 'AddAdmin',
      component: () => import('@/adminviews/admin/addadmin')
    },
    {
      path: '/admin/order',
      name: 'OrderManagement',
      component: () => import('@/adminviews/order/management')
    },
    {
      path: '/admin/order/detail',
      name: 'OrderDetail',
      component: () => import('@/adminviews/order/detail')
    }
  ]
})
