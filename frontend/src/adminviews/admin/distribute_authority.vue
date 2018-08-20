<template>
  <Basic :items="items">
    <DistributeAuthorityBasic class="my-content"/>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import DistributeAuthorityBasic from './components/distribute_authority_basic'
export default {
  name: 'DistributeAuthority',
  components: {DistributeAuthorityBasic, Basic},
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
        href: '/admin/adminmanagement/detail'
      }, {
        text: '分配权限',
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
