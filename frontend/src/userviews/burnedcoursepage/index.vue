<template>
  <div
    id="burnedcourse">
    <div>
      <UserNavbar/>
    </div>
    <div id="gif">
      <img src="../../assets/404.gif">
    </div>
    <div>
      <h4>Oops! 课程已焚毁</h4>
      <h4>如有问题请联系客服：152222761676</h4>
    </div>
  </div>
</template>

<script>
import UserNavbar from '../components/navbar'

export default {
  name: 'BurnedCourse',
  components: {
    UserNavbar
  }
}
</script>
