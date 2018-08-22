/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AdminManagement from '@/adminviews/admin/management.vue'

describe('管理员管理模块单元测验', () => {
  const wrapper = shallowMount(AdminManagement)

  it('标题是"管理员列表"', () => {
    expect(wrapper.find('h2').text()).toEqual('管理员列表')
  })

  it('渲染查询输入框', () => {
    expect(wrapper.findAll('[type=text]').length).toEqual(2)
  })

  it('输入查询手机号内容正确显示', () => {
    wrapper.findAll('[type=text]').at(1).setValue('15222583257')
    expect(wrapper.vm.phone_number).toEqual('15222583257')
  })

  it('检测新增管理员按钮的正确跳转', () => {
    expect(wrapper.vm.test_add_admin).toBe(false)
    wrapper.findAll('button').at(0).trigger('click')
    expect(wrapper.vm.test_add_admin).toBe(true)
  })
})
