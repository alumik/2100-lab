/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AdminDetailBasic from '@/adminviews/admin/components/detail_basic.vue'

const $route = {
  path: '/admin/adminmanagement/detail',
  query: {'admin_id': 0}
}

describe('管理员详情模块单元测验', () => {
  const wrapper = shallowMount(AdminDetailBasic, {
    mocks: {
      $route
    }
  })

  it('标题是"管理员详情"', () => {
    expect(wrapper.find('h2').text()).toEqual('管理员详情')
  })
})
