<template>
  <div>
    <UserNavbar/>
    <slot/>
    <div class="footer">
      <p class="text-center">
        --- 2100实验室 ---
      </p>
    </div>
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

<style scoped>
.footer {
  min-height: 100px;
  max-height: 100px;
}
</style>
