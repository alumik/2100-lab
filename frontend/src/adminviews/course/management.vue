<template>
  <div>
    <div>
      <AdminNavbar/>
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
              @click="add_new_course"
            >新增课程</button>
            <label>&nbsp;&nbsp;&nbsp;&nbsp;</label>
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
              <th scope="col-2">课程代码</th>
              <th scope="col-2">课程名</th>
              <th scope="col-4">修改时间</th>
              <th scope="col-4">操作</th>
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
              <td>
              <div/></td>
            </tr>
            <tr
              v-for="course in courses"
              :key="course.id">
              <td>{{ course.ID }}</td>
              <td>{{ course.name }}</td>
              <td>{{ course.change_time }}</td>
              <button
                type="button"
                class="in-btn row inner-btn btn-primary btn-sm"
                @click="detail_information"
              >详情</button>
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
  name: 'CourseManagement',
  components: {BreadCrumb, Menu, AdminNavbar},
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
      }]
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
    flex: 0 1 auto;
    flex-direction: row;
    justify-content: space-around;
    margin-top: 60px;
    margin-bottom: 60px;
  }

  .head-btn {
    display: flex;
    justify-content: space-around;
  }

  .my-list {
    position: relative;
    margin-right: 30%;
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
