/* eslint-disable no-undef */

import { mount } from '@vue/test-utils'
import login from '@/userviews/personal/login.vue'

describe('登录页面单元测试', () => {
  const wrapper = mount(login)
  const button = wrapper.find('#send')
  it('点击登录页面的"获取验证码"按钮后按钮不可再被点击', () => {
    button.trigger('click')
    expect(wrapper.vm.disabled).toBe(true)
  })
})
