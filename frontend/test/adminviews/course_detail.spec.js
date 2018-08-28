/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import BackendCourseDetail from '@/adminviews/course/detail.vue'

const $route = {
  path: '/admin/course/detail',
  query: {'course_id': 0}
}

describe('课程详情模块单元测验', () => {
  const wrapper = shallowMount(BackendCourseDetail, {
    mocks: {
      $route
    }
  })

  it('标题是"课程详情"', () => {
    expect(wrapper.find('h1').text()).toEqual('课程详情')
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
