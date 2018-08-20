<template>
  <div>
    <b-pagination
      :total-rows="rows"
      :per-page="perpage"
      v-model="page"
      align="center"
      size="md"
      @input="change_page"/>
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
      page: 1
    }
  },
  methods: {
    change_page: function () {
      this.$emit('change', this.page)
    }
  }
}
</script>
