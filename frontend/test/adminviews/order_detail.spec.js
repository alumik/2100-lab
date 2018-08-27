/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import OrderDetail from '@/adminviews/order/detail'
import Basic from '@/adminviews/basic/basic'
import DetailTable from '@/adminviews/components/detail_table'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

const $route = {
  path: '/admin/message/detail',
  query: { order_id: 1001 }
}

describe('订单详情页面单元测试', () => {
  const wrapper = shallowMount(OrderDetail, {
    mocks: {
      $route
    }
  })

  it('测试订单详情组件是否存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('测试是否包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('测试是否包含标题', () => {
    expect(wrapper.contains('.title')).toBe(true)
  })

  it('测试按钮渲染数量', () => {
    expect(wrapper.findAll('a').length).toEqual(1)
  })

  it('测试是否包含DetailTable组件', () => {
    expect(wrapper.contains(DetailTable)).toBe(true)
  })

  it('测试compute_order函数', () => {
    const order1 = {
      order_no: '1',
      course_codename: 'SOFT',
      course_title: '1',
      customer_username: 'liu',
      created_at: '123456789012',
      refunded_at: null,
      money: 10.0,
      is_refunded: true
    }
    const result1 = ['1', 'SOFT', '1', 'liu', '1234567890', '-', 10.0, '已退款']
    expect(wrapper.vm.compute_order(order1)).toEqual(result1)
    const order2 = {
      order_no: '1',
      course_codename: 'SOFT',
      course_title: '1',
      customer_username: 'liu',
      created_at: '123456789012',
      refunded_at: '2018-08-05Z8:12',
      money: 10.0,
      is_refunded: false
    }
    const result2 = ['1', 'SOFT', '1', 'liu', '1234567890', '2018-08-05', 10.0, '已完成']
    expect(wrapper.vm.compute_order(order2)).toEqual(result2)
  })

  it('测试refund函数', () => {
    expect(wrapper.vm.wrong_count_down).toBe(wrapper.vm.dismiss_second)
    expect(wrapper.vm.is_refunded).toBe(false)
    wrapper.find('#refund-button').trigger('click')
    expect(wrapper.vm.wrong_count_down).toBe(wrapper.vm.dismiss_second)
    expect(wrapper.vm.is_refunded).toBe(false)
    expect(wrapper.vm.wrong.substr(0, 4)).toEqual('获取订单')
  })
})
