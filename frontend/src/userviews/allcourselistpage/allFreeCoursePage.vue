<template>
  <Basic>
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
      :course_list="course_list"
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
      page_title: '免费课程',
      course_list: [],
      course_type: 'free',
      page_limit: 15,
      page: 1,
      created_test: false,
      created_error_msg: ''
    }
  },
  created () {
    let that = this
    axios.get('http://localhost:8000/api/v1/courses/backstage/course/get-course-list/', { params: {
      course_type: that.course_type,
      page_limit: that.per_page,
      page: that.page
    }}).then(function (response) {
      that.course_list = response.content.data
    }).catch(function (error) {
      that.created_test = true
      that.created_error_msg = error
    })
  },
  methods: {
    change_page: function (page) {
      this.page = page
    }
  }
}
</script>
