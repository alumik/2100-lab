/* eslint-disable no-undef */

import Vue from 'vue'
import PageNotFount from '@/userviews/pagenotfound/index'
import {shallowMount} from '@vue/test-utils'
import BootstrapVue from 'bootstrap-vue'
import Basic from '@/userviews/components/basic'

Vue.use(BootstrapVue)

describe('404页面', () => {
  const wrapper = shallowMount(PageNotFount)

  it('包含导航栏', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('包含导航栏', () => {
    expect(wrapper.contains('#pagenotfound')).toBe(true)
  })

  it('包含gif动图', () => {
    expect(wrapper.contains('#gif')).toBe(true)
  })

  it('包含提示信息', () => {
    expect(wrapper.contains('#remind')).toBe(true)
  })
})
