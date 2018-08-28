/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import LogDetail from '@/adminviews/log/detail'
import Basic from '@/adminviews/basic/basic'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

const $route = {
  path: '/admin/log/detail',
  query: {'admin_id': 1001,
  begin_date: 1534702219,
  end_date: 1534702319,
  select: 'a'}
}

describe('日志详情页面单元测试', () => {
  const wrapper = shallowMount(LogDetail, {
    mocks: {
      $route
    }
  })

  it('测试日志详情组件是否存在', () => {
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
    expect(wrapper.vm.compute_date('2018-08-27T17:57:31.385Z')).toEqual('8/28/2018, 1:57:31 AM')
  })

  it('测试compute_admin_name函数', () => {
    expect(wrapper.vm.compute_admin_name('1_deleted_2')).toEqual('1（已删除）')
    expect(wrapper.vm.compute_admin_name('1523')).toEqual('1523')
  })
})
