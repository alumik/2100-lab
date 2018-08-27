/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import UserDetail from '@/adminviews/user/detail'
import Basic from '@/adminviews/basic/basic'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

const $route = {
  path: '/admin/user/detail',
  query: { user_id: '001' }
}

describe('用户详情页面单元测试', () => {
  const wrapper = shallowMount(UserDetail, {
    mocks: {
      $route
    }
  })

  it('测试用户详情组件是否存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('测试是否包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('测试按钮渲染数量', () => {
    expect(wrapper.findAll('a').length).toEqual(5)
  })

  it('测试是否能够正确跳转到相关页面', () => {
    expect(wrapper.vm.page_jump_course).toBe(false)
    wrapper.find('#course').trigger('click')
    expect(wrapper.vm.page_jump_course).toBe(true)
    expect(wrapper.vm.page_jump_order).toBe(false)
    wrapper.findAll('#order').trigger('click')
    expect(wrapper.vm.page_jump_order).toBe(true)
  })

  it('测试compute_user函数', () => {
    const user = {
      username: 'liu',
      phone_number: '123',
      reward_coin: 10.0,
      date_joined: '2018-08-15Z08:15',
      updated_at: '2018-08-17Z08:15'
    }
    const result = ['liu', '123', 10.0, '2018-08-15', '2018-08-17']
    expect(wrapper.vm.compute_user(user)).toEqual(result)
  })

  it('测试compute_state函数', () => {
    expect(wrapper.vm.compute_state(true)).toEqual('已退款')
    expect(wrapper.vm.compute_state(false)).toEqual('未退款')
  })

  it('测试compute_date函数', () => {
    expect(wrapper.vm.compute_date('2018-08-15Z08:15')).toEqual('2018-08-15')
  })

  it('测试compute_burnt函数', () => {
    expect(wrapper.vm.compute_burnt(true)).toEqual('已焚毁')
    expect(wrapper.vm.compute_burnt(false)).toEqual('未焚毁')
  })
})
