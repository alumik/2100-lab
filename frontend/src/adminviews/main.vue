<template>
  <div>
    <Basic :items="items"/>
  </div>
</template>

<script>
import Basic from './basic/basic'
import AdminMenu from './components/menu'
import AdminNavbar from './components/navbar'
export default {
  name: 'Main',
  components: {AdminMenu, AdminNavbar, Basic},
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }]
    }
  }
}
</script>

<style scoped>
  #navbar {
    min-width: 500px;
  }

  div {
    height: 100%;
  }

  .div {
    display: flex;
    height: calc(100% - 70px);
  }
</style>
