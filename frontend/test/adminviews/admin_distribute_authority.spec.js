/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import DistributeAuthority from '@/adminviews/admin/distribute_authority.vue'

const $route = {
  path: '/admin/adminmanagement/distribution',
  query: {'admin_id': 0}
}

describe('分配权限模块单元测验', () => {
  const wrapper = shallowMount(DistributeAuthority, {
    mocks: {
      $route
    }
  })

  it('标题是"分配权限"', () => {
    expect(wrapper.find('h1').text()).toEqual('分配权限')
  })
})
