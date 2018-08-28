/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import InputModal from '@/adminviews/components/InputModal'

describe('InputModal单元测试', () => {
  const wrapper = shallowMount(InputModal)

  it('测试InputModal组件是否存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('测试是否包含textarea组件', () => {
    expect(wrapper.contains('textarea')).toBe(true)
  })

  it('测试clear_input函数', () => {
    wrapper.vm.input = '123'
    wrapper.vm.clear_input()
    expect(wrapper.vm.input).toBe('')
  })
})
