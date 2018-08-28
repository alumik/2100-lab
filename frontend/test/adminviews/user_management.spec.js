/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import UserManagement from '@/adminviews/user/management'
import Basic from '@/adminviews/basic/basic'
import Pagination from '@/components/pagination'

describe('用户管理页面单元测试', () => {
  const wrapper = shallowMount(UserManagement)

  it('用户管理组件存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('测试是否包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('测试是否包含翻页导航', () => {
    expect(wrapper.contains(Pagination)).toBe(true)
  })

  it('测试输入框渲染数量', () => {
    expect(wrapper.findAll("[type = 'text']").length).toEqual(3)
  })

  it('测试下拉菜单输入框数量', () => {
    expect(wrapper.findAll('select').length).toEqual(2)
  })

  it('测试按钮渲染数量', () => {
    const length = wrapper.findAll('tr').length
    expect(wrapper.findAll('button').length).toEqual(length - 2)
  })

  it('测试改变用户类型菜单选项绑定数据是否改变', () => {
    wrapper.findAll('option').at(0).setSelected()
    expect(wrapper.vm.type).toBe('whole')
  })

  it('测试改变状态菜单选项绑定数据是否改变', () => {
    wrapper.findAll('option').at(4).setSelected()
    expect(wrapper.vm.state).toBe('not_banned')
  })

  it('测试文本框输入是否正确', () => {
    const inputs = wrapper.findAll("[type='text']")
    const input0 = inputs.at(0)
    input0.setValue('001')
    expect(wrapper.vm.user_id).toBe('001')
    const input1 = inputs.at(1)
    input1.setValue('小红')
    expect(wrapper.vm.user_name).toBe('小红')
    const input2 = inputs.at(2)
    input2.setValue('13102250001')
    expect(wrapper.vm.phone).toBe('13102250001')
  })

  it('测试get_type函数', () => {
    expect(wrapper.vm.get_type(true)).toBe('认证用户')
    expect(wrapper.vm.get_type(false)).toBe('普通用户')
  })

  it('测试get_state函数', () => {
    expect(wrapper.vm.get_state(true)).toBe('已禁言')
    expect(wrapper.vm.get_state(false)).toBe('未禁言')
  })

  it('测试get_type_data函数', () => {
    wrapper.vm.type = 'whole'
    expect(wrapper.vm.get_type_data()).toEqual('0')
    wrapper.vm.type = 'normal'
    expect(wrapper.vm.get_type_data()).toEqual('1')
    wrapper.vm.type = 'authenticated'
    expect(wrapper.vm.get_type_data()).toEqual('2')
  })

  it('测试get_state_data函数', () => {
    wrapper.vm.state = 'whole'
    expect(wrapper.vm.get_state_data()).toEqual('0')
    wrapper.vm.state = 'not_banned'
    expect(wrapper.vm.get_state_data()).toEqual('1')
    wrapper.vm.state = 'is_banned'
    expect(wrapper.vm.get_state_data()).toEqual('2')
  })

  it('测试change_page函数', () => {
    expect(wrapper.vm.page).toBe(1)
    wrapper.vm.change_page(2)
    expect(wrapper.vm.page).toBe(2)
  })
})
