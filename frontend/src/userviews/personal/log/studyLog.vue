<template>
  <div>
    <UserNavbar/>
    <div id="div">
      <UserMenu
        :list="list"/>
    </div>
  </div>
</template>
<script>
import UserNavbar from '../../components/navbar'
import UserMenu from '../menu'
export default {
  name: 'StudyLog',
  components: {
    UserNavbar,
    UserMenu
  },
  data: function () {
    return {
      list: [
        {id: 0, text: '查看学习记录', isActive: true},
        {id: 1, text: '查看订单记录', isActive: false}
      ]
    }
  },
  methods: {
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
