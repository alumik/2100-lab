<template>
  <nav
    id="sidebar"
    ref="menu"
    :class="{hide: hidden, 'sidemenu': true}">
    <div
      class="sidemenu-header"
      @click="$router.push({path: '/admin/main'})">
      {{ $t('menu.header') }}
    </div>
    <ul class="components">
      <li
        v-for="i in lists.length"
        v-show="$store.state.groups.includes(i)"
        :key="i"
        :class="{ active: $store.state.menu.toString() === i.toString() }">
        <a
          @click="jump(i)">
          <simple-line-icons
            :icon="icons[i-1]"
            :color="colors[i-1]"
            class="icon"
            size="small"/>
          {{ lists[i-1].text }}</a>
      </li>
    </ul>
  </nav>
</template>

<script>
import './style/admin_style.css'
import axios from 'axios'
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
      icons: [
        'notebook',
        'note',
        'people',
        'docs',
        'calendar',
        'chart',
        'user'
      ],
      colors: this.$store.state.colors
    }
  },
  computed: {
  },
  async created () {
    this.$store.commit('menu', sessionStorage.getItem('menu'))
    this.$store.commit('colors', sessionStorage.getItem('colors'))
    try {
      let response = await axios.post(
        'http://localhost/api/v1/core/auth/is-authenticated/',
        {
          withCredentials: true
        }
      )
      if (response.data.is_authenticated && response.data.is_staff) {
        this.$store.commit('status')
        this.$store.commit('groups', response.data.admin_groups)
      }
    } catch (error) {
      alert(error.message)
    }
  },
  methods: {
    jump: function (id) {
      this.$emit('jump', id)
      this.$store.commit('colors', id - 1)
      this.$store.commit('menu', id)
      this.$router.push({ path: this.lists[id - 1].path })
    }
  }
}
</script>

<style scoped>
#sidebar {
  position: fixed;
  text-align: left;
}

.sidemenu-header {
  text-align: center;
}

.sidemenu-header,
a {
  cursor: pointer;
}

.icon {
  width: 15px;
  height: 15px;
}
</style>
