/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AddCourse from '@/adminviews/course/add_course.vue'

const $route = {
  path: '/admin/course/detail',
  query: {'course_id': 0}
}

describe('新增课程模块单元测验', () => {
  const wrapper = shallowMount(AddCourse, {
    mocks: {
      $route
    }
  })

  it('标题是"新增课程"', () => {
    expect(wrapper.find('h1').text()).toEqual('新增课程')
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

  it('接收到上传数据', () => {
    let s = []
    wrapper.vm.receive_uploaded_resource(s, s, '')
    expect(wrapper.vm.is_uploaded).toBe(true)
  })

  it('接收到排序数据', () => {
    let s = []
    wrapper.vm.receive_sorted_pictures(s)
    expect(wrapper.vm.image_file_list.length).toEqual(0)
  })

  it('接收到同步数据', () => {
    let s = []
    expect(wrapper.vm.image_file_list).toEqual(s)
    let t = ['', '', '']
    wrapper.vm.receive_sync_data(t)
    expect(wrapper.vm.image_file_list).toEqual(t)
  })
})
