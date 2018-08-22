/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import UserDetail from '@/adminviews/user/detail'
import Basic from '@/adminviews/basic/basic'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

const $route = {
  path: '/admin/user/detail',
  query: {'user_id': '001'}
}

describe('用户详情页面单元测试', () => {
  const wrapper = shallowMount(UserDetail, {
    mocks: {
      $route
    }
  })

  it('用户详情组件存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('测试按钮渲染数量', () => {
    expect(wrapper.findAll('button').length).toEqual(5)
  })

  // it('测试按钮文本改变', () => {
  //   wrapper.vm.is_banned = true
  //   expect(wrapper.findAll('button').at(1).text()).toBe('取消禁言')
  //   wrapper.findAll('button').at(1).trigger('click')
  //   expect(wrapper.findAll('button').at(1).text()).toBe('禁言用户')
  // })

  it('测试是否能够正确跳转到相关页面', () => {
    expect(wrapper.vm.page_jump_course).toBe(false)
    wrapper.findAll('button').at(4).trigger('click')
    expect(wrapper.vm.page_jump_course).toBe(true)
    expect(wrapper.vm.page_jump_order).toBe(false)
    wrapper.findAll('button').at(3).trigger('click')
    expect(wrapper.vm.page_jump_order).toBe(true)
  })
})
