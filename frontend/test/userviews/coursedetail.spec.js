/* eslint-disable no-undef */

import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import CourseDetail from '@/userviews/coursedetail/index'
import Basic from '@/userviews/components/basic'
import {shallowMount} from '@vue/test-utils'
import Vuex from 'vuex'
Vue.use(Vuex)

Vue.use(BootstrapVue)

const $route = {
  path: '/coursedetail',
  query: {
    course_id: 1,
    referer_id: 1
  }
}

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

describe('课程详情页单元测试', () => {
  const wrapper = shallowMount(CourseDetail, {
    mocks: {
      $route,
      $store
    }
  })

  it('包含页面标题', () => {
    expect(wrapper.contains('#page-title')).toBe(true)
  })

  it('包含信息获取出错警告', () => {
    expect(wrapper.contains('#created_test_alert')).toBe(true)
  })

  it('包含点赞出错警告', () => {
    expect(wrapper.contains('#add_praise_alert')).toBe(true)
  })

  it('标题是课程名称', () => {
    expect(wrapper.contains('.content-style')).toBe(true)
  })

  it('包含导航栏', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('包含课程图片', () => {
    expect(wrapper.contains('#course-image')).toBe(true)
  })

  it('测试按钮数量', () => {
    expect(wrapper.findAll('.my-btn').length).toEqual(4)
  })

  it('测试课程简介渲染', () => {
    expect(wrapper.contains('.profile-style')).toBe(true)
  })

  it('点击按钮课程点赞数增加', () => {
    wrapper.find('#praise-button').trigger('click')
    expect(wrapper.vm.course.num_of_praise).toBe(wrapper.vm.course.num_of_praise)
  })

  it('点击分享按钮弹出模态框', () => {
    wrapper.find('#share-button').trigger('click')
    expect(wrapper.contains('#share-popup')).toBe(true)
  })

  it('分享模态框渲染提示语句', () => {
    wrapper.find('#share-button').trigger('click')
    expect(wrapper.contains('#share-popup-textarea')).toBe(true)
  })

  it('分享模态框渲染分享二维码', () => {
    wrapper.find('#share-button').trigger('click')
    expect(wrapper.contains('#share-qrcode')).toBe(true)
  })

  it('点击学习按钮弹出模态框', () => {
    wrapper.find('#study-button').trigger('click')
    expect(wrapper.contains('#study-popup')).toBe(true)
  })

  it('点击学习按钮渲染模态框', () => {
    wrapper.vm.start_study()
    expect(wrapper.contains('#time_reminder')).toBe(true)
  })

  it('课程简介渲染', () => {
    expect(wrapper.contains('#introduction')).toBe(true)
  })

  it('点击分享按钮弹出模态框', () => {
    wrapper.find('#pay-button').trigger('click')
    expect(wrapper.contains('#pay-popup')).toBe(true)
  })
})
