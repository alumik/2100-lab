<template>
  <div>
    <div class="row">
      <div id="list">管理员列表</div>
      <button
        type="button"
        class="row btn btn-primary btn-sm"
        @click="add_new_admin"
      >新增管理员</button>
    </div>
    <table class="table table-striped">
      <thead>
        <tr>
          <th scope="col">管理员ID</th>
          <th scope="col">管理员账号</th>
          <th scope="col">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            <div class="input-group">
              <input
                type="text"
                class="form-control col-xs-2"
                placeholder="">
          </div></td>
          <td>
            <div class="input-group">
              <input
                type="text"
                class="form-control col-xs-2"
                placeholder="">
            </div>
          </td><td>
            <div class="input-group">
              <input
                type="text"
                class="form-control col-xs-2"
                placeholder="">
          </div></td>
        </tr>
        <tr
          v-for="user in users"
          :key="user.id">
          <td>{{ user.ID }}</td>
          <td>{{ user.name }}</td>
          <td>详情</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'AdminManagement',
  data: function () {
    return {
      users: [
        {'ID': '000000', 'name': 'DingQuan'},
        {'ID': '000001', 'name': 'DingQuan1'},
        {'ID': '000002', 'name': 'DingQuan2'},
        {'ID': '000000', 'name': 'DingQuan3'},
        {'ID': '000001', 'name': 'DingQuan4'},
        {'ID': '000002', 'name': 'DingQuan5'},
        {'ID': '000000', 'name': 'DingQuan6'},
        {'ID': '000001', 'name': 'DingQuan7'},
        {'ID': '000002', 'name': 'DingQuan8'}
      ]
    }
  },
  methods: {
    add_new_admin () {
      this.$emit('add_new_admin')
    }
  }
}
</script>

<style>
  .row {
    display: flex;
    flex-direction: row;
  }

  #list {
    margin-top: 3%;
    margin-left: 20%;
  }

  .btn {
    margin-top: 2%;
    margin-left: 50%;
  }

  .table {
    margin-top: 1%;
  }
</style>
