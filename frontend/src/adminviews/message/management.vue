<template>
  <div>
    <AdminNavbar/>
    <BreadCrumb :items="items"/>
    <h4>留言列表</h4>
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
          <td>
            <div class="input-group">
              <input
                type="text"
                class="form-control"
                placeholder="">
            </div>
          </td>
          <td>
            <div class="input-group">
              <input
                type="text"
                class="form-control"
                placeholder="">
            </div>
          </td>
          <td>
            <div class="input-group">
              <input
                type="text"
                class="form-control"
                placeholder="">
            </div>
          </td>
          <td>
            <div class="input-group">
              <input
                type="text"
                class="form-control"
                placeholder="">
            </div>
          </td>
          <td/>
          <td
            class="dropdown-toggle"
            data-toggle="dropdown">
            状态选择
            <span class="caret"/>
          </td>
          <td/>
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
          <td class="buttons">
            <button
              type="button"
              class="btn-primary btn-xs">
              详情
            </button>
            <button
              type="button"
              class="btn-primary btn-xs">
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
</template>

<script>
import AdminNavbar from '../components/navbar'
import BreadCrumb from '../../components/breadCrumb'
import Pagination from '../../components/pagination'
let messages = [
  { data: '2018-08-10', user: '小红', courseCode: 'SOFT1', courseName: '计算机', message: '很好', state: '已删除' },
  { data: '2018-08-11', user: '小明', courseCode: 'English2', courseName: '口语', message: '还不错', state: '未删除' }
]
export default {
  name: 'MessageManagement',
  components: { AdminNavbar, BreadCrumb, Pagination },
  data () {
    return {
      items: [{
        text: 'Admin',
        to: { name: 'AdminNavBar' }
      }, {
        text: 'Manage',
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
  }
}
</script>

<style scoped>
  h4 {
    padding-left: 2vh;
    text-align: left;
  }

  .buttons {
    display: flex;
  }

  .input-group {
    width: 70%;
  }
</style>
