<template>
  <Basic :items="items">
    <ChangeCodeBasic class="my-content"/>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import ChangeCodeBasic from './components/change_code_basic'
export default {
  name: 'ChangeCode',
  components: {ChangeCodeBasic, Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '管理员管理',
        href: '/admin/adminmanagement'
      }, {
        text: '管理员详情',
        href: '/admin/adminmanagement/detail'
      }, {
        text: '修改密码',
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
