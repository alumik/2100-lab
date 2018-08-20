<template>
  <div>
    <AdminNavbar/>
    <div class="my-menu">
      <Menu
        :lists="lists"
        @jump="jump"/>
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
  },
  data () {
    return {
      lists: [
        {id: 1, text: '课程管理', isActive: false, path: '/admin/course'},
        {id: 2, text: '留言管理', isActive: false, path: '/admin/message'},
        {id: 3, text: '用户管理', isActive: false, path: '/admin/user'},
        {id: 4, text: '订单管理', isActive: false, path: '/admin/order'},
        {id: 5, text: '管理员管理', isActive: false, path: '/admin/adminmanagement'},
        {id: 6, text: '数据分析', isActive: false, path: '/admin/data'},
        {id: 7, text: '日志查询', isActive: false, path: '/admin/log'}
      ]}
  },
  methods: {
    jump (id) {
      for (let list = 0; list < 7; list = list + 1) {
        this.lists[list].isActive = false
      }
      this.lists[id - 1].isActive = true
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
    margin-left: 200px;
  }
</style>
