<template>
  <div>
    <div>
      <AdminNavbar
        style="min-width: 500px;"/>
    </div>
    <div style="display: flex;">
      <div>
        <Menu/>
      </div>
      <div class="father container-fluid"/>
    </div>
  </div>
</template>

<script>
import Menu from './components/menu'
import AdminNavbar from './components/navbar'
export default {
  name: 'Main',
  components: {Menu, AdminNavbar}
}
</script>

<style scoped>
  .father {
    min-width: 500px;
    padding: 0;
  }
</style>
