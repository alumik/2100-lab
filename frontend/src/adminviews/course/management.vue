<template>
  <div class="my-head">
    <AdminNavbar class="my-navbar"/>
    <div class="my-menu">
      <Menu/>
      <div class="father container-fluid">
        <BreadCrumb :items="items"/>
        <div class="my-row">
          <h3 class="my-list">课程列表</h3>
          <div class="head-btn">
            <button
              type="button"
              class="row btn btn-sm my-in-btn"
              @click="jump(0)"
            >新增课程</button>
            <button
              type="button"
              class="row btn btn-sm my-in-btn"
              @click="jump(-1)"
            >更换首页图片</button>
          </div>
        </div>
        <div class="table_div">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th scope="col">课程代码</th>
                <th scope="col">课程名</th>
                <th scope="col">修改时间</th>
                <th scope="col">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <div class="input-group my-short-input">
                    <input
                      type="text"
                      class="form-control col-5"
                      placeholder="">
                </div></td>
                <td>
                  <div class="input-group my-long-input">
                    <input
                      type="text"
                      class="form-control col-6"
                      placeholder="">
                  </div>
                </td><td>
                  <div class="input-group my-short-input">
                    <input
                      type="text"
                      class="form-control col-5"
                      placeholder="">
                </div></td>
                <td class="my-td">
                <div/></td>
              </tr>
              <tr
                v-for="course in courses"
                :key="course.id">
                <td>{{ course.ID }}</td>
                <td>{{ course.name }}</td>
                <td>{{ course.change_time }}</td>
                <div class="my-in-for-btn">
                  <button
                    id="content"
                    type="button"
                    class="in-btn row btn-sm"
                    @click="jump(course.id + 1)"
                  >详情</button>
                  <button
                    id="edit"
                    type="button"
                    class="in-btn row btn-sm"
                    @click="jump(course.id * (-1) - 2)"
                  >修改</button>
                </div>
              </tr>
            </tbody>
          </table>
        </div>
        <Pagination :rows="rows"/>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
import Pagination from '../../components/pagination'
export default {
  name: 'CourseManagement',
  components: {Pagination, BreadCrumb, Menu, AdminNavbar},
  data: function () {
    return {
      courses: [
        {'id': 0, 'ID': '000001', 'name': 'ABCDE', 'change_time': '2018-08-12'},
        {'id': 1, 'ID': '000001', 'name': 'ABCDE', 'change_time': '2018-08-12'},
        {'id': 2, 'ID': '000001', 'name': 'ABCDE', 'change_time': '2018-08-12'},
        {'id': 3, 'ID': '000001', 'name': 'ABCDE', 'change_time': '2018-08-12'},
        {'id': 4, 'ID': '000001', 'name': 'ABCDE', 'change_time': '2018-08-12'},
        {'id': 5, 'ID': '000001', 'name': 'ABCDE', 'change_time': '2018-08-12'}
      ],
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '课程管理',
        active: true
      }],
      rows: 20
    }
  },
  methods: {
    jump: function (id) {
      if (id === 0) {
        this.$router.push({name: 'AddCourse'})
      } else if (id === -1) {
        this.$router.push({name: ''})
      } else if (id > 0) {
        this.$router.push({name: 'BackendCourseDetail'})
      } else if (id < 0) {
        this.$router.push({name: 'EditCourse'})
      }
    }
  }
}
</script>

<style scoped>
  .my-head {
    height: 100%;
  }

  .my-navbar {
    min-width: 500px;
  }

  .my-menu {
    display: flex;
    height: calc(100% - 70px);
  }

  .father {
    min-width: 500px;
    padding: 0;
    margin-left: 0;
    text-align: center;
  }

  .my-row {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-top: 30px;
    margin-bottom: 30px;
  }

  .my-in-btn {
    margin-right: 15%;
    margin-left: auto;
  }

  .my-td {
    width: 250px;
  }

  .my-in-for-btn {
    display: flex;
  }

  #content {
    margin-top: 10px;
    margin-right: -10px;
  }

  #edit {
    margin-top: 10px;
  }

  .head-btn {
    display: flex;
    justify-content: space-around;
    margin-right: 30px;
  }

  .my-list {
    margin-left: 25px;
  }

  .my-long-input {
    margin-left: 25%;
  }

  .my-short-input {
    margin-left: 28%;
  }

  .in-btn {
    margin-right: auto;
    margin-left: auto;
  }

  thead tr {
    font-weight: bold;
    color: white;
    background-color: #6c757d;
  }

  .table {
    border: 1px solid #d3d9df;
  }

  .table_div {
    padding-right: 15px;
    padding-left: 15px;
  }

  .btn,
  .in-btn {
    color: white;
    background-color: #8d4e91;
    border-color: #8d6592;
    border-radius: 10px;
    outline: none;
    box-shadow: #8d6592 inset;
  }

  .btn:hover,
  .in-btn:hover,
  .btn:active,
  .in-btn:active {
    background-color: #5e0057;
  }
</style>
