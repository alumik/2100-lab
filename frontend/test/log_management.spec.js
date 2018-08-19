/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import LogManagement from '@/adminviews/log/management'
import AdminNavbar from '@/adminviews/components/navbar'
import Menu from '@/adminviews/components/menu'
import BreadCrumb from '@/components/breadCrumb'

describe('日志查询页面单元测试', () => {
  const wrapper = shallowMount(LogManagement)

  it('日志查询组件存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('包含导航栏', () => {
    expect(wrapper.contains(AdminNavbar)).toBe(true)
  })

  it('包含侧栏菜单', () => {
    expect(wrapper.contains(Menu)).toBe(true)
  })

  it('包含面包屑', () => {
    expect(wrapper.contains(BreadCrumb)).toBe(true)
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
})
