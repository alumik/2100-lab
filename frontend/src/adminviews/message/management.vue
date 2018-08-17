<template>
  <div class="html">
    <AdminNavbar id="navbar"/>
    <div id="body">
      <Menu/>
      <div id="management">
        <BreadCrumb :items="items"/>
        <h1>留言列表</h1>
        <div class="table_div">
          <table class="table table-striped">
            <thead>
              <tr>
                <td
                  v-for="title in titles"
                  :key="title.id">
                  {{ title.label }}
                </td>
              </tr>
            </thead>
            <tbody>
              <tr align="center">
                <td class="xs_td">
                  <div class="input-group-sm">
                    <input
                      type="text"
                      class="form-control"
                      placeholder="">
                  </div>
                </td>
                <td class="xs_td">
                  <div class="input-group-sm">
                    <input
                      type="text"
                      class="form-control"
                      placeholder="">
                  </div>
                </td>
                <td class="xs_td">
                  <div class="input-group-sm">
                    <input
                      type="text"
                      class="form-control"
                      placeholder="">
                  </div>
                </td>
                <td class="xs_td">
                  <div class="input-group-sm">
                    <input
                      type="text"
                      class="form-control"
                      placeholder="">
                  </div>
                </td>
                <td class="lg_td"/>
                <td class="s_td">
                  <div>
                    <select
                      v-model="state"
                      class="selectpicker">
                      <option value="whole">全部</option>
                      <option value="reserved">未删除</option>
                      <option value="deleted">已删除</option>
                    </select>
                  </div>
                </td>
                <td class="md_td"/>
              </tr>
              <tr
                v-for="message in messages"
                :key="message.id">
                <td>{{ message.data }}</td>
                <td>{{ message.user }}</td>
                <td>{{ message.course_code }}</td>
                <td>{{ message.course_name }}</td>
                <td>{{ message.message }}</td>
                <td> {{ message.state }} </td>
                <td class="buttons">
                  <button
                    type="button"
                    class="btn btn-xs"
                    @click="to_detail">
                    详情
                  </button>
                  <button
                    v-b-modal.reply
                    type="button"
                    class="btn">
                    回复
                  </button>
                  <button
                    v-b-modal.delete
                    type="button"
                    class="btn">
                    删除
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <InputModal
          id="reply"
          :input="reply"
          title="回复留言"
          placeholder="请输入你要回复的内容"/>
        <ConfirmModal
          id="delete"
          title="确认删除"
          text="您确定要删除此条留言吗？"/>
        <Pagination :rows="rows"/>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import BreadCrumb from '../../components/breadCrumb'
import Pagination from '../../components/pagination'
import Menu from '../components/menu'
import ConfirmModal from '../components/ConfirmModal'
import InputModal from '../components/InputModal'
let messages = [
  { data: '2018-08-10', user: '小红', course_code: 'SOFT1', course_name: '计算机', message: '很好', state: '已删除' },
  { data: '2018-08-11', user: '小明', course_code: 'English2', course_name: '口语', message: '还不错', state: '未删除' }
]
export default {
  name: 'MessageManagement',
  components: { InputModal, ConfirmModal, Menu, AdminNavbar, BreadCrumb, Pagination },
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '留言管理',
        active: true
      }],
      rows: 20,
      messages: messages,
      titles: [
        { label: '日期' },
        { label: '用户' },
        { label: '课程代码' },
        { label: '课程名' },
        { label: '留言' },
        { label: '状态' },
        { label: '操作' }
      ],
      state: null,
      reply: '123'
    }
  },
  methods: {
    to_detail: function () {
      this.$router.push({ path: '/admin/message/detail' })
    }
  }
}
</script>

<style scoped>
  #navbar {
    min-width: 1300px;
  }

  h1 {
    padding-left: 15px;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  .buttons {
    display: flex;
    padding-left: 30px;
  }

  table {
    font-size: 1.2em;
    border: 1px solid #d3d9df;
  }

  td {
    vertical-align: middle;
  }

  #body {
    display: flex;
    justify-content: space-between;
    min-width: 1300px;
    height: calc(100% - 70px);
  }

  #management {
    flex-basis: 100%;
    padding: 0;
  }

  td button {
    margin-right: 7px;
    margin-left: 7px;
    border-radius: 10px;
    outline: none;
    box-shadow: #adb5bd inset;
  }

  select {
    width: 130px;
    height: 30px;
    border-radius: 5px;
    outline: none;
  }

  option {
    font-size: 18px;
  }

  .html {
    height: 100%;
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

  thead tr {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }

  .xs_td {
    width: 160px;
  }

  .s_td {
    width: 200px;
  }

  .md_td {
    width: 270px;
  }

  .lg_td {
    width: 350px;
  }
</style>
