<template>
  <Basic :items="items">
    <div class="my-content">
      <h2>课程列表</h2>
      {{ error_message }}
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
                    v-model="codename"
                    type="text"
                    class="form-control col-5"
                    placeholder=""
                    @keyup.enter="change">
              </div></td>
              <td>
                <div class="input-group my-long-input">
                  <input
                    v-model="title"
                    type="text"
                    class="form-control col-6"
                    placeholder=""
                    @keyup.enter="change">
                </div>
              </td><td>
              <div/></td>
              <td class="my-td">
              <div/></td>
            </tr>
            <tr
              v-for="course in courses"
              :key="course.course_id">
              <td>{{ course.codename }}</td>
              <td>{{ course.title }}</td>
              <td>{{ course.updated_at }}</td>
              <div class="my-in-for-btn">
                <button
                  id="content"
                  type="button"
                  class="in-btn row btn-sm"
                  @click="jump(course.course_id + 1)"
                >详情</button>
                <button
                  id="edit"
                  type="button"
                  class="in-btn row btn-sm"
                  @click="jump(course.course_id * (-1) - 2)"
                >修改</button>
              </div>
            </tr>
          </tbody>
        </table>
      </div>
      <Pagination
        :rows="rows"
        :perpage="per_limit"
        @change="changePage"/>
    </div>
  </Basic>
</template>

<script>
import axios from 'axios'
import Basic from '../basic/basic'
import UploadPicture from './upload_picture'
import Pagination from '../../components/pagination'
export default {
  name: 'CourseManagement',
  components: {Pagination, UploadPicture, Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '课程管理',
        active: true
      }],
      courses: [],
      codename: '',
      title: '',
      rows: 0,
      error_message: '',
      per_limit: 8,
      page: 1
    }
  },
  created: function () {
    axios.get('http://localhost:8000/api/v1/courses/backstage/course-management/get-course-list', {
      params: {
        codename: '',
        title: '',
        page_limit: this.per_limit,
        page: 1
      }
    }).then(
      response => {
        this.rows = response.data.count
        let _course = []
        for (let data of response.data.content) {
          _course.push({'course_id': data['course_id'], 'codename': data['codename'], 'title': data['title'], 'updated_at': data['updated_at'].substring(0, 10)})
        }
        this.courses = _course
      }).catch(
      error => {
        this.error_message = '读取数据出错' + error.response.data.message
      }
    )
  },
  methods: {
    jump: function (id) {
      if (id === 0) {
        this.$router.push({name: 'AddCourse'})
      } else if (id === -1) {
        this.$refs.upload_picture.show()
      } else if (id > 0) {
        this.$router.push({name: 'BackendCourseDetail', query: {course_id: id - 1}})
      } else if (id < 0) {
        this.$router.push({name: 'EditCourse', query: {course_id: (-(id + 2)).toString()}})
      }
    },
    change: function () {
      axios.get('http://localhost:8000/api/v1/courses/backstage/course-management/get-course-list', {
        params: {
          codename: this.codename,
          title: this.title,
          page_limit: this.per_limit,
          page: this.page
        }
      }).then(
        response => {
          this.rows = response.data.count
          let _course = []
          for (let data of response.data.content) {
            _course.push({
              'course_id': data['course_id'],
              'codename': data['codename'],
              'title': data['title'],
              'updated_at': data['updated_at'].substring(0, 10)
            })
          }
          this.courses = _course
        }).catch(
        error => {
          this.error_message = '读取数据出错' + error
        }
      )
    },
    changePage: function (currentpage) {
      this.page = currentpage
      this.change()
    }
  }
}
</script>

<style scoped>
  .my-content {
    margin: 40px;
    text-align: left;
  }

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
