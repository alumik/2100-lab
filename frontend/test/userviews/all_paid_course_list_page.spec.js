/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AllPaidCoursePage from '@/userviews/allcourselistpage/allPaidCoursePage.vue'

describe('全部付费课程单元测验', () => {
  const wrapper = shallowMount(AllPaidCoursePage)

  it('包含列表组件', () => {
    expect(wrapper.contains('#all-paid')).toBe(true)
  })
})
