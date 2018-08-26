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

  it('全选函数测试', () => {
    expect(wrapper.vm.selected).toEqual([])
    wrapper.vm.toggle_all(false)
    expect(wrapper.vm.selected).toEqual([])
  })


  it('转换信息测试1_1', () => {
    let s = wrapper.vm.transfer_permission('comment_admin')
    expect(s).toEqual('评论管理权限')
  })

  it('转换信息测试2', () => {
    let s = wrapper.vm.reverse_permission('评论管理权限')
    expect(s).toEqual('comment_admin')
  })

  it('转换信息测试2_2', () => {
    let s = wrapper.vm.reverse_permission('课程管理权限')
    expect(s).toEqual('course_admin')
  })
})
