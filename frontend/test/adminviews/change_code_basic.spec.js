/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import ChangeCodeBasic from '@/adminviews/admin/components/change_code_basic.vue'

describe('修改密码模块单元测验', () => {
  const wrapper = shallowMount(ChangeCodeBasic)

  it('标题是"修改密码"', () => {
    expect(wrapper.find('h2').text()).toEqual('修改密码')
  })

  it('输入新密码', () => {
    expect(wrapper.vm.new_password).toEqual(null)
    wrapper.find('#newpassword').setValue('123456789')
    expect(wrapper.vm.new_password).toEqual('123456789')
  })

  it('再次输入新密码', () => {
    expect(wrapper.vm.new_password_again).toEqual(null)
    wrapper.find('#newpasswordagain').setValue('123456789')
    expect(wrapper.vm.new_password_again).toEqual('123456789')
  })
})
