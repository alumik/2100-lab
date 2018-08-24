<template>
  <Basic>
    <b-alert
      :show="created_test"
      variant="danger"
      dismissible
      fade
      @dismissed="created_test=false">
      {{ created_error_msg }}
    </b-alert>
    <AllCourseList
      id="all-paid"
      :page_title="page_title"
      :course_list="course_list"
      :rows="rows"
      @change_page="change_page"/>
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
  data () {
    return {
      page_title: '付费课程',
      course_list: [],
      course_type: 'paid',
      page: 1,
      page_limit: 15,
      rows: 0,
      created_test: false,
      created_error_msg: ''
    }
  },
  created () {
    this.getcourselist()
  },
  methods: {
    change_page: function (page) {
      let that = this
      that.page = page
      that.getcourselist()
    },
    getcourselist: function (page) {
      let that = this
      axios.get('http://localhost:8000/api/v1/courses/forestage/course/get-course-list/', { params: {
        course_type: that.course_type,
        page_limit: that.page_limit,
        page: that.page
      }}).then(function (response) {
        that.course_list = response.data.content
        that.rows = response.data.count
      }).catch(function (error) {
        that.created_test = true
        that.created_error_msg = error.response.data.message
      })
    }
  }
}
</script>
