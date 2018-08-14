<template>
  <div>
    <b-pagination
      :total-rows="rows"
      v-model="currentPage"
      :per-page="perpage"
      align="center"
      size="md"/>
  </div>
</template>

<script>
export default {
  name: 'Pagination',
  props: {
    rows: {
      type: Number,
      default: 0
    },
    perpage: {
      type: Number,
      default: 10
    }
  },
  data () {
    return {
      currentPage: 1
    }
  }
}
</script>

<style scoped>
  #page {
    font-size: 1em;
  }
</style>
