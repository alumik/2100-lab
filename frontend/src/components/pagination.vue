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
  /**
   * rows: number, 数据总条数
   * perpage: number 单页最大数据量
   */
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
  /**
   * @returns {{
   * page: number 当前页数
   * }}
   */
  data () {
    return {
      page: 1
    }
  },
  /**
   * 该函数改变页数，
   * 触发change函数。
   */
  methods: {
    change_page: function () {
      this.$emit('change', this.page)
    }
  }
}
</script>
