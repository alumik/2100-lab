<template>
  <Basic :items="items">
    <CourseManagementBasic class="my-content"/>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import CourseManagementBasic from './components/management_basic'
export default {
  name: 'CourseManagement',
  components: {CourseManagementBasic, Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '课程管理',
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
