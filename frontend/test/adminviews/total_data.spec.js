/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import TimeData from '@/adminviews/data/time_data'
import Basic from '@/adminviews/basic/basic'
import Alert from '@/components/alert'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

describe('数据分析页面2单元测试', () => {
  const wrapper = shallowMount(TimeData)

  it('数据分析页面2组件存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('测试错误信息', () => {
    expect(wrapper.find('#alert').isVisible()).toBe(true)
  })

  it('测试提示信息是否显示', () => {
    expect(wrapper.find('.data-empty').isVisible()).toBe(true)
  })
})
