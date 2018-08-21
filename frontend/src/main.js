// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
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
    user: {
      is_new_customer: null,
      customer_id: '',
      username: '',
      avatar: null
    }
  },
  mutations: {
    status (state) {
      state.status = true
      sessionStorage.setItem('status', 'true')
    },
    user (state, data) {
      state.user = data
      sessionStorage.setItem('user', JSON.stringify(data))
    },
    new_customer (state, status) {
      state.user.is_new_customer = status
    },
    logout (state) {
      state.status = false
      sessionStorage.setItem('status', 'false')
    }
  }
})

const i18n = new VueI18n({
  locale: 'zh',
  messages: {
    'zh': require('./lang/zh/zh'),
    'en': require('./lang/en/en')
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  axios,
  store,
  i18n,
  components: { App },
  template: '<App/>'
}).$mount('#app')
