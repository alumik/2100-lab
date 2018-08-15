<template>
  <div>
    <div>
      <AdminNavbar style="min-width: 500px;"/>
    </div>
    <div style="display: flex;">
      <div>
        <Menu/>
      </div>
      <div class="father container-fluid">
        <BreadCrumb :items="items"/>
        <div class="my-row">
          <h3 class="my-list">课程列表</h3>
          <div class="head-btn">
            <button
              type="button"
              class="row btn btn-primary btn-sm my-in-btn"
              style="margin-right: 15%;"
              @click="add_new_course"
            >新增课程</button>
            <button
              type="button"
              class="row btn btn-primary btn-sm my-in-btn"
              @click="add_new_course"
            >更换首页图片</button>
          </div>
        </div>
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
                <div class="input-group short-input">
                  <input
                    type="text"
                    class="form-control col-5"
                    placeholder="">
              </div></td>
              <td>
                <div class="input-group long-input">
                  <input
                    type="text"
                    class="form-control col-6"
                    placeholder="">
                </div>
              </td><td>
                <div class="input-group short-input">
                  <input
                    type="text"
                    class="form-control col-5"
                    placeholder="">
              </div></td>
              <td style="width: 250px;">
              <div/></td>
            </tr>
            <tr
              v-for="course in courses"
              :key="course.id">
              <td>{{ course.ID }}</td>
              <td>{{ course.name }}</td>
              <td>{{ course.change_time }}</td>
              <div style="display: flex;">
                <button
                  type="button"
                  class="in-btn row btn-primary btn-sm"
                  style="margin-right: -10px; margin-top: 10px;"
                  @click="detail_information"
                >详情</button>
                <button
                  type="button"
                  class="in-btn row btn-primary btn-sm"
                  style="margin-top: 10px;"
                  @click="detail_information"
                >修改</button>
              </div>
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
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
import Pagination from '../../components/pagination'
export default {
  name: 'CourseManagement',
  components: {Pagination, BreadCrumb, Menu, AdminNavbar},
  data: function () {
    return {
      courses: [
        {'ID': '000001', 'name': 'ABCDE', 'change_time': '2018-08-12'},
        {'ID': '000001', 'name': 'ABCDE', 'change_time': '2018-08-12'},
        {'ID': '000001', 'name': 'ABCDE', 'change_time': '2018-08-12'},
        {'ID': '000001', 'name': 'ABCDE', 'change_time': '2018-08-12'},
        {'ID': '000001', 'name': 'ABCDE', 'change_time': '2018-08-12'},
        {'ID': '000001', 'name': 'ABCDE', 'change_time': '2018-08-12'}
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
  }
}

</script>

<style>
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
    margin-top: 20px;
    margin-bottom: 10px;
  }

  .head-btn {
    display: flex;
    justify-content: space-around;
  }

  .my-list {
    margin-left: 25px;
  }

  .my-in-btn {
    margin-right: auto;
    margin-left: auto;
  }

  .long-input {
    margin-left: 25%;
  }

  .short-input {
    margin-left: 28%;
  }

  .in-btn {
    margin-right: auto;
    margin-left: auto;
  }
</style>
