/* eslint-disable no-undef */

import UserNavbar from '@/userviews/components/navbar'
import {shallowMount} from '@vue/test-utils'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'
import Vuex from "vuex";

Vue.use(BootstrapVue)

const $store = new Vuex.Store({
  state: {
    status: true,
    user: {
      is_new_customer: null,
      customer_id: '',
      username: '',
      avatar: null
    },
    phone: '',
    money: '',
    time: ''
  }
})

describe('用户端导航栏测试', () => {
  const wrapper = shallowMount(UserNavbar,  {
    mocks: {
      $store
    }
  })

  it('导航栏组件渲染', () => {
    expect(wrapper.contains('#user-navbar')).toBe(true)
  })

  it('汉堡包渲染', () => {
    expect(wrapper.contains('#hamburger')).toBe(true)
  })

  it('logo渲染', () => {
    expect(wrapper.contains('#logoimg')).toBe(true)
  })

  it('用户头像渲染', () => {
    expect(wrapper.contains('#userlogo')).toBe(true)
  })

  it('登录注销按钮渲染', () => {
    expect(wrapper.contains('#logout')).toBe(true)
  })
})
