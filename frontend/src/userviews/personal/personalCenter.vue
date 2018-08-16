<template>
  <div id="page">
    <UserNavbar @hide="hide"/>
    <div id="main">
      <UserMenu
        :list="list"
        :hidden="hidden"/>
      <b-container>
        <b-img
          thumbnail
          fluid
          src="https://picsum.photos/250/250/?image=54"
          alt="Thumbnail" />
        <button
          type="button"
          class="btn btn-warning btn-lg imgbtn">
          修改头像</button>
      </b-container>
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
  },
  data: function () {
    return {
      hidden: false,
      list: [
        {id: 0, text: '查看学习记录', isActive: false},
        {id: 1, text: '查看订单记录', isActive: false}
      ]
    }
  },
  methods: {
    hide: function () {
      this.hidden = !this.hidden
    }
  }
}
</script>

<style scoped>
  #page {
    height: 100%;
  }
  #main {
    display: flex;
    height: calc(100% - 70px);
  }
  b-container {
    max-height: 100px;
  }
  .imgbtn {
    position: relative;
    bottom: -106px;
  }
</style>
