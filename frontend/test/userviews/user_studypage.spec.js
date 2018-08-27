/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import Basic from '@/userviews/components/basic.vue'
import StudyPage from '@/userviews/studypage/index.vue'

const $route = {
  path: '/studypage',
  query: {
    course_id: 1,
    page: 1
  }
}

describe('学习页面单元测验', () => {
  const wrapper = shallowMount(StudyPage, {
    mocks: {
      $route
    }
  })

  it('包含导航栏', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('包含图片播放区', () => {
    expect(wrapper.contains('#image')).toBe(true)
  })

  it('包含播放器', () => {
    expect(wrapper.contains('#audio')).toBe(true)
  })

  it('点击展开可以查看全部', () => {
    expect(wrapper.contains('#watch-all')).toBe(true)
  })

  it('留言板渲染', () => {
    expect(wrapper.contains('#message-board')).toBe(true)
  })
})
