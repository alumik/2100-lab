<template>
  <Basic :items="items">
    <AddAdminBasic class="my-content"/>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import AddAdminBasic from './components/add_admin_basic'
export default {
  name: 'AddAdmin',
  components: {AddAdminBasic, Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '管理员管理',
        href: '/admin/adminmanagement'
      }, {
        text: '新增管理员',
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
