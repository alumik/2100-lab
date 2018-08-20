/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AllPaidCoursePage from '@/userviews/allcourselistpage/allPaidCoursePage.vue'
import Basic from '@/userviews/components/basic'

describe('全部付费课程单元测验', () => {
  const wrapper = shallowMount(AllPaidCoursePage)

  it('包含列表组件', () => {
    expect(wrapper.contains('#all-paid')).toBe(true)
  })

  it('包含导航栏', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })
})
