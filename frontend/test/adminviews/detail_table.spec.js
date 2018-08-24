/* eslint-disable no-undef */

import {shallowMount} from '@vue/test-utils'
import DetailTable from '@/adminviews/components/detail_table'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

describe('DetailTable组件单元测试', () => {
  const wrapper = shallowMount(DetailTable,{
    propsData: {
      data: ['2018-08-02', '1310225', 'SOFT', 'Date Structure', '10', '12', '已删除', '2018-08-10', '很好'],
      titles: ['留言日期', '用户', '课程代码', '课程名', '点赞数', '点踩数', '状态', '删除日期', '内容']
    }})

  it('DetailTable组件存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('测试数据是否正常显示', () => {
    expect(wrapper.find('td').text()).toBe('留言日期')
    expect(wrapper.findAll('td').at(1).text()).toBe('2018-08-02')
  })

  it('测试table渲染', () => {
    expect(wrapper.findAll('td').length).toEqual(wrapper.vm.titles.length * 2)
  })
})
