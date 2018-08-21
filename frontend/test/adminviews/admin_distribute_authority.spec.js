/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import DistributeAuthority from '@/adminviews/admin/distribute_authority.vue'

describe('分配权限模块单元测验', () => {
  const wrapper = shallowMount(DistributeAuthority)

  it('标题是"分配权限"', () => {
    expect(wrapper.find('h2').text()).toEqual('分配权限')
  })
})
