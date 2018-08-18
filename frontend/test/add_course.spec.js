import { shallowMount } from '@vue/test-utils'
import AddCourse from '@/adminviews/course/add_course.vue'

describe('add_course.vue', () => {
  it('标题是"新增课程"', () => {
    const wrapper = shallowMount(AddCourse)
    expect(wrapper.find('h2').text()).toBe('新增课程')
  })
})
