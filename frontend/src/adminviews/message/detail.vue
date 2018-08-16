<template>
  <div>
    <AdminNavbar
      style="min-width: 1000px;"/>
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
              class="btn btn-lg"
              style="margin-right: 10px;">
              回复留言
            </button>
            <b-modal
              id="reply"
              ref="modal"
              title="回复留言"
              centered
              ok-title="保存"
              cancel-title="关闭"
              @ok="handle_ok"
              @shown="clear_reply">
              <form @submit.stop.prevent="handle_submit">
                <textarea
                  v-model="reply"
                  class="form-control"
                  rows="3"
                  placeholder="请输入你要回复的内容"/>
              </form>
            </b-modal>
          </div>
          <div>
            <button
              v-b-modal.delete
              type="button"
              class="btn btn-lg">
              删除留言
            </button>
            <b-modal
              id="delete"
              ref="modal"
              title="确认删除"
              centered
              ok-title="确定"
              cancel-title="取消">
              <p id="delete_confirm">您确定要删除此条留言吗？</p>
            </b-modal>
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
export default {
  name: 'Message',
  components: {AdminNavbar, BreadCrumb, Menu},
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
      },
      reply: ''
    }
  },
  methods: {
    clear_reply () {
      this.reply = ''
    },
    handle_ok (evt) {
      if (!this.reply) {
        evt.preventDefault()
        alert('请输入内容后提交')
      } else {
        this.handle_submit()
      }
    },
    handle_submit () {
      this.clear_reply()
      this.$refs.modal.hide()
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

  #delete_confirm {
    text-align: left;
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
