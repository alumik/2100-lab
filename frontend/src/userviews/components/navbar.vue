<template>
  <b-navbar
    toggleable="md"
    type="dark"
    variant="info"
    class="navbar">

    <b-navbar-toggle target="nav_collapse"/>

    <b-navbar-brand
      href=""
      disabled>2100实验室
    </b-navbar-brand>

    <b-collapse
      id="nav_collapse"
      is-nav>
      <b-navbar-nav class="ml-auto">

        <img
          src="../../assets/logo.png"
          class="img-rounded">

        <b-nav-item href="/personal">用户一</b-nav-item>

        <b-nav-item
          href="/login"
          right>
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
</style>
