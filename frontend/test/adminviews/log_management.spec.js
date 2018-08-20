/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import LogManagement from '@/adminviews/log/management'
import Basic from '@/adminviews/basic/basic'

describe('日志查询页面单元测试', () => {
  const wrapper = shallowMount(LogManagement)

  it('日志查询组件存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('测试输入框渲染数量', () => {
    expect(wrapper.findAll("[type = 'text']").length).toEqual(1)
  })

  it('测试按钮渲染数量', () => {
    expect(wrapper.findAll('button').length).toEqual(1)
  })

  it('测试文本框输入是否正确', () => {
    const input = wrapper.find("[type='text']")
    input.setValue('100001')
    expect(wrapper.vm.admin_id).toBe('100001')
  })

  it('测试页面是否跳转', () => {
    expect(wrapper.vm.page_jump).toBe(false)
    wrapper.find('button').trigger('click')
    expect(wrapper.vm.page_jump).toBe(true)
  })
})
