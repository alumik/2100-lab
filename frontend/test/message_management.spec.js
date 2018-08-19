/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import MessageManagement from '@/adminviews/message/management'
import AdminNavbar from '@/adminviews/components/navbar'
import Menu from '@/adminviews/components/menu'
import BreadCrumb from '@/components/breadCrumb'
import Pagination from '@/components/pagination'

describe('留言管理页面单元测试', () => {
  const wrapper = shallowMount(MessageManagement)

  it('留言管理组件存在', () => {
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

  it('包含翻页导航', () => {
    expect(wrapper.contains(Pagination)).toBe(true)
  })

  it('测试输入框渲染数量', () => {
    expect(wrapper.findAll("[type = 'text']").length).toEqual(4)
  })

  it('测试下拉菜单输入框数量', () => {
    expect(wrapper.findAll('select').length).toEqual(1)
  })

  it('测试按钮渲染数量', () => {
    const buttons_length = wrapper.findAll("[class='buttons']").length
    expect(wrapper.findAll('button').length).toEqual(3*buttons_length)
  })

  it('测试改变下拉菜单选项绑定数据是否改变', () => {
    wrapper.findAll('option').at(0).setSelected()
    expect(wrapper.vm.state).toBe('whole')
  })

  it('测试文本框输入是否正确', () => {
    const inputs = wrapper.findAll("[type='text']")
    const input_one = inputs.at(0)
    input_one.setValue('2018-08-19')
    expect(wrapper.vm.date).toBe('2018-08-19')
    const input_two = inputs.at(1)
    input_two.setValue('小红')
    expect(wrapper.vm.user).toBe('小红')
    const input_three = inputs.at(2)
    input_three.setValue('SOFT1')
    expect(wrapper.vm.course_code).toBe('SOFT1')
    const input_four = inputs.at(3)
    input_four.setValue('计算机')
    expect(wrapper.vm.course_name).toBe('计算机')
  })
})
