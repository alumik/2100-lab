<template>
  <div>
    <BreadCrumb :items="items"/>
    <h4>留言详情</h4>
    <div class="buttons">
      <div>
        <button
          v-b-modal.reply
          type="button"
          class="btn-primary">
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
            <b-form-input
              v-model="name"
              type="text"
              placeholder="请输入你要回复的内容"/>
          </form>
        </b-modal>
      </div>
      <button
        type="button"
        class="btn-primary">
        删除留言
      </button>
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
</template>

<script>
import BreadCrumb from '../../components/breadCrumb'
export default {
  name: 'Message',
  components: {BreadCrumb},
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
      if (!this.name) {
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
  h4 {
    padding-left: 2vh;
    text-align: left;
  }

  .buttons {
    padding-right: 2vh;
    padding-bottom: 2vh;
    text-align: right;
  }

  .table {
    width: 98%;
    margin-right: 2vh;
    margin-left: 2vh;
  }
</style>
