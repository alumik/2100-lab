<template>
  <nav id="sidebar">
    <div class="sidebar-header">个人中心</div>
    <ul class="components">
      <li
        v-for="item in list"
        :key="item.id"
        :class="{active: item.isActive}"
        @click="$emit('select', item.id)">
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
    list: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    jump: function (id) {
      if (id === 1) {
        this.$router.push({path: '/personal'})
      } else {
        this.$router.push({path: '/studylog'})
      }
    }
  }
}
</script>

<style scoped>

</style>
