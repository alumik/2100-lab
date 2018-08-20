<template>
  <Basic :items="items">
    <AdminDetailBasic class="my-content"/>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import AdminDetailBasic from './components/detail_basic'
export default {
  name: 'AdminDetail',
  components: {Basic, AdminDetailBasic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '管理员管理',
        href: '/admin/adminmanagement'
      }, {
        text: '管理员详情',
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
