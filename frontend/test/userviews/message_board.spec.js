/* eslint-disable no-undef */

import MessageBoard from '@/userviews/components/messageboard'
import Pagination from '@/components/pagination'
import {shallowMount} from '@vue/test-utils'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'
import Vuex from "vuex";

Vue.use(BootstrapVue)

const $route = {
  path: '/coursedetail',
  query: {
    referer_id: 1
  }
}

const $store = new Vuex.Store({
  state: {
    status: true,
    user: {
      is_new_customer: null,
      customer_id: '',
      username: '1',
      avatar: null
    },
    phone: '',
    money: '',
    time: ''
  }
})

describe('留言板单元测试', () => {
  const wrapper = shallowMount(MessageBoard, {
    mocks: {
      $route,
      $store
    }
  })

  wrapper.setData({
    message_list: [{
      username: '1',
      created_at: '2018-8-26',
      comment_id: 1,
      content: 'a',
      up_votes: 1,
      down_votes: 1,
      up_voted: false,
      down_voted: false,
      replies: []
    }],
    replies: [{
      username: '2',
      created_at: '2018-8-26',
      comment_id: 2,
      content: 'a',
      up_votes: 1,
      down_votes: 1,
      up_voted: false,
      down_voted: false
    }]
  })

  const numOfMessage = wrapper.vm.message_list.length

  it('留言板', () => {
    expect(wrapper.contains('#message-board')).toBe(true)
  })

  it('留言分页', () => {
    expect(wrapper.contains(Pagination)).toBe(true)
  })

  it('留言数量', () => {
    expect(wrapper.findAll('#piece-of-message').length).toEqual(numOfMessage)
  })

  it('全部回复弹窗渲染', () => {
    expect(wrapper.contains('#reply-popup')).toBe(true)
  })

  it('回复留言弹窗渲染', () => {
    wrapper.find('#reply-button').trigger('click')
    expect(wrapper.contains('#reply-popup')).toBe(true)
    expect(wrapper.contains('#reply-input')).toBe(true)
  })

  it('查看全部留言弹窗测试', () => {
    wrapper.find('#watch-more').trigger('click')
    expect(wrapper.contains('#reply-list-popup')).toBe(true)
  })

  it('查看全部留言分页测试', () => {
    wrapper.find('#watch-more').trigger('click')
    expect(wrapper.contains('#popup-pagination')).toBe(true)
  })

  it('查看全部留言留言列表测试', () => {
    wrapper.find('#watch-more').trigger('click')
    expect(wrapper.contains('#replies-list')).toBe(true)
  })

  it('删除留言按钮渲染', () => {
    expect(wrapper.contains('#delete-button')).toBe(true)
  })

  it('留言输入', () => {
    expect(wrapper.contains('#input-message')).toBe(true)
  })

  it('点击“点赞”按钮渲染', () => {
    expect(wrapper.contains('#praise-button')).toBe(true)
  })

  it('点击“点踩”按钮渲染', () => {
    expect(wrapper.contains('#detest-button')).toBe(true)
  })
})
