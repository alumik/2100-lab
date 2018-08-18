/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AddAdmin from '@/adminviews/admin/add_admin.vue'
import AdminNavbar from '@/adminviews/components/navbar.vue'
import Menu from '@/adminviews/components/menu'
import BreadCrumb from '@/components/breadCrumb'

describe('新增管理员页面单元测验', () => {
  const wrapper = shallowMount(AddAdmin)

  it('标题是"新增管理员"', () => {
    expect(wrapper.find('h2').text()).toEqual('新增管理员')
  })

  it('包含导航栏', () => {
    expect(wrapper.contains(AdminNavbar)).toBe(true)
  })

  it('包含侧栏菜单', () => {
    expect(wrapper.contains(Menu)).toBe(true)
  })

  it('包含面包屑', () => {
    expect(wrapper.contains(BreadCrumb)).toBe(true)
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
