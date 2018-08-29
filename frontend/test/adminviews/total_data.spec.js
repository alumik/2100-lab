/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import TotalData from '@/adminviews/data/total_data'
import Basic from '@/adminviews/basic/basic'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

describe('数据分析页面1单元测试', () => {
  const wrapper = shallowMount(TotalData)

  it('数据分析页面1组件存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('测试是否包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('测试是否包含标题', () => {
    expect(wrapper.contains('.head-title')).toBe(true)
  })

  it('测试时间选择按钮渲染', () => {
    expect(wrapper.findAll('.time-btn').length).toBe(4)
  })

  it('测试错误信息', () => {
    expect(wrapper.find('#alert').isVisible()).toBe(true)
  })

  it('测试get_days函数', () => {
    expect(wrapper.vm.get_days()).toBe(1)
    wrapper.vm.buttons[0].state = false
    wrapper.vm.buttons[1].state = true
    expect(wrapper.vm.get_days()).toBe(7)
    wrapper.vm.buttons[1].state = false
    wrapper.vm.buttons[2].state = true
    expect(wrapper.vm.get_days()).toBe(31)
    wrapper.vm.buttons[2].state = false
    wrapper.vm.buttons[3].state = true
    expect(wrapper.vm.get_days()).toBe(182)
  })

  it('测试change_button_state函数', () => {
    wrapper.vm.change_button_state(0)
    expect(wrapper.vm.buttons[0].state).toBe(true)
    expect(wrapper.vm.buttons[1].state).toBe(false)
    expect(wrapper.vm.buttons[2].state).toBe(false)
    expect(wrapper.vm.buttons[3].state).toBe(false)
  })
})
