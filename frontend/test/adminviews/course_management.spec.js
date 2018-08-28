/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import CourseManagement from '@/adminviews/course/management.vue'

describe('课程管理模块单元测验', () => {
  const wrapper = shallowMount(CourseManagement)

  it('标题是"课程列表"', () => {
    expect(wrapper.find('h1').text()).toEqual('课程列表')
  })

  it('渲染查询输入框', () => {
    expect(wrapper.findAll('[type=text]').length).toEqual(2)
  })

  it('输入查询内容正确显示', () => {
    wrapper.findAll('[type=text]').at(1).setValue('Data Structure')
    expect(wrapper.vm.title).toEqual('Data Structure')
  })

  it('测试查询为空时的page显示', () => {
    expect(wrapper.vm.page).toEqual(1)
    wrapper.vm.update_num_pages(0)
    expect(wrapper.vm.page).toEqual(1)
  })

  it('测试查询到时的page显示', () => {
    expect(wrapper.vm.page).toEqual(1)
    let s = wrapper.vm.update_num_pages(10)
    expect(s).toEqual(10)
  })

  it('测试翻页的page显示', () => {
    expect(wrapper.vm.page).toEqual(1)
    wrapper.vm.change_page(1)
    expect(wrapper.vm.page).toEqual(1)
  })

  it('测试删除照片', () => {
    wrapper.vm.image_data_list = ['', '']
    wrapper.vm.file_name_list = ['', '']
    expect(wrapper.vm.image_data_list.length).toEqual(2)
    expect(wrapper.vm.file_name_list.length).toEqual(2)
    wrapper.vm.delete_img(1)
    expect(wrapper.vm.image_data_list.length).toEqual(1)
    expect(wrapper.vm.file_name_list.length).toEqual(1)
  })

  it('测试删除已有封面照片', () => {
    wrapper.vm.delete_origin_list = []
    wrapper.vm.delete_origin_img(10)
    expect(wrapper.vm.delete_origin_list[0]).toEqual(10)
  })

  it('测试错误信息_1', () => {
    let s = wrapper.vm.init_error_message('Access denied.')
    expect(s).toEqual('用户无权限，拒绝访问')
  })

  it('测试错误信息_2', () => {
    let s = wrapper.vm.init_error_message('Object not found.')
    expect(s).toEqual('查询的对象不存在')
  })

  it('测试错误信息_3', () => {
    let s = wrapper.vm.init_error_message('')
    expect(s).toEqual('数据库查询出错')
  })
})
