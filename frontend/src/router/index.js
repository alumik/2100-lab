import Vue from 'vue'
import Router from 'vue-router'
import Homepage from '@/userviews/homepage/index'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/personal',
      name: 'PersonalCenter',
      component: () => import('@/userviews/personal/personalCenter')
    },
    {
      path: '/studypage',
      name: 'Studypage',
      component: () => import('@/userviews/studypage/index')
    },
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
      path: '/studylog',
      name: 'StudyLog',
      component: () => import('@/userviews/personal/log/studyLog')
    },
    {
      path: '/coursedetail',
      name: 'CourseDetail',
      component: () => import('@/userviews/coursedetail/index')
    },
    {
      path: '/admin',
      name: 'Main',
      component: () => import('@/adminviews/main')
    },
    {
      path: '/admin/course',
      name: 'CourseManagement',
      component: () => import('@/adminviews/course/management')
    },
    {
      path: '/admin/course/detail',
      name: 'BackendCourseDetail',
      component: () => import('@/adminviews/course/detail')
    },
    {
      path: '/admin/course/creation',
      name: 'AddCourse',
      component: () => import('@/adminviews/course/add_course')
    },
    {
      path: '/admin/course/edit',
      name: 'EditCourse',
      component: () => import('@/adminviews/course/edit_course')
    },
    {
      path: '/admin/message',
      name: 'MessageManagement',
      component: () => import('@/adminviews/message/management')
    },
    {
      path: '/admin/message/detail',
      name: 'MessageDetail',
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
    },
    {
      path: '/admin/user',
      name: 'UserManagement',
      component: () => import('@/adminviews/user/management')
    },
    {
      path: '/admin/user/detail',
      name: 'UserDetail',
      component: () => import('@/adminviews/user/detail')
    },
    {
      path: '/admin/user/detail/course',
      name: 'Course',
      component: () => import('@/adminviews/user/course')
    },
    {
      path: '/admin/user/detail/order',
      name: 'Order',
      component: () => import('@/adminviews/user/order')
    }
  ]
})
