<template>
  <Basic :items="items">
    <AddCourseBasic class="my-content"/>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import AddCourseBasic from './components/add_course_basic'
export default {
  name: 'AddCourse',
  components: {AddCourseBasic, Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '课程管理',
        href: '/admin/course'
      }, {
        text: '新增课程',
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
