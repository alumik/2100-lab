<template>
  <Basic>
    <div class="body">
      <b-alert
        :show="created_test"
        variant="danger"
        dismissible
        fade
        @dismissed="created_test = false">
        {{ created_error_msg }}
      </b-alert>
      <AllCourseList
        id="all-free"
        :page_title="page_title"
        :another_page_title="another_page_title"
        :course_list="course_list"
        :rows="rows"
        @change_page="change_page"
        @to_another_page="to_another_page"/>
    </div>
  </Basic>
</template>

<script>
import AllCourseList from '../components/allCourseList'
import Basic from '../components/basic'
import axios from 'axios'

export default {
  name: 'AllFreeCoursePage',
  components: {
    AllCourseList,
    Basic
  },
  /**
   * @returns {IterableIterator<{
   * page_title: string, 列表名称
   * course_list: Array, 课程列表
   * course_type: string, 课程类型（免费、付费）
   * page_limit: number, 每页将展示的课程数目
   * page: number, rows: number, 页码
   * created_test: boolean, 获取数据测试
   * created_error_msg: string 获取数据返回错误信息
   * }>
   * }
   */
  data () {
    return {
      page_title: '免费课程',
      another_page_title: '付费课程',
      course_list: [],
      course_type: 'free',
      page_limit: 15,
      page: 1,
      rows: 0,
      created_test: false,
      created_error_msg: ''
    }
  },
  /**
   * 向后端发送请求
   * 获取课程列表
   */
  created () {
    this.get_course_list()
  },
  methods: {
    /**
     * 点击子组件分页器
     * 改变父组件的页码
     */
    change_page: function (page) {
      let that = this
      that.page = page
      that.get_course_list()
    },
    /**
     * 获取课程列表
     * 发送数据：
     *   课程类型
     *   每页显示课程数
     *   当前页码
     *
     *   像后端发送请求
     *   得到回复，获取相应类型、相应数量课程列表
     *   得到错误，弹出错误信息 */
    get_course_list: function () {
      let that = this
      axios
        .get(
          'http://localhost/api/v1/courses/forestage/course' +
          '/get-course-list/',
          {
            params: {
              course_type: that.course_type,
              page_limit: that.page_limit,
              page: that.page
            }
          }
        )
        .then(function (response) {
          that.course_list = response.data.content
          that.rows = response.data.count
        })
        .catch(function (error) {
          that.created_test = true
          that.created_error_msg = error.response.data.message
        })
    },
    to_another_page: function () {
      this.$router.push({ path: '/allpaidcourse' })
    }
  }
}
</script>
