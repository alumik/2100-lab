<template>
  <b-navbar
    :sticky="true"
    toggleable="md"
    type="dark"
    variant="primary"
    class="navbar">
    <button
      class="navbar-toggler"
      @click="$emit('hide')">
      <span class="navbar-toggler-icon"/>
    </button>
    <b-navbar-brand
      class="logo">
      <img
        id="logoimg"
        src="../../assets/2100logo.png">
    </b-navbar-brand>
    <b-navbar-toggle target="nav_collapse"/>
    <b-collapse
      id="nav_collapse"
      is-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-item>管理员一</b-nav-item>
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

  .logo {
    height: 50px;
    margin: 0;
    vertical-align: middle;
  }

  .logo img {
    height: 35px;
  }

  .navbar {
    min-width: 350px;
    padding: 15px 10px;
    background-color: #6f5499 !important;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  }

  .navbar-dark .navbar-nav .nav-link {
    color: #999;
  }

  .navbar-dark .navbar-nav .nav-link:hover,
  .navbar-dark .navbar-nav .nav-link:focus {
    color: #f00;
  }

  .navbar {
    padding: 10px 5px;
    background-color: #fff !important;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
    opacity: 0.8;
  }

  .navbar-toggler {
    background-color: #f00;
  }

  @media (min-width: 768px) {
    button {
      display: none;
    }
  }
</style>
