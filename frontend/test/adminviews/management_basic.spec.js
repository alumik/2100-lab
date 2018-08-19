/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AdminManagementBasic from '@/adminviews/admin/components/management_basic.vue'

describe('管理员管理模块单元测验', () => {
  const wrapper = shallowMount(AdminManagementBasic)

  it('标题是"管理员列表"', () => {
    expect(wrapper.find('h2').text()).toEqual('管理员列表')
  })

  it('渲染查询输入框', () => {
    expect(wrapper.findAll('[type=text]').length).toEqual(2)
  })

  it('输入查询手机号内容正确显示', () => {
    wrapper.findAll('[type=text]').at(1).setValue('15222583257')
    expect(wrapper.vm.query_input[1]).toEqual('15222583257')
  })

  it('查询id为3的管理员', () => {
    expect(wrapper.vm.query_id).toEqual(-1)
    wrapper.findAll('[type=button]').at(4).trigger('click')
    expect(wrapper.vm.query_id).toEqual(3)
  })

  it('测试访问新增管理员页面', () => {
    expect(wrapper.vm.test_add_admin).toBe(false)
    wrapper.findAll('[type=button]').at(0).trigger('click')
    expect(wrapper.vm.test_add_admin).toBe(true)
  })
})
