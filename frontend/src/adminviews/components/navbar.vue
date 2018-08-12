<template>
  <b-navbar
    toggleable="md"
    type="dark"
    variant="info"
    class="navbar">

    <b-navbar-toggle target="nav_collapse"/>

    <b-navbar-brand
      href="#"
      disabled>2100实验室 管理后台
    </b-navbar-brand>

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
