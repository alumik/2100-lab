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
