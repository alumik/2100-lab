/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import MessageManagement from '@/adminviews/message/management'
import AdminNavbar from '@/adminviews/components/navbar'
import Menu from '@/adminviews/components/menu'
import BreadCrumb from '@/components/breadCrumb'
import Pagination from '@/components/pagination'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

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
    const length = wrapper.findAll("[class='buttons']").length
    expect(wrapper.findAll('button').length).toEqual(3 * length)
  })

  it('测试改变下拉菜单选项绑定数据是否改变', () => {
    wrapper.findAll('option').at(0).setSelected()
    expect(wrapper.vm.state).toBe('whole')
  })

  it('测试文本框输入是否正确', () => {
    const inputs = wrapper.findAll("[type='text']")
    const input0 = inputs.at(0)
    input0.setValue('2018-08-19')
    expect(wrapper.vm.date).toBe('2018-08-19')
    const input1 = inputs.at(1)
    input1.setValue('小红')
    expect(wrapper.vm.user).toBe('小红')
    const input2 = inputs.at(2)
    input2.setValue('SOFT1')
    expect(wrapper.vm.course_code).toBe('SOFT1')
    const input3 = inputs.at(3)
    input3.setValue('计算机')
    expect(wrapper.vm.course_name).toBe('计算机')
  })
})