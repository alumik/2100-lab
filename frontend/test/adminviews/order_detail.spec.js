/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import OrderDetail from '@/adminviews/order/detail'
import Basic from '@/adminviews/basic/basic'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

const $route = {
  path: '/admin/message/detail',
  query: {'order_id': 1001}
}

describe('订单详情页面单元测试', () => {
  const wrapper = shallowMount(OrderDetail, {
    mocks: {
      $route
    }
  })

  it('订单详情组件存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('测试按钮渲染数量', () => {
    expect(wrapper.findAll('button').length).toEqual(1)
  })
})
