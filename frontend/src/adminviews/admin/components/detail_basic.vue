<template>
  <div>
    <h2>管理员详情</h2>
    <div class="button_group">
      <button
        type="button"
        class="row btn btn-sm"
        @click="jump(1)"
      >分配权限</button>
      <button
        type="button"
        class="row btn btn-sm"
        @click="jump(2)"
      >修改密码</button>
      <button
        v-b-modal.delete
        type="button"
        class="row btn btn-sm"
      >删除管理员</button>
      <ConfirmModal
        id="delete"
        title="确认删除"
        text="您确定要删除该管理员吗？"/>
    </div>
    <div class="table_div">
      <table
        class="table table-striped table-hover"
        width="100%">
        <tbody>
          <tr>
            <td class="head-td">
              testID
            </td>
            <td class="content-td">
              {{ admin_id }}
            </td>
          </tr>
          <tr>
            <td class="head-td">
              管理员ID
            </td>
            <td class="content-td">
              {{ admin.ID }}
            </td>
          </tr>
          <tr>
            <td class="head-td">
              管理员手机号
            </td>
            <td class="content-td">
              {{ admin.name }}
            </td>
          </tr>
          <tr>
            <td class="head-td">
              添加时间
            </td>
            <td class="content-td">
              {{ admin.create_time }}
            </td>
          </tr>
          <tr>
            <td class="head-td">
              修改时间
            </td>
            <td class="content-td">
              {{ admin.change_time }}
            </td>
          </tr>
          <tr>
            <td class="head-td">
              权限
            </td>
            <td class="content-td">
              {{ admin.authority }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import ConfirmModal from '../../components/ConfirmModal'
export default {
  name: 'AdminDetailBasic',
  components: {ConfirmModal},
  data: function () {
    return {
      admin: {
        'ID': '000001',
        'name': 'DINGQUAN',
        'create_time': '2018-08-13',
        'change_time': '2018-08-13',
        'authority': 'askcnkj'
      },
      admin_id: -1,
      test_router: -1
    }
  },
  created () {
    if (typeof (this.$route.query.admin_id) === 'number') {
      this.admin_id = this.$route.query.admin_id
    }
  },
  methods: {
    jump: function (id) {
      this.test_router = id
      if (id === 1) {
        this.$router.push({name: 'DistributeAuthority'})
      } else if (id === 2) {
        this.$router.push({name: 'ChangeCode'})
      }
    }
  }
}
</script>

<style scoped>
  .head-td {
    width: 35%;
  }

  .content-td {
    width: 65%;
  }

  .button_group {
    display: inline-block;
    float: right;
    margin-bottom: 20px;
  }

  .btn {
    margin-right: 25px;
    color: white;
    background-color: #8d4e91;
    border-color: #8d6592;
    border-radius: 10px;
    outline: none;
    box-shadow: #8d6592 inset;
  }

  .btn:hover,
  .btn:active {
    background-color: #5e0057;
  }
</style>
