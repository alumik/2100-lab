<template>
  <!-- Sidebar  -->
  <nav id="sidebar">
    <div class="sidebar-header">后台管理</div>

    <ul class="components">
      <li class="active">
        <a @click="jump('/admin/course')">课程管理</a>
      </li>
      <li>
        <a @click="jump('/admin/message')">留言管理</a>
      </li>
      <li>
        <a @click="jump('/admin/user')">用户管理</a>
      </li>
      <li>
        <a @click="jump('/admin/order')">订单管理</a>
      </li>
      <li>
        <a @click="jump('/admin/adminmanagement')">管理员管理</a>
      </li>
      <li>
        <a @click="jump('/admin/data')">数据分析</a>
      </li>
      <li>
        <a @click="jump('/admin/log')">日志查询</a>
      </li>
    </ul>
  </nav>
</template>

<script>
import './style/style.css'
export default {
  name: 'Menu',
  methods: {
    jump: function (paths) {
      this.$router.push({path: paths})
    }}
}
</script>
