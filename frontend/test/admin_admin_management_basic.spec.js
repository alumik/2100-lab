/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AdminManagementBasic from '@/adminviews/admin/components/management_basic.vue'

describe('管理员管理模块单元测验', () => {
  const wrapper = shallowMount(AdminManagementBasic)

  it('标题是"管理员列表"', () => {
    expect(wrapper.find('h2').text()).toEqual('管理员列表')
  })
})
