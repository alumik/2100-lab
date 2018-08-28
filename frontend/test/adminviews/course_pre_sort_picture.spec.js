/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import PreSortPicture from '@/adminviews/course/pre_sort_picture.vue'

const $route = {
  path: '/admin/course/detail',
  query: {'course_id': 0}
}

describe('预排序图片模块单元测试', () => {
  const wrapper = shallowMount(PreSortPicture, {
    mocks: {
      $route
    }
  })

  it('测试是否包含打开按钮', () => {
    expect(wrapper.contains('#pre-sort-btn')).toBe(true)
  })
})
