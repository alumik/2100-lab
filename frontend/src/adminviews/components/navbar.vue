<template>
  <b-navbar
    :sticky="true"
    toggleable="md"
    type="dark"
    variant="primary"
    class="navbar">
    <button
      class="navbar-toggler"
      @click="$emit('hide')"><span class="navbar-toggler-icon"/></button>
    <b-navbar-brand disabled>2100实验室</b-navbar-brand>
    <b-navbar-toggle target="nav_collapse"/>
    <b-collapse
      id="nav_collapse"
      is-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-text>管理员一</b-nav-text>
        <b-nav-item
          href="#"
          right>
          注销
        </b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  name: 'AdminNavbar'
}
</script>

<style scoped>
  .navbar {
    min-width: 350px;
    padding: 15px 10px;
    background-color: #6f5499 !important;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  }

  @media (min-width: 768px) {
    button {
      display: none;
    }
  }
</style>
