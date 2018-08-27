/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import Course from '@/adminviews/user/course'
import Basic from '@/adminviews/basic/basic'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

const $route = {
  path: '/admin/user/detail/course',
  query: { user_id: 1001 }
}

describe('相关课程页面单元测试', () => {
  const wrapper = shallowMount(Course, {
    mocks: {
      $route
    }
  })

  it('测试相关课程组件是否存在', () => {
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

  it('测试compute_date函数', () => {
    expect(wrapper.vm.compute_date('2018-08-15Z08:15')).toEqual('2018-08-15')
  })

  it('测试compute_burnt函数', () => {
    expect(wrapper.vm.compute_burnt(true)).toEqual('已焚毁')
    expect(wrapper.vm.compute_burnt(false)).toEqual('未焚毁')
  })
})
