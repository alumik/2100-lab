/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import LogManagement from '@/adminviews/log/management'
import Basic from '@/adminviews/basic/basic'

describe('日志查询页面单元测试', () => {
  const wrapper = shallowMount(LogManagement)

  it('测试日志查询组件是否存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('测试是否包含Basic组件', () => {
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

  it('测试复选框渲染数量', () => {
    expect(wrapper.findAll('.outer').length).toBe(1)
    expect(wrapper.findAll('.inner').length).toBe(4)
  })

  it('测试indeterminate函数', () => {
    wrapper.vm.select1 = [1, 2, 3, 4]
    wrapper.vm.select2 = [5, 6, 7, 8]
    wrapper.vm.select3 = [9, 10, 11, 12]
    wrapper.vm.select4 = [13, 14, 15, 16]
    expect(wrapper.vm.indeterminate).toBe(false)
    wrapper.vm.select1 = []
    wrapper.vm.select2 = []
    wrapper.vm.select3 = []
    wrapper.vm.select4 = []
    expect(wrapper.vm.indeterminate).toBe(false)
    wrapper.vm.select1 = [1, 2]
    wrapper.vm.select2 = [5, 6, 7, 8]
    wrapper.vm.select3 = [9, 10, 11, 12]
    wrapper.vm.select4 = [13, 14, 15, 16]
    expect(wrapper.vm.indeterminate).toBe(true)
  })

  it('测试toggle_all函数', () => {
    expect(wrapper.vm.select1).toEqual([1, 2])
    wrapper.vm.toggle_all(true)
    expect(wrapper.vm.select1).toEqual([1, 2, 3, 4])
    wrapper.vm.toggle_all(false)
    expect(wrapper.vm.select1).toEqual([])
  })

  it('测试输入时间错误处理', () => {
    let temp = wrapper.vm.begin_date
    wrapper.vm.begin_date = wrapper.vm.end_date
    wrapper.vm.end_date = temp
    expect(wrapper.vm.wrong).toEqual('')
    expect(wrapper.vm.wrong_count_down).toBe(0)
    wrapper.find('button').trigger('click')
    expect(wrapper.vm.wrong).toEqual('您输入的查询日期有误！')
    expect(wrapper.vm.wrong_count_down).toBe(5)
  })
})
