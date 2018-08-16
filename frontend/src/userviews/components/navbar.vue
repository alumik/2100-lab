<template>
  <b-navbar
    toggleable="md"
    type="dark"
    variant="primary"
    style="margin: 0">
    <button
      @click="$emit('hide')"><span class="navbar-toggler-icon"/></button>
    <b-navbar-brand
      href=""
      disabled>2100实验室
    </b-navbar-brand>
    <b-navbar-toggle target="nav_collapse"/>
    <b-collapse
      id="nav_collapse"
      is-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-item
          href="/personal">
          <img
          src="../../assets/logo.png">用户一
        </b-nav-item>
        <b-nav-item
          id="logout"
          href="/login">
          注销
        </b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  name: 'UserNavbar'
}
</script>

<style>
  img {
    width: 40px;
    height: 40px;
  }
  .navbar {
    padding: 15px 10px;
    background-color: #6f5499 !important;
    min-width: 350px;
    box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.2);
  }
  .nav-link {
    padding: 0;
  }
  #logout {
    padding: 6px;
  }
  @media (min-width: 768px) {
    button {
      display: none;
    }
  }
</style>
