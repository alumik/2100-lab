/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import RecommendList from '@/userviews/components/recommendList.vue'
import UserNavbar from '@/userviews/components/navbar.vue'
import Homepage from '@/userviews/homepage/index'

describe('用户首页单元测验', () => {
  const wrapper = shallowMount(Homepage)

  it('包含轮播图', () => {
    expect(wrapper.contains('#carousel')).toBe(true)
  })

  it('包含导航栏', () => {
    expect(wrapper.contains(UserNavbar)).toBe(true)
  })

  it('测试推荐列表渲染数量', () => {
    expect(wrapper.findAll(RecommendList).length).toEqual(2)
  })

  it('测试轮播图图片渲染数量', () => {
    expect(wrapper.findAll('.height-change').length).toEqual(4)
  })
})
