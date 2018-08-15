<template>
  <div>
    <UserNavbar/>
    <div>
      <UserMenu/>
    </div>
  </div>
</template>

<script>
import UserNavbar from '../components/navbar'
import UserMenu from './menu'
export default {
  name: 'PersonalCenter',
  components: {
    UserNavbar,
    UserMenu
  }
}
</script>

<style scoped>
  img {
    width: 40px;
    height: 40px;
  }
</style>
