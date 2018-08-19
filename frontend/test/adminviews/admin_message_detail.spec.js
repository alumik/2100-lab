/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import MessageDetail from '@/adminviews/message/detail'
import AdminNavbar from '@/adminviews/components/navbar'
import Menu from '@/adminviews/components/menu'
import BreadCrumb from '@/components/breadCrumb'

const $route = {
  path: '/admin/message/detail',
  query: {'message_id': 1001}
}

describe('留言详情页面单元测试', () => {
  const wrapper = shallowMount(MessageDetail, {
    mocks: {
      $route
    }
  })

  it('留言详情组件存在', () => {
    expect(wrapper.exists()).toBe(true)
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

  it('测试按钮渲染数量', () => {
    expect(wrapper.findAll('button').length).toEqual(2)
  })
})
