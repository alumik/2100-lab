/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import Basic from '@/adminviews/basic/basic'
import AdminNavbar from '@/adminviews/components/navbar.vue'
import Menu from '@/adminviews/components/menu'
import BreadCrumb from '@/components/breadCrumb'

describe('基本组件单元测验', () => {
  const wrapper = shallowMount(Basic)

  it('包含导航栏', () => {
    expect(wrapper.contains(AdminNavbar)).toBe(true)
  })

  it('包含侧栏菜单', () => {
    expect(wrapper.contains(Menu)).toBe(true)
  })

  it('包含面包屑', () => {
    expect(wrapper.contains(BreadCrumb)).toBe(true)
  })
})
