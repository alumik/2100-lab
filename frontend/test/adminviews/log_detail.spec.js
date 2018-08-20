/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import LogDetail from '@/adminviews/log/detail'
import Basic from '@/adminviews/basic/basic'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

const $route = {
  path: '/admin/log/detail',
  query: {'admin_id': 1001,
  begin_date: 1534702219,
  end_date: 1534702319,
  select: 'a'}
}

describe('日志详情页面单元测试', () => {
  const wrapper = shallowMount(LogDetail, {
    mocks: {
      $route
    }
  })

  it('日志详情组件存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })
})
