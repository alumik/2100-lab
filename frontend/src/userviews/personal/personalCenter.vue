<template>
  <div>
    <b-navbar
      toggleable="md"
      type="dark"
      variant="info"
      class="navbar">

      <b-navbar-toggle
        target="nav_collapse"/>

      <b-navbar-brand
        href="#"
        disabled>2100实验室</b-navbar-brand>

      <b-collapse
        id="nav_collapse"
        is-nav>
        <b-navbar-nav class="ml-auto">

          <img
            src="../../assets/logo.png"
            class="img-rounded">

          <b-nav-text>用户一</b-nav-text>

          <b-nav-item
            href="#"
            right>
            注销
          </b-nav-item>
        </b-navbar-nav>

      </b-collapse>
    </b-navbar>
    <b-card no-body>
      <b-tabs
        pills
        card
        vertical>
        <b-tab
          title="查看学习记录"
          active>
          Tab Contents 1
        </b-tab>
        <b-tab title="查看订单记录">
          Tab Contents 2
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
export default {
  name: 'PersonalCenter'
}
</script>

<style scoped>
  img {
    width: 40px;
    height: 40px;
  }
</style>
