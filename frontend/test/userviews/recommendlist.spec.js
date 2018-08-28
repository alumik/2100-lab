/* eslint-disable no-undef */

import Vue from 'vue'
import RecommendList from '@/userviews/components/recommendList'
import {shallowMount} from '@vue/test-utils'
import BootstrapVue from 'bootstrap-vue'
import Vuex from "vuex";

Vue.use(BootstrapVue)

const $store = new Vuex.Store({
  state: {
    status: true,
    user: {
      is_new_customer: null,
      customer_id: '',
      username: '',
      avatar: null
    },
    phone: '',
    money: '',
    time: ''
  }
})

describe('推荐列表单元测试', () => {
  const wrapper = shallowMount(RecommendList, {
    mocks: {
      $store
    },
    propsData: {
      courselist: [
        {
          course_id: 1,
          title: '数据库',
          description: '床前明月光'
        },
        {
          course_id: 2,
          title: '数据库',
          description: '床前明月光'
        },
        {
          course_id: 3,
          title: '数据库',
          description: '床前明月光'
        },
        {
          course_id: 4,
          title: '数据库',
          description: '床前明月光'
        },
        {
          course_id: 5,
          title: '数据库',
          description: '床前明月光'
        },
        {
          course_id: 6,
          title: '数据库',
          description: '床前明月光'
        },
        {
          course_id: 7,
          title: '数据库',
          description: '床前明月光'
        },
        {
          course_id: 8,
          title: '数据库',
          description: '床前明月光'
        }
      ]
    }
  })

  it('列表名渲染', () => {
    expect(wrapper.contains('#list-title')).toBe(true)
  })

  it('更多按钮渲染', () => {
    expect(wrapper.contains('#watch-more')).toBe(true)
  })

  it('课程卡片渲染', () => {
    expect(wrapper.findAll('#course-card').length).toEqual(wrapper.vm.courselist.length)
  })
})
