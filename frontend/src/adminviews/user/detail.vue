<template>
  <div>
    <AdminNavbar
      style="min-width: 920px;"/>
    <div id="body">
      <div>
        <Menu/>
      </div>
      <div id="detail">
        <BreadCrumb :items="items"/>
        <h1>用户详情</h1>
        <div class="buttons">
          <button
            type="button"
            class="btn-primary btn-lg"
            style="margin-right: 10px;">
            认证用户
          </button>
          <button
            type="button"
            class="btn-primary btn-lg"
            style="margin-right: 10px;">
            禁言用户
          </button>
          <button
            v-b-modal.delete
            type="button"
            class="btn-primary btn-lg"
            style="margin-right: 10px;">
            删除用户
          </button>
          <b-modal
            id="delete"
            ref="modal"
            title="确认删除"
            centered
            ok-title="确定"
            cancel-title="取消">
            <p id="delete_confirm">您确定要删除此用户吗？</p>
          </b-modal>
        </div>
        <table class="table table-bordered table-hover">
          <tbody class="w-100">
            <tr class="row mx-0">
              <td class="col-2">头像</td>
              <td class="col-10">
                <img :src="user.img">
              </td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">用户名</td>
              <td class="col-10">{{ user.name }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">手机号码</td>
              <td class="col-10">{{ user.phone }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">奖励金</td>
              <td class="col-10">{{ user.balance }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">注册时间</td>
              <td class="col-10">{{ user.register_time }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">修改时间</td>
              <td class="col-10">{{ user.change_time }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
export default {
  name: 'UserDetail',
  components: {BreadCrumb, AdminNavbar, Menu},
  data () {
    return {
      user: { img: require('../../assets/logo.png'),
        name: '小红',
        phone: '13102250001',
        balance: '15.00',
        register_time: '2018-01-01',
        change_time: '2018-08-01' },
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '用户管理',
        href: '/admin/user'
      }, {
        text: '用户详情',
        active: true
      }]
    }
  }
}
</script>

<style scoped>
  h1 {
    padding-left: 15px;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  .buttons {
    display: flex;
    justify-content: flex-end;
    padding-right: 15px;
    padding-bottom: 15px;
    text-align: right;
  }

  #body {
    display: flex;
    justify-content: space-between;
    min-width: 920px;
  }

  #detail {
    flex-basis: 100%;
    padding: 0;
  }

  table {
    font-size: 1.5em;
    text-align: center;
  }

  img {
    width: 40px;
  }

  #delete_confirm {
    text-align: left;
  }
</style>
