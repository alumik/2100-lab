<template>
  <Basic :items="items">
    <EditCourseBasic class="my-content"/>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import EditCourseBasic from './components/edit_course_basic'
export default {
  name: 'EditCourse',
  components: {EditCourseBasic, Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '课程管理',
        href: '/admin/course'
      }, {
        text: 'A001',
        href: '/admin/course/detail'
      }, {
        text: '修改课程',
        active: true
      }]
    }
  }
}
</script>

<style scoped>
  .my-content {
    margin: 40px;
    text-align: left;
  }
</style>
