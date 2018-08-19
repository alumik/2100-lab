/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import UserDetail from '@/adminviews/user/detail'
import AdminNavbar from '@/adminviews/components/navbar'
import Menu from '@/adminviews/components/menu'
import BreadCrumb from '@/components/breadCrumb'

const $route = {
  path: '/admin/message/detail',
  query: {'user_id': '001'}
}

describe('用户详情页面单元测试', () => {
  const wrapper = shallowMount(UserDetail, {
    mocks: {
      $route
    }
  })

  it('用户详情组件存在', () => {
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
    expect(wrapper.findAll('button').length).toEqual(5)
  })

  it('测试按钮文本改变', () => {
    wrapper.vm.is_banned = true
    expect(wrapper.findAll('button').at(1).text()).toBe('取消禁言')
    wrapper.findAll('button').at(1).trigger('click')
    expect(wrapper.findAll('button').at(1).text()).toBe('禁言用户')
  })
})
