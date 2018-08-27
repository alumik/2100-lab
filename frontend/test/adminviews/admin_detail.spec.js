/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AdminDetail from '@/adminviews/admin/detail.vue'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

const $route = {
  path: '/admin/adminmanagement/detail',
  query: {'admin_id': 0}
}

describe('管理员详情模块单元测验', () => {
  const wrapper = shallowMount(AdminDetail, {
    mocks: {
      $route
    }
  })

  it('标题是"管理员详情"', () => {
    expect(wrapper.find('h1').text()).toEqual('管理员详情')
  })

  it('传递参数信息到页面中', () => {
    expect(wrapper.vm.admin_id).toEqual(0)
  })

  it('转换信息测试1_1', () => {
    let s = wrapper.vm.transfer_permission('comment_admin')
    expect(s).toEqual('留言管理权限')
  })

  it('转换信息测试1_2', () => {
    let s = wrapper.vm.transfer_permission('course_admin')
    expect(s).toEqual('课程管理权限')
  })

  it('转换信息测试1_3', () => {
    let s = wrapper.vm.transfer_permission('customer_admin')
    expect(s).toEqual('用户管理权限')
  })

  it('转换信息测试1_4', () => {
    let s = wrapper.vm.transfer_permission('log_admin')
    expect(s).toEqual('日志管理权限')
  })

  it('转换信息测试1_5', () => {
    let s = wrapper.vm.transfer_permission('order_admin')
    expect(s).toEqual('订单管理权限')
  })

  it('转换信息测试1_6', () => {
    let s = wrapper.vm.transfer_permission('super_admin')
    expect(s).toEqual('超级管理员权限')
  })
})
