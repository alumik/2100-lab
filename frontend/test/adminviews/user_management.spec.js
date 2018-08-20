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

  it('包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('测试是否包含分页导航', () => {
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
    expect(wrapper.vm.state).toBe('is_banned')
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

  it('测试是否能够正确进行页面跳转', () => {
    expect(wrapper.vm.page_jump).toBe(false)
    wrapper.find('button').trigger('click')
    expect(wrapper.vm.page_jump).toBe(true)
  })
})
