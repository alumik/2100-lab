/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import StudyLog from '@/userviews/personal/log/studyLog.vue'

describe('个人学习记录页面单元测试', () => {
  const wrapper = shallowMount(StudyLog)
  it('包含顶部导航栏', () => {
    expect(wrapper.contains('#menu')).toBe(true)
  })
  it('包含顶部面包屑', () => {
    expect(wrapper.contains('#breadcrumb')).toBe(true)
  })
  it('包含数据项', () => {
    expect(wrapper.contains('.content')).toBe(true)
  })
  it('包含底部页码栏', () => {
    expect(wrapper.contains('.my-0')).toBe(true)
  })
})
