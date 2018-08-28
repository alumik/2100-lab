/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import MessageDetail from '@/adminviews/message/detail'
import DetailTable from '@/adminviews/components/detail_table'
import Basic from '@/adminviews/basic/basic'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

const $route = {
  path: '/admin/message/detail',
  query: { message_id: 1001 }
}

describe('留言详情页面单元测试', () => {
  const wrapper = shallowMount(MessageDetail, {
    mocks: {
      $route
    }
  })

  it('测试留言详情组件是否存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('测试是否包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('测试按钮渲染数量', () => {
    expect(wrapper.findAll('a').length).toEqual(2)
  })

  it('测试是否包含表格', () => {
    expect(wrapper.contains(DetailTable)).toBe(true)
  })

  it('测试compute_state函数', () => {
    expect(wrapper.vm.compute_state(true)).toBe('已删除')
    expect(wrapper.vm.compute_state(false)).toBe('未删除')
  })

  it('测试computed_message函数', () => {
    const val1 = {
      created_at: '2018-08-05Z08:15',
      username: 'liu',
      course_codename: 'SOFT',
      course_title: 'Data',
      up_votes: 1,
      down_votes: 2,
      is_deleted: true,
      deleted_at: null,
      content: '123'
    }
    const result1 = [
      '2018-08-05',
      'liu',
      'SOFT',
      'Data',
      1,
      2,
      '已删除',
      '-',
      '123'
    ]
    expect(wrapper.vm.computed_message(val1)).toEqual(result1)
    const val2 = {
      created_at: '2018-08-05Z08:15',
      username: 'liu',
      course_codename: 'SOFT',
      course_title: 'Data',
      up_votes: 1,
      down_votes: 2,
      is_deleted: false,
      deleted_at: '2018-08-07Z08:15',
      content: '123'
    }
    const result2 = [
      '2018-08-05',
      'liu',
      'SOFT',
      'Data',
      1,
      2,
      '未删除',
      '2018-08-07',
      '123'
    ]
    expect(wrapper.vm.computed_message(val2)).toEqual(result2)
  })
})
