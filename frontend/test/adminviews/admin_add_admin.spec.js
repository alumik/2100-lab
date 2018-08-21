/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AddAdmin from '@/adminviews/admin/add_admin.vue'

describe('新增管理员模块单元测验', () => {
  const wrapper = shallowMount(AddAdmin)

  it('标题是"新增管理员"', () => {
    expect(wrapper.find('h2').text()).toEqual('新增管理员')
  })
})
