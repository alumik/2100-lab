/* eslint-disable no-undef */

import { mount } from '@vue/test-utils'
import AdminLogin from '@/adminviews/login.vue'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

describe('登录页面单元测试', () => {
  it('标题是后台登录入口', () => {
    const wrapper = mount(AdminLogin)
    expect(wrapper.find('.my-head-second').text()).toEqual('后台登录入口')
  })

  it('手机号码只应该出现数字', () => {
    const wrapper = mount(AdminLogin)
    expect(wrapper.vm.phone_number).toEqual('')
    expect(wrapper.vm.error_message).toEqual('')
    wrapper.find("[type='text']").setValue('asaf')
    wrapper.find('#btn').trigger('click')
    expect(wrapper.vm.phone_number).toEqual('asaf')
    expect(wrapper.vm.error_message).toEqual('请输入一个正确的手机号！')
  })

  it('手机号码数字应该为13位', () => {
    const wrapper = mount(AdminLogin)
    expect(wrapper.vm.phone_number).toEqual('')
    expect(wrapper.vm.error_message).toEqual('')
    wrapper.find('[type=text]').setValue('123')
    wrapper.find('#btn').trigger('click')
    expect(wrapper.vm.phone_number).toEqual('123')
    expect(wrapper.vm.error_message).toEqual('请输入一个正确的手机号！')
  })

  it('用户输入密码错误提示', () => {
    const wrapper = mount(AdminLogin)
    expect(wrapper.vm.phone_number).toEqual('')
    wrapper.find('[type=text]').setValue('12345678901')
    wrapper.find('[type=password]').setValue('1234567')
    expect(wrapper.vm.phone_number).toEqual('12345678901')
    expect(wrapper.vm.password).toEqual('1234567')
    wrapper.find('#btn').trigger('click')
  })

  it('用户登录成功', (done) => {
    const wrapper = mount(AdminLogin)
    expect(wrapper.vm.phone_number).toEqual('')
    wrapper.find('[type=text]').setValue('12345678901')
    wrapper.find('[type=password]').setValue('1234567')
    expect(wrapper.vm.phone_number).toEqual('12345678901')
    expect(wrapper.vm.password).toEqual('1234567')
    wrapper.find('#btn').trigger('click')
    wrapper.vm.$nextTick(() => {
      expect(wrapper.vm.error_message).toEqual('')
      done()
    })
  })
})
