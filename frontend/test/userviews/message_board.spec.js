/* eslint-disable no-undef */

import MessageBoard from '@/userviews/components/messageboard'
import {shallowMount} from '@vue/test-utils'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

describe('留言板单元测试', () => {
  const wrapper = shallowMount(MessageBoard)

  it('留言板', () => {
    expect(wrapper.contains('#message-board')).toBe(true)
  })

  it('留言数量', () => {
    expect(wrapper.findAll('#piece-of-message').length).toEqual(3)
  })

  it('留言输入', () => {
    expect(wrapper.contains('#input-message')).toBe(true)
  })

  it('点击“点赞”按钮点赞数加1', () => {
    const praiseNum = wrapper.vm.message_list[0].num_of_praise
    wrapper.findAll('#praise-button').at(0).trigger('click')
    expect(wrapper.vm.message_list[0].num_of_praise).toBe(praiseNum + 1)
  })

  it('点击“点踩”按钮点踩数加1', () => {
    const detestNum = wrapper.vm.message_list[0].num_of_detest
    wrapper.findAll('#detest-button').at(0).trigger('click')
    expect(wrapper.vm.message_list[0].num_of_detest).toBe(detestNum + 1)
  })
})
