import { shallowMount } from '@vue/test-utils'
import personalCenter from '@/userviews/personal/personalCenter.vue'

describe('personalCenter.vue', () => {
  const wrapper = shallowMount(personalCenter)
  const button = wrapper.find('b-btn')
  it('点击个人中心的"修改"按钮后按钮文本变为"保存"', () => {
    button.trigger('click')
    expect(wrapper.vm.status).toBe('保存')
  })
  it('昵称输入框文本可以编辑', () => {
    expect(wrapper.vm.disabled).toEqual(false)
  })
  it('点击"保存"按钮后按钮文本变为"修改"', () => {
    button.trigger('click')
    expect(wrapper.vm.status).toBe('修改')
  })
})
