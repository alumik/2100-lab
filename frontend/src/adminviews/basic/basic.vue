<template>
  <div>
    <div class="container-fluid my-nav">
      <AdminNavbar/>
    </div>
    <div class="my-menu">
      <div>
        <Menu/>
      </div>
      <div class="container-fluid my-container">
        <div class="my-bread">
          <BreadCrumb :items="items"/>
        </div>
        <slot/>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
export default {
  name: 'Basic',
  components: {BreadCrumb, Menu, AdminNavbar},
  props: {
    items: {
      type: Array,
      default: null
    }
  }
}
</script>

<style scoped>
  .my-nav {
    min-width: 500px;
    padding: 0;
  }

  .my-menu {
    display: flex;
  }

  .my-container {
    padding: 0;
  }
</style>
