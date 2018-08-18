<template>
  <div>
    <AdminNavbar id="navbar"/>
    <div class="div">
      <AdminMenu/>
    </div>
  </div>
</template>

<script>
import AdminMenu from './components/menu'
import AdminNavbar from './components/navbar'
export default {
  name: 'Main',
  components: {AdminMenu, AdminNavbar}
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
