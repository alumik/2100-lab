<template>
  <div class="table-div">
    <table class="table">
      <tbody class="w-100">
        <tr
          v-for="n in titles.length"
          :key="n"
          class="row mx-0">
          <td class="col-3">{{ titles[n-1] }}</td>
          <td class="col-9">{{ data[n-1] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'DetailTable',
  props: {
    titles: {
      type: Array,
      default: null
    },
    data: {
      type: Array,
      default: null
    }
  }
}
</script>

<style scoped>
.table-div {
  padding-right: 15px;
  padding-left: 15px;
  overflow-x: auto;
}

table {
  margin-bottom: 20px;
  font-size: 1rem;
  border-top: 1px solid #d3d9df;
  border-bottom: 1px solid #d3d9df;
}

td {
  word-break: break-all;
  vertical-align: middle;
}

.col-3 {
  font-weight: bold;
  color: #337ab7;
  background-color: #f3f4f6;
}

.col-9 {
  color: #748085;
}
</style>
