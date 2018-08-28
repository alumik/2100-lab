/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import OrderLog from '@/userviews/personal/log/orderLog.vue'

describe('个人订单记录页面单元测试', () => {
  const wrapper = shallowMount(OrderLog)
  it('包含整个页面', () => {
    expect(wrapper.contains('#page')).toBe(true)
  })
  it('包含顶部导航栏', () => {
    expect(wrapper.contains('#nav')).toBe(true)
  })
  it('点击导航栏上的toggler后侧边栏收缩', () => {
    wrapper.vm.hide()
    expect(wrapper.vm.hidden).toBe(true)
  })
  it('包含左侧菜单栏', () => {
    expect(wrapper.contains('.menu')).toBe(true)
  })
  it('左侧菜单栏的"查看学习记录"处于高亮状态', () => {
    expect(wrapper.vm.list[1].isActive).toBe(true)
  })
  it('包含顶部面包屑', () => {
    expect(wrapper.contains('#breadcrumb')).toBe(true)
  })
  it('包含数据项', () => {
    expect(wrapper.contains('.content')).toBe(true)
  })
  it('包含底部页码栏', () => {
    expect(wrapper.contains('.my-0')).toBe(true)
  })
})
