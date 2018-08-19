<template>
  <div class="table-div">
    <table class="table table-bordered">
      <tbody class="w-100">
        <tr
          v-for="n in titles.length"
          :key="n"
          class="row mx-0">
          <td class="col-2">{{ titles[n-1] }}</td>
          <td class="col-10">{{ data[n-1] }}</td>
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
  }

  table {
    font-size: 1.5em;
  }

  .col-2 {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }

  .col-10 {
    background-color: rgba(0, 0, 0, 0.05);
  }
</style>
