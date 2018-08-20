<template>
  <!-- Sidebar  -->
  <nav id="sidebar">
    <div class="sidebar-header">后台管理</div>
    <ul class="components">
      <li
        v-for="list in lists"
        :key="list.id"
        :class="{active: list.isActive}">
        <a @click="jump(list.id)">{{ list.text }}</a>
      </li>
    </ul>
  </nav>
</template>

<script>
import './style/style.css'
export default {
  name: 'Menu',
  props: {
    lists: {
      type: Array,
      default: () => [
        {id: 1, text: '课程管理', isActive: false, path: '/admin/course'},
        {id: 2, text: '留言管理', isActive: false, path: '/admin/message'},
        {id: 3, text: '用户管理', isActive: false, path: '/admin/user'},
        {id: 4, text: '订单管理', isActive: false, path: '/admin/order'},
        {id: 5, text: '管理员管理', isActive: false, path: '/admin/adminmanagement'},
        {id: 6, text: '数据分析', isActive: false, path: '/admin/date'},
        {id: 7, text: '日志查询', isActive: false, path: '/admin/log'}
      ]
    }
  },
  methods: {
    jump: function (id) {
      this.$emit('jump', id)
      this.$router.push({path: this.lists[id - 1].path})
    }}
}
</script>

<style>
  #sidebar {
    position: fixed;
  }
</style>
