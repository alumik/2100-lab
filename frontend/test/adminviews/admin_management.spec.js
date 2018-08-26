/* eslint-disable no-undef */

import { shallowMount, createLocalVue } from '@vue/test-utils'
import AdminManagement from '@/adminviews/admin/management.vue'
import VueRouter from 'vue-router'

const localVue = createLocalVue()
localVue.use(VueRouter)
const router = new VueRouter()

describe('管理员管理模块单元测验', () => {
  const wrapper = shallowMount(AdminManagement, {
    localVue,
    router
  })

  it('标题是"管理员列表"', () => {
    expect(wrapper.find('h1').text()).toEqual('管理员列表')
  })

  it('渲染查询输入框', () => {
    expect(wrapper.findAll('[type=text]').length).toEqual(2)
  })

  it('测试跳转到增加管理员界面', () => {
    expect(wrapper.vm.test_router).toBe(false)
    wrapper.vm.jump(-1)
    expect(wrapper.vm.test_router).toBe(true)
  })

  it('测试跳转到详情界面', () => {
    expect(wrapper.vm.query_id).toEqual(-1)
    wrapper.vm.jump(1)
    expect(wrapper.vm.query_id).toEqual(1)
  })

  it('测试进行页面跳转', () => {
    expect(wrapper.vm.page).toEqual(1)
    wrapper.vm.change_page(2)
    expect(wrapper.vm.page).toEqual(2)
  })
})
