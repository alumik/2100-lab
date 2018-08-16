<template>
  <div>
    <UserNavbar @hide="hide"/>
    <div id="div">
      <UserMenu
        :list="list"
        :hidden="hidden"/>
    </div>
  </div>
</template>

<script>
import UserNavbar from '../../components/navbar'
import UserMenu from '../menu'
export default {
  name: 'OrderLog',
  components: {
    UserNavbar,
    UserMenu
  },
  data: function () {
    return {
      hidden: false,
      list: [
        {id: 0, text: '查看学习记录', isActive: false},
        {id: 1, text: '查看订单记录', isActive: true}
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
