/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import DistributeAuthority from '@/adminviews/admin/distribute_authority.vue'

describe('分配权限模块单元测验', () => {
  const wrapper = shallowMount(DistributeAuthority)

  it('标题是"分配权限"', () => {
    expect(wrapper.find('h2').text()).toEqual('分配权限')
  })

  it('点击A组权限，选中a权限', () => {
    expect(wrapper.vm.auth_text.length).toEqual(0)
    wrapper.findAll('[type=button]').at(0).trigger('click')
    expect(wrapper.vm.auth_text.length).toEqual(1)
    expect(wrapper.vm.auth_text[0]).toEqual('a')
  })
})
