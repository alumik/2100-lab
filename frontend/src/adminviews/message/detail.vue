<template>
  <div>
    <AdminNavbar/>
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
              class="btn-primary btn-lg"
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
              @ok="handleOk"
              @shown="clearReply">
              <form @submit.stop.prevent="handleSubmit">
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
              class="btn-primary btn-lg">
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
              <td class="col-10">{{ message.courseCode }}</td>
            </tr>
            <tr class="row mx-0">
              <td class="col-2">课程名</td>
              <td class="col-10">{{ message.courseName }}</td>
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
        to: { name: 'AdminNavBar' }
      }, {
        text: '留言管理',
        to: { name: 'MessageManagement' }
      }, {
        text: '留言详情',
        active: true
      }],
      message: {
        data: '2018-08-10', user: '小红', courseCode: 'SOFT1', courseName: '计算机', message: '很好', state: '已删除'
      },
      reply: ''
    }
  },
  methods: {
    clearReply () {
      this.reply = ''
    },
    handleOk (evt) {
      // Prevent modal from closing
      evt.preventDefault()
      if (!this.reply) {
        alert('请输入内容后提交')
      } else {
        this.handleSubmit()
      }
    },
    handleSubmit () {
      this.clearReply()
      this.$refs.modal.hide()
    }
  }
}
</script>

<style scoped>
  h1 {
    padding-left: 15px;
    text-align: left;
  }

  .buttons {
    display: flex;
    justify-content: flex-end;
    padding-bottom: 15px;
    text-align: right;
  }

  #delete_confirm {
    text-align: left;
  }

  #body {
    display: flex;
    justify-content: space-between;
  }

  #detail {
    flex-basis: 100%;
    padding-right: 15px;
  }

  table {
    min-width: 800px;
    padding-right: 15px;
    margin-left: 15px;
    font-size: 1.5em;
  }
</style>
