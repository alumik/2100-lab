<template>
  <div>
    <UserNavbar/>
    <div id="div">
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
  div {
    height: 100%;
  }
  #div {
    height: calc(100% - 70px);
  }
</style>
