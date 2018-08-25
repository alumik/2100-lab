<template>
  <nav
    id="sidebar"
    ref="menu"
    :class="{hide: hidden, 'sidebar': true}">
    <div
      class="sidebar-header"
      @click="$router.push({path: '/admin/main'})">
      <simple-line-icons
        icon="home"
        class="head-icon"
        size="small"/>
      {{ $t('menu.header') }}
    </div>
    <ul class="components">
      <li
        v-for="i in lists.length"
        :key="i"
        :class="{active: $store.state.menu === i}">
        <a @click="jump(i)">
          <simple-line-icons
            :icon="icons[i-1]"
            class="icon"
            size="small"/>
          {{ lists[i-1].text }}</a>
      </li>
    </ul>
  </nav>
</template>

<script>
import './style/style.css'
export default {
  name: 'Menu',
  props: {
    hidden: {
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
          text: this.$t('menu.log'),
          isActive: false,
          path: '/admin/log'
        },
        {
          id: 6,
          text: this.$t('menu.data'),
          isActive: false,
          path: '/admin/data/total'
        },
        {
          id: 7,
          text: this.$t('menu.admin'),
          isActive: false,
          path: '/admin/adminmanagement'
        }
      ]
    }
  },
  data () {
    return {
      icons: ['notebook', 'note', 'people', 'calculator', 'user', 'chart', 'calendar']
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
  z-index: 9999;
  text-align: left;
}

.sidebar-header,
a {
  cursor: pointer;
}

.icon {
  width: 15px;
  height: 15px;
}

.head-icon {
  width: 20px;
  height: 20px;
}
</style>
