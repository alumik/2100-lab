/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AddAdmin from '@/adminviews/admin/add_admin.vue'

describe('新增管理员模块单元测验', () => {
  const wrapper = shallowMount(AddAdmin)

  it('标题是"新增管理员"', () => {
    expect(wrapper.find('h1').text()).toEqual('新增管理员')
  })

  it('未输入手机号', () => {
    expect(wrapper.vm.error_message).toEqual('')
    wrapper.vm.check_format()
    expect(wrapper.vm.error_message).toEqual('请输入手机号')
  })

  it('输入一个错误格式的手机号', () => {
    wrapper.vm.error_message = ''
    wrapper.vm.admin.phone_number = '0000000000000'
    expect(wrapper.vm.error_message).toEqual('')
    wrapper.vm.check_format()
    expect(wrapper.vm.error_message).toEqual('请输入一个正确的手机号')
  })

  it('未输入密码', () => {
    wrapper.vm.error_message = ''
    wrapper.vm.admin.phone_number = '15222583257'
    expect(wrapper.vm.error_message).toEqual('')
    wrapper.vm.check_format()
    expect(wrapper.vm.error_message).toEqual('请输入密码')
  })
})
