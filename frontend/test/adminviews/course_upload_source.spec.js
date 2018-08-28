/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import UploadSource from '@/adminviews/course/upload_source.vue'

const $route = {
  path: '/admin/course/detail',
  query: {'course_id': 0}
}

describe('上传资源模块单元测试', () => {
  const wrapper = shallowMount(UploadSource, {
    mocks: {
      $route
    }
  })

  it('测试是否包含打开按钮', () => {
    expect(wrapper.contains('#manage-btn')).toBe(true)
  })
})
