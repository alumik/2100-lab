/* eslint-disable no-undef */

import Vue from 'vue'
import AllCourseList from '@/userviews/components/allCourseList'
import {shallowMount} from '@vue/test-utils'
import BootstrapVue from 'bootstrap-vue'

Vue.use(BootstrapVue)

describe('全部课程单元测试', () => {
  const wrapper = shallowMount(AllCourseList, {
    propsData: {
      page_title: '免费课程',
      course_list: [
        {
          id: 1,
          name: '数据库',
          introduction: '床前明月光',
          src: 'https://picsum.photos/1024/480/?image=54',
          value: 0
        },
        {
          id: 2,
          name: '数据结构',
          introduction: '疑是地上霜',
          src: 'https://picsum.photos/1024/480/?image=54',
          value: 0
        },
        {
          id: 3,
          name: '线性代数',
          introduction: '举头望明月',
          src: 'https://picsum.photos/1024/480/?image=58',
          value: 0
        },
        {
          id: 4,
          name: '离散数学',
          introduction: '低头思故乡',
          src: 'https://picsum.photos/1024/480/?image=55',
          value: 0
        }
      ]
    }
  })

  it('列表名渲染', () => {
    expect(wrapper.contains('#page-title')).toBe(true)
  })

  it('课程列表渲染', () => {
    expect(wrapper.contains('#course-list')).toBe(true)
  })

  it('课程图片渲染', () => {
    expect(wrapper.findAll('#course-img').length).toEqual(wrapper.vm.course_list.length)
  })

  it('分页渲染', () => {
    expect(wrapper.contains('#pagination')).toBe(true)
  })
})
