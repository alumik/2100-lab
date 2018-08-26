/* eslint-disable no-undef */

import { shallowMount } from '@vue/test-utils'
import AdminDetail from '@/adminviews/admin/detail.vue'
import ConfirmModal from '@/adminviews/components/InputModal.vue'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'

Vue.use(BootstrapVue)

const $route = {
  path: '/admin/adminmanagement/detail',
  query: {'admin_id': 0}
}

describe('管理员详情模块单元测验', () => {
  const wrapper = shallowMount(AdminDetail, {
    mocks: {
      $route
    }
  })

  it('标题是"管理员详情"', () => {
    expect(wrapper.find('h1').text()).toEqual('管理员详情')
  })

  it('传递参数信息到页面中', () => {
    expect(wrapper.vm.admin_id).toEqual(0)
  })

  const wrappers = shallowMount(AdminDetail, {
    mocks: {
      $route
    }
  })
})
