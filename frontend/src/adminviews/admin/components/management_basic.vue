<template>
  <div>
    <h2>管理员列表</h2>
    <button
      id="head-btn"
      type="button"
      class="btn btn-sm"
      @click="jump(-1)"
    >新增管理员</button>
    <div class="table-div">
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th scope="col">管理员ID</th>
            <th scope="col">管理员手机号</th>
            <th scope="col">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <div class="input-group">
                <input
                  v-model="query_input[0]"
                  type="text"
                  class="form-control col-xs-2"
                  placeholder="">
            </div></td>
            <td>
              <div class="input-group">
                <input
                  v-model="query_input[1]"
                  type="text"
                  class="form-control col-xs-2"
                  placeholder="">
              </div>
            </td><td>
            <div class="input-group"/></td>
          </tr>
          <tr
            v-for="admin in admins"
            :key="admin.id">
            <td>{{ admin.ID }}</td>
            <td>{{ admin.name }}</td>
            <button
              type="button"
              class="row inner-btn btn-sm"
              @click="jump(admin.id)"
            >详情</button>
          </tr>
        </tbody>
      </table>
    </div>
    <Pagination :rows="rows"/>
  </div>
</template>

<script>
import Pagination from '../../../components/pagination'
export default {
  name: 'AdminManagementBasic',
  components: {Pagination},
  data: function () {
    return {
      admins: [
        {'id': 0, 'ID': '000000', 'name': 'DingQuan'},
        {'id': 1, 'ID': '000001', 'name': 'DingQuan1'},
        {'id': 2, 'ID': '000002', 'name': 'DingQuan2'},
        {'id': 3, 'ID': '000000', 'name': 'DingQuan3'},
        {'id': 4, 'ID': '000001', 'name': 'DingQuan4'},
        {'id': 5, 'ID': '000002', 'name': 'DingQuan5'},
        {'id': 6, 'ID': '000000', 'name': 'DingQuan6'},
        {'id': 7, 'ID': '000001', 'name': 'DingQuan7'}
      ],
      rows: 20,
      query_input: [],
      query_id: -1,
      test_add_admin: false
    }
  },
  methods: {
    jump: function (id) {
      if (id === -1) {
        this.test_add_admin = true
        this.$router.push({name: 'AddAdmin'})
      } else {
        this.query_id = id
        this.$router.push({name: 'AdminDetail', query: {'admin_id': this.query_id}})
      }
    }
  }
}
</script>

<style scoped>
  #head-btn {
    display: inline-block;
    float: right;
    margin-bottom: 20px;
  }

  .inner-btn {
    margin-top: 2%;
    margin-left: 50%;
  }

  .table-div {
    text-align: center;
  }

  .table {
    border: 1px solid #d3d9df;
  }

  thead tr {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }

  #head-btn,
  .inner-btn {
    color: white;
    background-color: #8d4e91;
    border-color: #8d6592;
    border-radius: 10px;
    outline: none;
    box-shadow: #8d6592 inset;
  }

  #head-btn:hover,
  .inner-btn:hover,
  #head-btn:active,
  .inner-btn:active {
    background-color: #5e0057;
  }

</style>
