/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import SyncPicture from '@/adminviews/course/synchronization.vue'

const $route = {
  path: '/admin/course/detail',
  query: {'course_id': 0}
}

describe('同步音图模块单元测试', () => {
  const wrapper = shallowMount(SyncPicture, {
    mocks: {
      $route
    }
  })

  it('测试是否包含打开按钮', () => {
    expect(wrapper.contains('#sync-btn')).toBe(true)
  })
})
