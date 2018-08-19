<template>
  <Basic :items="items">
    <BackendCourseDetailBasic class="my-content"/>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import BackendCourseDetailBasic from './components/detail_basic'
export default {
  name: 'BackendCourseDetail',
  components: {BackendCourseDetailBasic, Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '课程管理',
        href: '/admin/course'
      }, {
        text: '课程详情',
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
