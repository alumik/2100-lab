/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AddCourseBasic from '@/adminviews/course/components/add_course_basic.vue'
import UploadSource from '@/adminviews/course/components/upload_source'

describe('新增课程页面单元测验', () => {
  const wrapper = shallowMount(AddCourseBasic)

  it('标题是"新增课程"', () => {
    expect(wrapper.find('h2').text()).toEqual('新增课程')
  })

  it('包含上传资源组件', () => {
    expect(wrapper.contains(UploadSource)).toBe(true)
  })

  it('测试输入框渲染数量', () => {
    expect(wrapper.findAll("[type = 'text']").length).toEqual(6)
  })

  it('测试按钮渲染数量', () => {
    expect(wrapper.findAll('button').length).toEqual(1)
  })

  it('测试单位渲染数量', () => {
    expect(wrapper.findAll('span').length).toEqual(4)
  })

  it('测试单选按钮渲染数量', () => {
    expect(wrapper.findAll("[type='radio']").length).toEqual(2)
  })

  it('测试标签渲染数量', () => {
    expect(wrapper.findAll('label').length).toEqual(10)
  })

  it('测试多行输入渲染数量', () => {
    expect(wrapper.findAll('textarea').length).toEqual(1)
  })
})
