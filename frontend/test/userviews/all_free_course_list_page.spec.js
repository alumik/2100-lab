/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AllFreeCoursePage from '@/userviews/allcourselistpage/allFreeCoursePage.vue'
import Basic from '@/userviews/components/basic.vue'

describe('全部免费课程单元测验', () => {
  const wrapper = shallowMount(AllFreeCoursePage)

  it('包含列表组件', () => {
    expect(wrapper.contains('#all-free')).toBe(true)
  })

  it('包含导航栏', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })
})
