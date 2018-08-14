<template>
  <div>
    <AdminNavbar/>
    <div id="body">
      <Menu/>
      <div id="management">
        <BreadCrumb :items="items"/>
        <h1>留言列表</h1>
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
              <td style="width: 20vh;">
                <div class="input-group-sm">
                  <input
                    type="text"
                    class="form-control"
                    placeholder="">
                </div>
              </td>
              <td style="width: 20vh;">
                <div class="input-group-sm">
                  <input
                    type="text"
                    class="form-control"
                    placeholder="">
                </div>
              </td>
              <td style="width: 20vh;">
                <div class="input-group-sm">
                  <input
                    type="text"
                    class="form-control"
                    placeholder="">
                </div>
              </td>
              <td style="width: 20vh;">
                <div class="input-group-sm">
                  <input
                    type="text"
                    class="form-control"
                    placeholder="">
                </div>
              </td>
              <td style="width: 50vh;"/>
              <td
                style="width: 20vh;"
                class="dropdown-toggle"
                data-toggle="dropdown">
                状态
                <span class="caret"/>
              </td>
              <td style="width: 40vh;"/>
            </tr>
            <tr
              v-for="message in messages"
              :key="message.id">
              <td>{{ message.data }}</td>
              <td>{{ message.user }}</td>
              <td>{{ message.courseCode }}</td>
              <td>{{ message.courseName }}</td>
              <td>{{ message.message }}</td>
              <td> {{ message.state }} </td>
              <td
                class="buttons"
                style="padding-left: 5vh">
                <button
                  type="button"
                  class="btn-primary btn-xs"
                  @click="to_detail()">
                  详情
                </button>
                <button
                  type="button"
                  class="btn-primary btn-xs"
                >
                  回复
                </button>
                <button
                  type="button"
                  class="btn-primary btn-xs">
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>

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
let messages = [
  { data: '2018-08-10', user: '小红', courseCode: 'SOFT1', courseName: '计算机', message: '很好', state: '已删除' },
  { data: '2018-08-11', user: '小明', courseCode: 'English2', courseName: '口语', message: '还不错', state: '未删除' }
]
export default {
  name: 'MessageManagement',
  components: { Menu, AdminNavbar, BreadCrumb, Pagination },
  data () {
    return {
      items: [{
        text: '主页',
        to: { name: 'AdminNavBar' }
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
      ]
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
  h1 {
    padding-left: 2vh;
    margin-top: 4vh;
    margin-bottom: 4vh;
    text-align: left;
  }

  .buttons {
    display: flex;
  }

  table {
    min-width: 160vh;
    font-size: 1.2em;
  }

  #body {
    display: flex;
    justify-content: space-between;
  }

  .dropdown-toggle::after {
    position: static;
  }

  #management {
    flex-basis: 90%;
  }

  td button {
    margin-right: 1vh;
    margin-left: 1vh;
  }
</style>
