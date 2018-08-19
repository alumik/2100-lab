/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import Course from '@/adminviews/user/course'
import Basic from '@/adminviews/basic/basic'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

const $route = {
  path: '/admin/user/detail/course',
  query: {'user_id': 1001}
}

describe('相关课程页面单元测试', () => {
  const wrapper = shallowMount(Course, {
    mocks: {
      $route
    }
  })

  it('相关课程组件存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })
})
