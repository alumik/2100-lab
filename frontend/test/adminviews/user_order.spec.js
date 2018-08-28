/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import Order from '@/adminviews/user/order'
import Basic from '@/adminviews/basic/basic'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

const $route = {
  path: '/admin/user/detail/order',
  query: { user_id: 1001 }
}

describe('相关订单页面单元测试', () => {
  const wrapper = shallowMount(Order, {
    mocks: {
      $route
    }
  })

  it('测试相关订单组件是否存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('测试是否包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('测试是否包含标题', () => {
    expect(wrapper.contains('.head-title')).toBe(true)
  })

  it('测试change_page函数', () => {
    expect(wrapper.vm.page).toBe(1)
    wrapper.vm.change_page(2)
    expect(wrapper.vm.page).toBe(2)
  })

  it('测试compute_state函数', () => {
    expect(wrapper.vm.compute_state(true)).toEqual('已退款')
    expect(wrapper.vm.compute_state(false)).toEqual('未退款')
  })
})
