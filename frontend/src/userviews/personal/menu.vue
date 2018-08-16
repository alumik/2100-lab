<template>
  <nav
    id="sidebar"
    :class="{hide: hidden, 'sidebar': true}">
    <div
      class="sidebar-header"
      @click="jump(0)">个人中心</div>
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
import './style/style.css'
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
        this.$router.push({path: '/personal/orderlog'})
      } else {
        this.$router.push({path: '/personal/studylog'})
      }
    }
  }
}
</script>

<style scoped>

</style>
