/* eslint-disable no-undef */

import Vue from 'vue'
import RecommendList from '@/userviews/components/recommendList'
import {shallowMount} from '@vue/test-utils'
import BootstrapVue from 'bootstrap-vue'

Vue.use(BootstrapVue)

describe('推荐列表单元测试', () => {
  const wrapper = shallowMount(RecommendList, {
    propsData: {
      courselist: [
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
    expect(wrapper.contains('#list-title')).toBe(true)
  })

  it('更多按钮渲染', () => {
    expect(wrapper.contains('#watch-more')).toBe(true)
  })

  it('课程图片渲染', () => {
    expect(wrapper.findAll('#course-img').length).toEqual(wrapper.vm.courselist.length)
  })

  it('课程名称渲染', () => {
    expect(wrapper.findAll('#course-name').length).toEqual(wrapper.vm.courselist.length)
  })
})
