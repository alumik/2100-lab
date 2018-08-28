/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import TimeData from '@/adminviews/data/time_data'
import Basic from '@/adminviews/basic/basic'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

describe('数据分析页面2单元测试', () => {
  const wrapper = shallowMount(TimeData)

  it('数据分析页面2组件存在', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('测试是否包含Basic组件', () => {
    expect(wrapper.contains(Basic)).toBe(true)
  })

  it('测试标题是否存在', () => {
    expect(wrapper.contains('.head-title')).toBe(true)
  })

  it('测试搜索框和图表是否存在', () => {
    expect(wrapper.contains('.search')).toBe(true)
    expect(wrapper.contains('.charts')).toBe(true)
  })

  it('测试错误信息', () => {
    expect(wrapper.find('#alert').isVisible()).toBe(true)
  })

  it('测试提示信息是否显示', () => {
    expect(wrapper.find('.data-empty').isVisible()).toBe(true)
  })

  it('测试get_step函数', () => {
    expect(wrapper.vm.get_step()).toBe(-1)
    wrapper.vm.month = '1.1'
    expect(wrapper.vm.get_step()).toBe(-2)
    wrapper.vm.month = '1'
    wrapper.vm.day = '2'
    expect(wrapper.vm.get_step()).toBe(32)
  })

  it('测试get_start_end_time函数', () => {
    let temp = wrapper.vm.begin_date
    wrapper.vm.begin_date = wrapper.vm.end_date
    wrapper.vm.end_date = temp
    expect(wrapper.vm.get_start_end_time()).toBe(-1)
    wrapper.vm.begin_date = '2018/08/20'
    wrapper.vm.end_date = '2018/08/28'
    expect(wrapper.vm.get_start_end_time()).toEqual([1534694400, 1535385600])
  })

  it('测试check_date函数', () => {
    wrapper.vm.month = ''
    wrapper.vm.day = ''
    expect(wrapper.vm.check_date()).toBe(-1)
    expect(wrapper.vm.wrong).toEqual('您所输入的时间有误')
    expect(wrapper.vm.wrong_count_down).toBe(5)
    wrapper.vm.month = '1.1'
    expect(wrapper.vm.check_date()).toBe(-1)
    expect(wrapper.vm.wrong).toEqual('请输入整数')
    expect(wrapper.vm.wrong_count_down).toBe(5)
    wrapper.vm.month = ''
    wrapper.vm.day = '1'
    wrapper.vm.begin_date = '2018/08/20'
    wrapper.vm.end_date = '2018/08/28'
    expect(wrapper.vm.check_date()).toEqual([1534694400, 1535385600, 1])
    wrapper.vm.begin_date = '2018/08/28'
    wrapper.vm.end_date = '2018/08/20'
    expect(wrapper.vm.check_date()).toBe(-1)
  })

  it('测试get_data函数', () => {
    const val = [
      {
        right_time: '2018-08-15Z008:15',
        data: {
          customers_count: 15,
          income: 1000.0,
          courses_count: 5,
          orders_count: 10
        }
      }
    ]
    expect(wrapper.vm.charts_users.rows).toEqual([])
    wrapper.vm.get_data(val)
    expect(wrapper.vm.charts_users.rows).toEqual([
      { 日期: '2018-08-15', 新增用户数: 15 }
    ])
  })
})
