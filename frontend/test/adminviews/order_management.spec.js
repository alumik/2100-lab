/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import OrderManagement from '@/adminviews/order/management'
import Basic from '@/adminviews/basic/basic'
import Pagination from '@/components/pagination'

describe('订单管理页面单元测试', () => {
  const wrapper = shallowMount(OrderManagement)

  it('订单管理组件存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
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
    const length = wrapper.findAll('tr').length
    expect(wrapper.findAll('.btn').length).toEqual(length - 2)
  })

  it('测试改变下拉菜单选项绑定数据是否改变', () => {
    wrapper.findAll('option').at(0).setSelected()
    expect(wrapper.vm.state).toBe('whole')
  })

  it('测试文本框输入是否正确', () => {
    const inputs = wrapper.findAll("[type='text']")
    const input0 = inputs.at(0)
    input0.setValue('1001')
    expect(wrapper.vm.order_code).toBe('1001')
    const input1 = inputs.at(1)
    input1.setValue('SOFT1')
    expect(wrapper.vm.course_code).toBe('SOFT1')
    const input2 = inputs.at(2)
    input2.setValue('计算机')
    expect(wrapper.vm.course_name).toBe('计算机')
    const input3 = inputs.at(3)
    input3.setValue('小红')
    expect(wrapper.vm.user).toBe('小红')
  })

  // it('测试是否进入订单详情页面', () => {
  //   const button = wrapper.find('button')
  //   expect(wrapper.vm.page_jump).toBe(false)
  //   button.trigger('click')
  //   expect(wrapper.vm.page_jump).toBe(true)
  // })
})
