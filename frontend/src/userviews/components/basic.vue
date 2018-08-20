<template>
  <div>
    <UserNavbar/>
    <slot/>
  </div>
</template>

<script>
import UserNavbar from './navbar.vue'

export default {
  name: 'Basic',
  components: {
    UserNavbar
  }
}
</script>

<style>
  .my-nav {
    min-width: 500px;
    padding: 0;
  }
</style>
