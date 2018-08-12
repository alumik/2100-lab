import Vue from 'vue'
import Router from 'vue-router'
import AdminNavBar from '@/adminviews/components/navbar'
import UserNavBar from '@/userviews/components/navbar'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'AdminNavBar',
      component: AdminNavBar
    },
    {
      path: '/user',
      name: 'UserNavBar',
      component: UserNavBar
    }
  ]
})
