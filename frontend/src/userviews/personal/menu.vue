<template>
  <nav
    id="sidebar"
    :class="{hide: hidden, 'sidebar': true}">
    <div
      class="sidebar-header"
      @click="jump(2)">个人中心</div>
    <ul class="components">
      <li
        v-for="item in list"
        :key="item.id"
        :class="{active: item.isActive}">
        <a @click="jump(item.id)">{{ item.text }}</a>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'Menu',
  props: {
    hidden: {
      type: Boolean,
      default: true
    },
    list: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    jump: function (id) {
      if (id === 1) {
        this.$router.push({ path: '/personal/orderlog' })
      } else if (id === 0) {
        this.$router.push({ path: '/personal/studylog' })
      } else {
        this.$router.push({ path: '/personal' })
      }
    }
  }
}
</script>

<style scoped>
#sidebar {
  min-width: 200px;
  max-width: 200px;
  height: 100vh;
  color: darkblue;
  background: #f5f5f5;
  transition: all 0.3s;
}

@media (max-width: 768px) {
  .sidebar {
    margin-left: -200px;
  }
}

.hide {
  margin-left: 0;
}

#sidebar .sidebar-header {
  padding: 20px;
  font-size: 1.25rem;
  cursor: pointer;
  background: #f3f5ee;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.1) inset;
}

#sidebar ul.components {
  padding: 0;
  cursor: pointer;
}

a:hover,
a:focus {
  color: inherit;
  text-decoration: none;
  transition: all 0.3s;
}

#sidebar ul li a {
  display: block;
  padding: 10px;
  font-size: 1.1em;
  color: darkblue;
}

#sidebar ul li.active > a,
a[aria-expanded='true'] {
  color: dodgerblue;
  background-color: white;
}
</style>
