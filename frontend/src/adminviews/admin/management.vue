<template>
  <Basic :items="items">
    <AdminManagementBasic class="my-content"/>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import AdminManagementBasic from './components/management_basic'
export default {
  name: 'AdminManagement',
  components: {AdminManagementBasic, Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '管理员管理',
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
