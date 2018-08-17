<template>
  <div>
    <AdminNavbar id="navbar"/>
    <div id="body">
      <div>
        <Menu/>
      </div>
      <div id="detail">
        <BreadCrumb :items="items"/>
        <h1>留言详情</h1>
        <div class="buttons">
          <div>
            <button
              v-b-modal.reply
              type="button"
              class="btn btn-lg">
              回复留言
            </button>
            <InputModal
              id="reply"
              title="回复留言"
              placeholder="请输入你要回复的内容"/>
          </div>
          <div>
            <button
              v-b-modal.delete
              type="button"
              class="btn btn-lg">
              删除留言
            </button>
            <ConfirmModal
              id="delete"
              title="确认删除"
              text="您确定要删除此条留言吗？"/>
          </div>
        </div>
        <div class="table_div">
          <table class="table table-bordered table-hover">
            <tbody class="w-100">
              <tr class="row mx-0">
                <td class="col-2">留言日期</td>
                <td class="col-10">{{ message.data }}</td>
              </tr>
              <tr class="row mx-0">
                <td class="col-2">用户</td>
                <td class="col-10">{{ message.user }}</td>
              </tr>
              <tr class="row mx-0">
                <td class="col-2">课程代码</td>
                <td class="col-10">{{ message.course_code }}</td>
              </tr>
              <tr class="row mx-0">
                <td class="col-2">课程名</td>
                <td class="col-10">{{ message.course_name }}</td>
              </tr>
              <tr class="row mx-0">
                <td class="col-2">状态</td>
                <td class="col-10">{{ message.state }}</td>
              </tr>
              <tr class="row mx-0">
                <td class="col-2">内容</td>
                <td class="col-10">{{ message.message }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BreadCrumb from '../../components/breadCrumb'
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import ConfirmModal from '../components/ConfirmModal'
import InputModal from '../components/InputModal'
export default {
  name: 'Message',
  components: {InputModal, ConfirmModal, AdminNavbar, BreadCrumb, Menu},
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '留言管理',
        href: '/admin/message'
      }, {
        text: '留言详情',
        active: true
      }],
      message: {
        data: '2018-08-10', user: '小红', course_code: 'SOFT1', course_name: '计算机', message: '很好', state: '已删除'
      }
    }
  }
}
</script>

<style scoped>
  #navbar {
    min-width: 1000px;
  }

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
    min-width: 1000px;
  }

  #detail {
    flex-basis: 100%;
    padding: 0;
  }

  table {
    font-size: 1.5em;
  }

  td {
    vertical-align: middle;
  }

  .table_div {
    padding-right: 15px;
    padding-left: 15px;
  }

  .btn {
    margin-right: 10px;
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

  .col-2 {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }

  .col-10 {
    background-color: rgba(0, 0, 0, 0.05);
  }
</style>
