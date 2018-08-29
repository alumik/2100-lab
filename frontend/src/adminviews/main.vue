<template>
  <div>
    <Basic :items="items"/>
  </div>
</template>

<script>
import Basic from './basic/basic'

export default {
  name: 'Main',
  components: { Basic },
  data () {
    return {
      items: [
        {
          text: '主页',
          href: '/admin/main'
        }
      ]
    }
  },
  mounted () {
    this.$store.commit('menu', 0)
    this.$store.commit('colors', -1)
  }
}
</script>

<style scoped>
div {
  height: 100%;
}
</style>
