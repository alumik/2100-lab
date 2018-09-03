import Vue from 'vue'
import Router from 'vue-router'
import Homepage from '@/userviews/homepage/index'

Vue.use(Router)

let backstage_suffix = ' - 2100实验室后台管理'
let forestage_suffix = ' - 2100实验室'

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/burnedcourse',
      name: 'BurnedCourse',
      meta: {
        title: '课程已焚毁' + forestage_suffix,
        requireAuth: false
      },
      component: () => import('@/userviews/burnedcoursepage/index')
    },
    {
      path: '/404',
      name: 'PageNotFound',
      meta: {
        title: '未找到页面' + forestage_suffix,
        requireAuth: false
      },
      component: () => import('@/userviews/pagenotfound/index')
    },
    {
      path: '/allfreecourse',
      name: 'AllFreeCourse',
      meta: {
        title: '免费课程' + forestage_suffix,
        requireAuth: false
      },
      component: () => import('@/userviews/allcourselistpage/allFreeCoursePage')
    },
    {
      path: '/allpaidcourse',
      name: 'AllPaidCourse',
      meta: {
        title: '付费课程' + forestage_suffix,
        requireAuth: false
      },
      component: () => import('@/userviews/allcourselistpage/allPaidCoursePage')
    },
    {
      path: '/personal',
      name: 'PersonalCenter',
      component: () => import('@/userviews/personal/personal_center'),
      meta: {title: '个人中心' + forestage_suffix}
    },
    {
      path: '/studypage',
      name: 'StudyPage',
      component: () => import('@/userviews/studypage/index'),
      meta: {title: '学习' + forestage_suffix}
    },
    {
      path: '/',
      name: 'Homepage',
      meta: {
        requireAuth: false,
        title: '2100实验室'
      },
      component: Homepage
    },
    {
      path: '/login',
      name: 'Login',
      meta: {
        requireAuth: false,
        title: '登录' + forestage_suffix
      },
      component: () => import('@/userviews/personal/login')
    },
    {
      path: '/personal/studylog',
      name: 'StudyLog',
      component: () => import('@/userviews/personal/log/study_log'),
      meta: {title: '学习记录' + forestage_suffix}
    },
    {
      path: '/personal/orderlog',
      name: 'OrderLog',
      component: () => import('@/userviews/personal/log/order_log'),
      meta: {title: '订单记录' + forestage_suffix}
    },
    {
      path: '/coursedetail',
      name: 'CourseDetail',
      meta: {
        title: '课程详情' + forestage_suffix,
        requireAuth: false
      },
      component: () => import('@/userviews/coursedetail/index')
    },
    {
      path: '/admin',
      name: 'AdminLogin',
      meta: {
        requireAuth: false,
        title: '登录' + backstage_suffix
      },
      component: () => import('@/adminviews/login')
    },
    {
      path: '/admin/main',
      name: 'Main',
      component: () => import('@/adminviews/main'),
      meta: {title: '主页' + backstage_suffix}
    },
    {
      path: '/admin/course',
      name: 'CourseManagement',
      component: () => import('@/adminviews/course/management'),
      meta: {title: '课程列表' + backstage_suffix}
    },
    {
      path: '/admin/course/detail',
      name: 'BackendCourseDetail',
      component: () => import('@/adminviews/course/detail'),
      meta: {title: '课程详情' + backstage_suffix}
    },
    {
      path: '/admin/course/creation',
      name: 'AddCourse',
      component: () => import('@/adminviews/course/add_course'),
      meta: {title: '新增课程' + backstage_suffix}
    },
    {
      path: '/admin/course/edit',
      name: 'EditCourse',
      component: () => import('@/adminviews/course/edit_course'),
      meta: {title: '修改课程' + backstage_suffix}
    },
    {
      path: '/admin/message',
      name: 'MessageManagement',
      component: () => import('@/adminviews/message/management'),
      meta: {title: '留言列表' + backstage_suffix}
    },
    {
      path: '/admin/message/detail',
      name: 'MessageDetail',
      component: () => import('@/adminviews/message/detail'),
      meta: {title: '留言详情' + backstage_suffix}
    },
    {
      path: '/admin/adminmanagement',
      name: 'AdminManagement',
      component: () => import('@/adminviews/admin/management'),
      meta: {title: '管理员管理' + backstage_suffix}
    },
    {
      path: '/admin/adminmanagement/changecode',
      name: 'ChangeCode',
      component: () => import('@/adminviews/admin/change_code'),
      meta: {title: '修改管理员密码' + backstage_suffix}
    },
    {
      path: '/admin/adminmanagement/changename',
      name: 'ChangeName',
      component: () => import('@/adminviews/admin/change_name'),
      meta: {title: '修改管理员名称' + backstage_suffix}
    },
    {
      path: '/admin/adminmanagement/distribution',
      name: 'DistributeAuthority',
      component: () => import('@/adminviews/admin/distribute_authority'),
      meta: {title: '分配管理员权限' + backstage_suffix}
    },
    {
      path: '/admin/adminmanagement/detail',
      name: 'AdminDetail',
      component: () => import('@/adminviews/admin/detail'),
      meta: {title: '管理员详情' + backstage_suffix}
    },
    {
      path: '/admin/adminmanagement/creation',
      name: 'AddAdmin',
      component: () => import('@/adminviews/admin/add_admin'),
      meta: {title: '新增管理员' + backstage_suffix}
    },
    {
      path: '/admin/order',
      name: 'OrderManagement',
      component: () => import('@/adminviews/order/management'),
      meta: {title: '订单列表' + backstage_suffix}
    },
    {
      path: '/admin/order/detail',
      name: 'OrderDetail',
      component: () => import('@/adminviews/order/detail'),
      meta: {title: '订单详情' + backstage_suffix}
    },
    {
      path: '/admin/user',
      name: 'UserManagement',
      component: () => import('@/adminviews/user/management'),
      meta: {title: '用户列表' + backstage_suffix}
    },
    {
      path: '/admin/user/detail',
      name: 'UserDetail',
      component: () => import('@/adminviews/user/detail'),
      meta: {title: '用户详情' + backstage_suffix}
    },
    {
      path: '/admin/user/detail/course',
      name: 'Course',
      component: () => import('@/adminviews/user/course'),
      meta: {title: '全部相关课程' + backstage_suffix}
    },
    {
      path: '/admin/user/detail/order',
      name: 'Order',
      component: () => import('@/adminviews/user/order'),
      meta: {title: '全部相关订单' + backstage_suffix}
    },
    {
      path: '/admin/log',
      name: 'LogManagement',
      component: () => import('@/adminviews/log/management'),
      meta: {title: '日志查询' + backstage_suffix}
    },
    {
      path: '/admin/log/detail',
      name: 'LogDetail',
      component: () => import('@/adminviews/log/detail'),
      meta: {title: '日志列表' + backstage_suffix}
    },
    {
      path: '/admin/data/total',
      name: 'TotalData',
      component: () => import('@/adminviews/data/total_data'),
      meta: {title: '数据分析' + backstage_suffix}
    },
    {
      path: '/admin/data/time',
      name: 'TimeData',
      component: () => import('@/adminviews/data/time_data'),
      meta: {title: '数据分析' + backstage_suffix}
    },
    {
      path: '*',
      redirect: '/404'
    }
  ]
})
