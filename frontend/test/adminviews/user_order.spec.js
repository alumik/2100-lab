/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import Order from '@/adminviews/user/order'
import Basic from '@/adminviews/basic/basic'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

const $route = {
  path: '/admin/user/detail/order',
  query: {'user_id': 1001}
}

describe('相关订单页面单元测试', () => {
  const wrapper = shallowMount(Order, {
    mocks: {
      $route
    }
  })

  it('相关订单组件存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })
})
