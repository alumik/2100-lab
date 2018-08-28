/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import MessageManagement from '@/adminviews/message/management'
import Basic from '@/adminviews/basic/basic'
import Pagination from '@/components/pagination'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'
import VueI18n from 'vue-i18n'
import Vuex from 'vuex'
Vue.use(VueI18n)
Vue.use(Vuex)

const i18n = new VueI18n({})

Vue.use(BootstrapVue)

describe('留言管理页面单元测试', () => {
  const wrapper = shallowMount(MessageManagement, {i18n})

  it('测试留言管理组件是否存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('测试是否包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('测试是否包含标题', () => {
    expect(wrapper.contains('.head-title')).toBe(true)
  })

  it('测试是否包含翻页导航', () => {
    expect(wrapper.contains(Pagination)).toBe(true)
  })

  it('测试输入框渲染数量', () => {
    expect(wrapper.findAll("[type = 'text']").length).toEqual(3)
  })

  it('测试下拉菜单输入框数量', () => {
    expect(wrapper.findAll('select').length).toEqual(1)
  })

  it('测试按钮渲染数量', () => {
    const length = wrapper.findAll("[class='buttons']").length
    expect(wrapper.findAll('a').length).toEqual(3 * length)
  })

  it('测试改变下拉菜单选项绑定数据是否改变', () => {
    wrapper.findAll('option').at(0).setSelected()
    expect(wrapper.vm.state).toBe('whole')
  })

  it('测试文本框输入是否正确', () => {
    const inputs = wrapper.findAll("[type='text']")
    const input0 = inputs.at(0)
    input0.setValue('小红')
    expect(wrapper.vm.user).toBe('小红')
    const input1 = inputs.at(1)
    input1.setValue('SOFT1')
    expect(wrapper.vm.course_code).toBe('SOFT1')
    const input2 = inputs.at(2)
    input2.setValue('计算机')
    expect(wrapper.vm.course_name).toBe('计算机')
  })

  it('测试compute_date函数', () => {
    expect(wrapper.vm.compute_date('2018-08-05Z08:15')).toBe('2018-08-05')
  })

  it('测试compute_state函数', () => {
    expect(wrapper.vm.compute_state(true)).toBe('message.state3')
    expect(wrapper.vm.compute_state(false)).toBe('message.state2')
  })

  it('测试compute_username函数', () => {
    expect(wrapper.vm.compute_username('1_deleted_2')).toBe('1（已删除）')
    expect(wrapper.vm.compute_username('1')).toBe('1')
  })

  it('测试compute_message函数', () => {
    expect(wrapper.vm.compute_message('1234567890')).toBe('1234567...')
    expect(wrapper.vm.compute_message('12345')).toBe('12345')
  })

  it('测试change_page函数', () => {
    expect(wrapper.vm.page).toBe(1)
    wrapper.vm.change_page(2)
    expect(wrapper.vm.page).toBe(2)
  })
})
