/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AddAdminBasic from '@/adminviews/admin/components/add_admin_basic.vue'

describe('新增管理员模块单元测验', () => {
  const wrapper = shallowMount(AddAdminBasic)

  it('标题是"新增管理员"', () => {
    expect(wrapper.find('h2').text()).toEqual('新增管理员')
  })

  it('测试输入框渲染数量', () => {
    expect(wrapper.findAll("[type = 'text']").length).toEqual(1)
  })

  it('测试密码框渲染数量', () => {
    expect(wrapper.findAll("[type = 'password']").length).toEqual(2)
  })

  it('测试按钮渲染数量', () => {
    expect(wrapper.findAll('button').length).toEqual(1)
  })

  it('测试标签渲染数量', () => {
    expect(wrapper.findAll('label').length).toEqual(3)
  })
})
