/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import MessageManagement from '@/adminviews/message/management'
import Basic from '@/adminviews/basic/basic'
import Pagination from '@/components/pagination'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

describe('留言管理页面单元测试', () => {
  const wrapper = shallowMount(MessageManagement)

  it('留言管理组件存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('包含翻页导航', () => {
    expect(wrapper.contains(Pagination)).toBe(true)
  })

  it('测试输入框渲染数量', () => {
    expect(wrapper.findAll("[type = 'text']").length).toEqual(3)
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
    input0.setValue('小红')
    expect(wrapper.vm.user).toBe('小红')
    const input1 = inputs.at(1)
    input1.setValue('SOFT1')
    expect(wrapper.vm.course_code).toBe('SOFT1')
    const input2 = inputs.at(2)
    input2.setValue('计算机')
    expect(wrapper.vm.course_name).toBe('计算机')
  })
  //
  // it('测试是否进入留言详情页面', () => {
  //   const button = wrapper.find('button')
  //   expect(wrapper.vm.page_jump).toBe(false)
  //   button.trigger('click')
  //   expect(wrapper.vm.page_jump).toBe(true)
  // })
})
