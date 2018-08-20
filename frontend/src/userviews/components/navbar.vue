<template>
  <b-navbar
    :sticky="true"
    toggleable="md"
    type="dark"
    variant="primary"
    class="my-navbar">
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
        <b-nav-item
          href="/personal">
          <img
            id="userimg"
            src="../../assets/logo.png">{{ user ? user.name : '' }}
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
  name: 'UserNavbar',
  props: {
    user: {
      type: Object,
      default: () => {
        return {
          name: '默认用户'
        }
      }
    }
  }
}
</script>

<style>
  .my-navbar {
    margin: 0;
    vertical-align: middle;
  }

  #userimg {
    width: 40px;
    height: 40px;
    margin-right: 20px;
    border-radius: 50%;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  }

  .logo {
    height: 50px;
    margin: 0;
    vertical-align: middle;
  }

  .logo img {
    height: 35px;
  }

  .nav-link {
    padding: 0;
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

  #userimg:hover {
    -webkit-filter: brightness(150%);
    filter: brightness(150%);
  }

  #logoimg:hover {
    -webkit-filter: brightness(150%);
    filter: brightness(150%);
  }

  #logout {
    padding: 6px;
  }

  @media (min-width: 780px) {
    button {
      display: none;
    }
  }
</style>
