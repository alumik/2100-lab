<template>
  <div>
    <h2>课程列表</h2>
    <div>
      <div class="head-btn">
        <button
          type="button"
          class="row btn btn-sm my-in-btn"
          @click="jump(0)"
        >新增课程</button>
      </div>
      <div class="head-btn">
        <button
          type="button"
          class="row btn btn-sm my-in-btn"
          @click="jump(-1)"
        >更换首页图片</button>
        <b-modal
          ref="upload_picture"
          size="lg"
          centered
          no-close-on-esc>
          <div slot="modal-header">
            <h3 class="float-left">更换首页图片</h3>
          </div>
          <b-container>
            <b-row
              align-v="center">
              <b-col>
                <h5 class="text-left">
                  图片资料
                </h5>
              </b-col>
            </b-row>
            <b-row>
              <UploadPicture
                upload_category="upload home cover pictures"/>
            </b-row>
          </b-container>
        </b-modal>
      </div>
    </div>
    <div class="my-table">
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
            <div/></td>
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
</template>

<script>
import Pagination from '../../../components/pagination'
import UploadPicture from './upload_picture'
export default {
  name: 'CourseManagementBasic',
  components: {UploadPicture, Pagination},
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
      rows: 20
    }
  },
  methods: {
    jump: function (id) {
      if (id === 0) {
        this.$router.push({name: 'AddCourse'})
      } else if (id === -1) {
        this.$refs.upload_picture.show()
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
  .head-btn {
    display: inline-block;
    float: right;
    margin-bottom: 20px;
  }

  .my-in-btn {
    margin-right: auto;
    margin-left: 50px;
  }

  .my-table {
    text-align: center;
  }

  .my-td {
    width: 250px;
  }

  .my-in-for-btn {
    display: flex;
  }

  #content {
    margin-top: 10px;
  }

  #edit {
    margin-top: 10px;
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
