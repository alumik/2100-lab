/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import CourseManagement from '@/adminviews/course/management.vue'

describe('管理员管理模块单元测验', () => {
  const wrapper = shallowMount(CourseManagement)

  it('标题是"课程列表"', () => {
    expect(wrapper.find('h2').text()).toEqual('课程列表')
  })

  it('渲染查询输入框', () => {
    expect(wrapper.findAll('[type=text]').length).toEqual(2)
  })

  it('输入查询内容正确显示', () => {
    wrapper.findAll('[type=text]').at(1).setValue('Data Structure')
    expect(wrapper.vm.title).toEqual('Data Structure')
  })
})
