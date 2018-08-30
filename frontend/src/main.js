import Vue from 'vue'
import App from './App'
import router from './router'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueQrcode from '@xkeshi/vue-qrcode'
import datePicker from 'vue-bootstrap-datetimepicker'
import 'pc-bootstrap4-datetimepicker/build/css/bootstrap-datetimepicker.css'
import VCharts from 'v-charts'
import axios from 'axios'
import Vuex from 'vuex'
import VueI18n from 'vue-i18n'
import SimpleLineIcons from 'vue-simple-line'

Vue.component(VueQrcode.name, VueQrcode)
Vue.use(BootstrapVue)
Vue.use(datePicker)
Vue.use(VCharts)
Vue.use(Vuex)
Vue.use(VueI18n)
Vue.config.productionTip = false
Vue.prototype.$http = axios
axios.defaults.withCredentials = true
const store = new Vuex.Store({
  state: {
    status: false,
    admin_id: '',
    user: {
      user_id: '',
      username: '',
      phone_number: '',
      avatar: 'default/customers/avatars/2100_lab.jpg',
      reward_coin: '0.00',
      is_vip: '',
      is_banned: '',
      date_joined: '',
      updated_at: '',
      groups: [],
      is_staff: false
    },
    groups: [],
    address: 'http://localhost/media/',
    menu: 0,
    colors: [
      '#204269',
      '#204269',
      '#204269',
      '#204269',
      '#204269',
      '#204269',
      '#204269'
    ],
    lists: [
      {
        id: 1,
        isActive: false,
        path: '/admin/course',
        permit: 'course_admin'
      },
      {
        id: 2,
        isActive: false,
        path: '/admin/message',
        permit: 'comment_admin'
      },
      {
        id: 3,
        isActive: false,
        path: '/admin/user',
        permit: 'customer_admin'
      },
      {
        id: 4,
        isActive: false,
        path: '/admin/order',
        permit: 'order_admin'
      },
      {
        id: 5,
        isActive: false,
        path: '/admin/log',
        permit: 'log_admin'
      },
      {
        id: 6,
        isActive: false,
        path: '/admin/data/total'
      },
      {
        id: 7,
        isActive: false,
        path: '/admin/adminmanagement'
      }
    ],
    permissions: [
      'course_admin',
      'comment_admin',
      'customer_admin',
      'order_admin',
      'log_admin'
    ]
  },
  mutations: {
    status (state, status = true) {
      state.status = status
      sessionStorage.setItem('status', status ? 'true' : 'false')
    },
    user (state, user) {
      state.user = user
    },
    username (state, username) {
      state.user.username = username
    },
    phone (state, number) {
      state.user.phone = number
      sessionStorage.setItem('phone', number)
    },
    money (state, money) {
      state.money = money
    },
    date_joined (state, time) {
      state.user.date_joined = time
    },
    avatar (state, avatar) {
      state.user.avatar = avatar
    },
    logout (state) {
      state.status = false
      sessionStorage.setItem('status', 'false')
    },
    menu (state, menu) {
      state.menu = menu
      sessionStorage.setItem('menu', menu)
    },
    colors (state, id) {
      for (let i = 0; i < 7; i++) {
        state.colors[i] = '#204269'
      }
      state.colors[id] = '#5b9bd1'
      sessionStorage.setItem('colors', id)
    },
    groups (state, groups) {
      if (groups.includes('super_admin')) {
        state.groups.push(1, 2, 3, 4, 5, 6, 7)
      } else {
        state.groups = []
        let i = 1
        for (let group of state.permissions) {
          if (groups.includes(group)) {
            state.groups.push(i)
          }
          i++
        }
      }
    },
    staff (state, is_staff = true) {
      state.user.is_staff = is_staff
    }
  }
})

const i18n = new VueI18n({
  locale: 'zh',
  messages: {
    zh: require('./lang/zh/zh'),
    en: require('./lang/en/en')
  }
})

Vue.component('simple-line-icons', SimpleLineIcons)
router.beforeEach(async (to, from, next) => {
  document.title = to.meta.title
  let response = await axios.post(
    'http://localhost/api/v1/core/auth/is-authenticated/',
    {
      withCredentials: true
    }
  )
  if (!response.data.is_authenticated && to.meta.requireAuth !== false) {
    next('/')
  } else if (response.data.is_authenticated && response.data.is_staff) {
    for (let list of store.state.lists) {
      if (to.path.toString().includes(list.path)) {
        if (response.data.admin_groups.includes('super_admin')) {
          sessionStorage.setItem('menu', list.id)
          sessionStorage.setItem('colors', parseInt(list.id) - 1)
          next()
        } else if (!response.data.admin_groups.includes(list.permit)) {
          next('/admin/main')
        }
        sessionStorage.setItem('menu', list.id)
        sessionStorage.setItem('colors', parseInt(list.id) - 1)
      }
    }
    next()
  } else if (
    response.data.is_authenticated &&
    !response.data.is_staff &&
    to.path.includes('admin/')
  ) {
    next('/404')
  } else {
    next()
  }
})
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  axios,
  store,
  i18n,
  components: { App, SimpleLineIcons },
  template: '<App/>'
}).$mount('#app')
