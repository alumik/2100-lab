<template>
  <nav
    id="sidebar"
    :class="{hide: menu_hide, 'sidebar': true}">
    <div
      class="sidebar-header"
      @click="$router.push({path: '/admin/main'})">{{ $t('menu.header') }}</div>
    <ul class="components">
      <li
        v-for="list in lists"
        :key="list.id"
        :class="{active: $store.state.menu === list.id}">
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
    menu_hide: {
      type: Boolean,
      default: true
    },
    lists: {
      type: Array,
      default: () => [
        {
          id: 1,
          text: this.$t('menu.course'),
          isActive: false,
          path: '/admin/course'
        },
        {
          id: 2,
          text: this.$t('menu.message'),
          isActive: false,
          path: '/admin/message'
        },
        {
          id: 3,
          text: this.$t('menu.user'),
          isActive: false,
          path: '/admin/user'
        },
        {
          id: 4,
          text: this.$t('menu.order'),
          isActive: false,
          path: '/admin/order'
        },
        {
          id: 5,
          text: this.$t('menu.admin'),
          isActive: false,
          path: '/admin/adminmanagement'
        },
        {
          id: 6,
          text: this.$t('menu.data'),
          isActive: false,
          path: '/admin/data/total'
        },
        {
          id: 7,
          text: this.$t('menu.log'),
          isActive: false,
          path: '/admin/log'
        }
      ]
    }
  },
  watch: {
    menu_hide () {
      console.log(123)
    }
  },
  create () {},
  methods: {
    jump: function (id) {
      this.$emit('jump', id)
      this.$store.commit('menu', id)
      this.$router.push({ path: this.lists[id - 1].path })
    }
  }
}
</script>

<style>
#sidebar {
  position: fixed;
}

.sidebar-header,
a {
  cursor: pointer;
}
</style>
