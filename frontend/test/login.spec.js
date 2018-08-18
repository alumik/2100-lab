import { shallowMount } from '@vue/test-utils'
import login from '../src/userviews/personal/login.vue'
import UserNavbar from '../src/userviews/components/navbar.vue'

describe('MessageToggle.vue', () => {
  it('toggles msg passed to Message when button is clicked', () => {
    const wrapper = shallowMount(login)
    const button = wrapper.find('#btn')
    button.trigger('click')
    // const MessageComponent = wrapper.find(Message)
    // expect(MessageComponent.props()).toEqual({msg: 'message'})
    // button.trigger('click')
    expect(wrapper.vm.value).toBe(undefined)
  })
})