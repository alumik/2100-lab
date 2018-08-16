<template>
  <div>
    <AdminNavbar style="min-width: 500px;"/>
    <div class="div">
      <AdminMenu/>
      <div class="father container-fluid">
        <BreadCrumb :items="items"/>
      </div>
    </div>
  </div>
</template>

<script>
import BreadCrumb from '../components/breadCrumb'
import AdminMenu from './components/menu'
import AdminNavbar from './components/navbar'
export default {
  name: 'Main',
  components: {AdminMenu, AdminNavbar, BreadCrumb},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '',
        active: true
      }]
    }
  }
}
</script>

<style scoped>
  .father {
    min-width: 500px;
    padding: 0;
  }
  div {
    height: 100%;
  }
  .div {
    display: flex;
    height: calc(100% - 70px);
  }
</style>
