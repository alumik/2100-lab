<template>
  <div>
    <AdminNavbar style="min-width: 500px;"/>
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
