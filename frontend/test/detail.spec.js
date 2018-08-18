/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import Detail from '@/adminviews/course/detail.vue'

describe('add_course.vue', () => {
  it('标题是"课程详情"', () => {
    const wrapper = shallowMount(Detail)
    expect(wrapper.find('h2').text()).toBe('课程详情')
  })
})
