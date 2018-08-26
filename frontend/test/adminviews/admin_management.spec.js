/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AdminManagement from '@/adminviews/admin/management.vue'

describe('管理员管理模块单元测验', () => {
  const wrapper = shallowMount(AdminManagement)

  it('标题是"管理员列表"', () => {
    expect(wrapper.find('h1').text()).toEqual('管理员列表')
  })

  it('渲染查询输入框', () => {
    expect(wrapper.findAll('[type=text]').length).toEqual(2)
  })
})
