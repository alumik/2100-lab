// /* eslint-disable no-undef */
//
// import Vue from 'vue'
// import BootstrapVue from 'bootstrap-vue'
// import Vuex from 'vuex'
//
// import { shallowMount } from '@vue/test-utils'
// import login from '@/userviews/personal/login.vue'
//
// Vue.use(Vuex)
// Vue.use(BootstrapVue)
//
// const $router = {
//   path: '/coursedetail',
//   query: { course_id: 1 },
//   params: {}
// }
//
// const $store = new Vuex.Store({
//   state: {
//     status: true,
//     user: {
//       is_new_customer: null,
//       customer_id: '',
//       username: '',
//       avatar: null
//     },
//     phone: '',
//     money: '',
//     time: ''
//   }
// })
//
// describe('登录页面单元测试', () => {
//   const wrapper = shallowMount(login, {
//     mocks: {
//       $router,
//       $store
//     }
//   })
//   wrapper.find('#send')
//   // const phoneInput = wrapper.find('[v-mo
//   // const send = wrapper.find('#send')
//   // const phoneInput = wrapper.find('[v-model="phone"]')
//   it('鼠标点击手机号输入框', () => {
//     // expect(phoneInput.exists()).toBe(true)
//     // button.trigger('click')
//     // expect(wrapper.vm.code_disabled).toBe(false)
//   })
// })
