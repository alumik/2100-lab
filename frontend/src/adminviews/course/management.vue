<template>
  <Basic :items="items">
    <div class="my-content">
      <div class="head-container">
        <div class="head-title">
          <h1>课程列表</h1>
          <Alert
            :count_down="wrong_count_down"
            :instruction="error_message"
            variant="danger"
            @decrease="wrong_count_down-1"
            @zero="wrong_count_down=0"/>
          <Alert
            :count_down="success_count_down"
            :instruction="error_message"
            variant="success"
            @decrease="success_count_down-1"
            @zero="success_count_down=0"/>
          <div class="my-btn-group">
            <a
              id="head-add-btn"
              class="btn"
              @click="jump(0)">
              <simple-line-icons
                id="add-icon"
                icon="user-follow"
                color="white"
                class="icon"/>
              新增课程
            </a>
            <a
              id="head-change-btn"
              class="btn"
              @click="jump(-1)">
              <simple-line-icons
                id="change-icon"
                icon="picture"
                color="white"
                class="icon"/>
              更换首页图片
            </a>
          </div>
        </div>
        <h6>第 {{ page }}/{{ num_pages }} 页，共 {{ rows }} 条数据</h6>
      </div>
      <b-modal
        ref="upload_picture"
        size="lg"
        centered
        no-close-on-esc>
        <div slot="modal-header">
          <h3 class="float-left">更换首页图片</h3>
        </div>
        <b-container>
          <b-row>
            <b-col>
              <h5 class="text-left">
                已有封面轮播图片列表
              </h5>
            </b-col>
          </b-row>
          <b-row class="my-row">
            <div
              v-for="image in origin_image_list"
              :key="image.hero_id"
              class="img-uploader-preview">
              <div class="preview-img">
                <b-img
                  :src="image.image"
                  thumbnail
                  fluid
                  alt="Thumbnail"/>
              </div>
              <img
                src="../../assets/close.png"
                class="img-uploader-delete-btn"
                @click="delete_origin_img(image.hero_id)">
            </div>
          </b-row>
          <b-row>
            <b-col>
              <h5 class="text-left">
                封面轮播图片上传区域
              </h5>
            </b-col>
          </b-row>
          <b-row class="content-row">
            <b-col
              ref="uploader"
              class="img-uploader"
              @drop="handle_drop">
              <p
                v-if="!has_images"
                class="img-uploader-placeholder">{{ placeholder }}</p>
              <div
                v-if="has_images"
                class="img-uploader-preview-list">
                <div
                  v-for="(data,index) in image_data_list"
                  :key="index"
                  class="img-uploader-preview">
                  <div class="preview-img">
                    <b-img
                      :src="data"
                      thumbnail
                      fluid
                      alt="Thumbnail"/>
                  </div>
                  <div
                    v-if="has_images"
                    class="img-uploader-mask">
                    <p
                      class="img-uploader-file-name"
                      @click="open_input()">
                      {{ placeholder }}</p>
                  </div>
                  <img
                    src="../../assets/close.png"
                    class="img-uploader-delete-btn"
                    @click="delete_img(index)">
                </div>
              </div>
              <label
                v-if="!has_images"
                for="inputID"
                class="img-uploader-label"/>
              <input
                id="inputID"
                ref="input"
                class="input-image col-lg-12"
                type="file"
                accept="image/gif,image/jpeg,image/jpg,image/png,image/svg"
                multiple="multiple"
                @change="handle_file_change">
            </b-col>
          </b-row>
          <b-row align-v="start">
            <b-col>
              <h5 class="text-left">
                文字输入区域 输入文字与图片为一一对应顺序，以换行为分隔符
              </h5>
            </b-col>
          </b-row>
          <b-row class="content-row">
            <b-col class="my-col">
              <textarea
                id="intro"
                v-model="input_content"
                class="form-control col-lg-12"
                rows="6s"/>
            </b-col>
          </b-row>
        </b-container>
        <div
          slot="modal-footer"
          class="w-100">
          <b-row class="define-btn">
            <b-col cols="8"/>
            <b-col cols="2">
              <a
                id="upload-btn"
                class="btn"
                @click="upload_data">
                上传
              </a>
            </b-col>
            <b-col cols="2">
              <a
                id="cancel-btn"
                class="btn"
                @click="hide_modal">
                取消
              </a>
            </b-col>
          </b-row>
        </div>
      </b-modal>
      <div class="table-div">
        <table class="table table-striped">
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
                <div class="input-group-sm my-input">
                  <input
                    v-model="codename"
                    type="text"
                    class="form-control"
                    placeholder=""
                    @keyup.enter="change">
                </div>
              </td>
              <td>
                <div class="input-group-sm">
                  <input
                    v-model="title"
                    type="text"
                    class="form-control"
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
              <td class="buttons">
                <a
                  id="detail-button"
                  class="btn"
                  @click="jump(course.course_id + 1)">
                  <simple-line-icons
                    icon="bubble"
                    color="#5b9bd1"
                    class="icon"
                    size="small"/>
                  详情
                </a>
                <a
                  id="change-button"
                  class="btn"
                  @click="jump(course.course_id * (-1) - 2)">
                  <simple-line-icons
                    icon="pencil"
                    color="green"
                    class="icon"
                    size="small"/>
                  修改
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <Pagination
        :rows="rows"
        :perpage="per_limit"
        @change="change_page"/>
    </div>
  </Basic>
</template>

<script>
import axios from 'axios'
import qs from 'qs'
import Basic from '../basic/basic'
import Pagination from '../../components/pagination'
import resize_image from './resize'
import Alert from '../../components/alert'
export default {
  name: 'CourseManagement',
  components: { Alert, Pagination, Basic },
  data: function () {
    return {
      items: [
        {
          text: '主页',
          href: '/admin/main'
        },
        {
          text: '课程管理',
          active: true
        }
      ],
      courses: [],
      codename: '',
      title: '',
      rows: 0,
      error_message: '',
      wrong_count_down: 0,
      success_count_down: 0,
      per_limit: 15,
      page: 1,
      num_pages: 0,
      placeholder: '点击上传图片',
      origin_image_list: [],
      image_data_list: [],
      file_name_list: [],
      delete_origin_list: [],
      input_content: ''
    }
  },
  computed: {
    has_images () {
      return this.image_data_list.length > 0
    }
  },
  created: function () {
    axios
      .get(
        'http://localhost/api/v1/courses/backstage/course-management/get-course-list',
        {
          params: {
            codename: '',
            title: '',
            page_limit: this.per_limit,
            page: 1
          }
        }
      )
      .then(response => {
        this.num_pages = this.update_num_pages(response.data.num_pages)
        this.rows = response.data.count
        let _course = []
        for (let data of response.data.content) {
          _course.push({
            course_id: data['course_id'],
            codename: data['codename'],
            title: data['title'],
            updated_at: data['updated_at'].substring(0, 10)
          })
        }
        this.courses = _course
      })
      .catch(error => {
        this.wrong_count_down = 0
        this.success_count_down = 0
        this.error_message = this.init_error_message(error.response.data.message)
        this.wrong_count_down = 5
      })
  },
  methods: {
    jump: function (id) {
      if (id === 0) {
        this.$router.push({ name: 'AddCourse' })
      } else if (id === -1) {
        axios
          .get(
            'http://localhost/api/v1/courses/forestage/main/get-heroes/'
          )
          .then(response => {
            this.origin_image_list = response.data.content
            for (let i = 0; i < this.origin_image_list.length; i++) {
              this.origin_image_list[i].image = this.$store.state.address.concat(
                this.origin_image_list[i].image
              )
            }
          })
          .catch(error => {
            this.wrong_count_down = 0
            this.success_count_down = 0
            this.error_message = this.init_error_message(error.response.data.message)
            this.wrong_count_down = 5
          })
        this.$refs.upload_picture.show()
      } else if (id > 0) {
        this.$router.push({
          name: 'BackendCourseDetail',
          query: { course_id: id - 1 }
        })
      } else if (id < 0) {
        this.$router.push({
          name: 'EditCourse',
          query: { course_id: (-(id + 2)).toString() }
        })
      }
    },
    change: function () {
      axios
        .get(
          'http://localhost/api/v1/courses/backstage/course-management/get-course-list',
          {
            params: {
              codename: this.codename,
              title: this.title,
              page_limit: this.per_limit,
              page: this.page
            }
          }
        )
        .then(response => {
          this.num_pages = this.update_num_pages(response.data.num_pages)
          this.rows = response.data.count
          let _course = []
          for (let data of response.data.content) {
            _course.push({
              course_id: data['course_id'],
              codename: data['codename'],
              title: data['title'],
              updated_at: data['updated_at'].substring(0, 10)
            })
          }
          this.courses = _course
        })
        .catch(error => {
          this.wrong_count_down = 0
          this.success_count_down = 0
          this.error_message = this.init_error_message(error.response.data.message)
          this.wrong_count_down = 5
        })
    },
    update_num_pages: function (page) {
      if (page === 0) {
        return 1
      } else {
        return page
      }
    },
    change_page: function (current_page) {
      this.page = current_page
      this.change()
    },
    handle_file_change () {
      let input = this.$refs.input
      let files = input.files
      this.preview(files)
    },
    handle_drop (e) {
      let files = e.dataTransfer.files
      this.preview(files)
    },
    open_input () {
      this.$refs.input.click()
    },
    delete_img (index) {
      this.image_data_list.splice(index, 1)
      this.file_name_list.splice(index, 1)
    },
    preview (files) {
      let _this = this
      if (!files || !window.FileReader) return

      for (let i = 0; i < files.length; i++) {
        let file = files[i]
        let reader = new FileReader()
        reader.onload = function (e) {
          resize_image(e.target.result, 150, 150, function (result) {
            _this.image_data_list.push(result)
            _this.file_name_list.push(file)
          })
        }
        reader.readAsDataURL(file)
      }
    },
    upload_data () {
      let update_text = this.input_content.split('\n')
      if (update_text.length < this.file_name_list.length) {
        for (let i = update_text.length; i < this.file_name_list.length; i++) {
          update_text[i] = ''
        }
      }
      let form_data = new FormData()
      for (let i = 0; i < this.file_name_list.length; i++) {
        form_data.append('heroes', this.file_name_list[i])
        form_data.append('captions', update_text[i])
      }
      axios.post(
        'http://localhost/api/v1/courses/backstage/course-management/add-hero/',
        form_data
      )
      axios.post(
        'http://localhost/api/v1/courses/backstage/course-management/delete-hero/',
        qs.stringify(
          {
            delete_list: this.delete_origin_list
          },
          { arrayFormat: 'repeat' }
        )
      )
      this.image_data_list = []
      this.file_name_list = []
      this.delete_origin_list = []
      this.input_content = ''
      this.$refs.upload_picture.hide()
    },
    delete_origin_img (index) {
      this.delete_origin_list.push(index)
      let i = -1
      for (i = 0; i < this.origin_image_list.length; i++) {
        if (this.origin_image_list[i].hero_id === index) {
          break
        }
      }
      this.origin_image_list.splice(i, 1)
    },
    hide_modal () {
      this.$refs.upload_picture.hide()
    },
    init_error_message (message) {
      switch (message) {
        case 'Access denied.':
          return '用户无权限，拒绝访问'
        case 'Object not found.':
          return '查询的对象不存在'
        default:
          return '数据库查询出错'
      }
    }
  }
}
</script>

<style scoped>
.my-content {
  padding: 20px;
  margin: 70px 20px 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

.my-btn-group {
  display: inline-block;
}

h1,
h6 {
  color: #204269;
}

.my-row {
  display: flex;
  flex-wrap: nowrap;
  min-height: 100px;
  overflow: hidden;
  overflow-x: auto;
}

.my-col {
  padding: 0;
}

#intro {
  width: 96%;
  margin-left: 15px;
}

h5 {
  margin-top: 20px;
  margin-bottom: 10px;
}

h1 {
  text-align: left;
}

h6 {
  margin-bottom: 0;
  font-weight: bold;
}

.btn {
  margin-left: 3px;
  border: 1px solid #d3d9df;
}

.buttons {
  padding: 10px;
  white-space: nowrap;
}

#head-add-btn {
  color: white;
  text-align: right;
  background-color: #4db14d;
}

#head-add-btn:hover,
#head-add-btn:active {
  background-color: #449c44;
}

#add-icon,
#change-icon {
  margin-top: 3px;
}

#upload-btn,
#cancel-btn,
#head-change-btn {
  color: white;
  background-color: #337ab7;
}

#upload-btn:hover,
#cancel-btn:hover,
#head-change-btn:hover {
  background-color: #286090;
}

.my-input {
  display: inline-block;
  max-width: 200px;
}

.table-div {
  padding: 0 15px;
  margin-bottom: 25px;
  overflow-x: auto;
}

#detail-button {
  color: #5b9bd1;
}

#detail-button:hover {
  background-color: rgba(91, 155, 209, 0.2);
}

#change-button {
  color: green;
}

#change-button:hover {
  background-color: rgba(0, 128, 0, 0.2);
}

thead tr {
  font-weight: bold;
  color: #999;
}

.table td {
  vertical-align: middle;
}

table {
  border-top: 1px solid #d3d9df;
}

.input-image {
  display: none;
}

.img-uploader {
  position: relative;
  width: auto;
  min-width: 260px;
  max-width: 800px;
  height: calc(150px + 25px * 2);
  margin-right: 15px;
  margin-left: 15px;
  background: #ebebeb;
  border-radius: 5px;
}

.img-uploader-placeholder {
  position: absolute;
  top: 50%;
  width: 100%;
  margin: 0;
  font-size: 15px;
  color: #aaa;
  text-align: center;
  transform: translate(0%, -50%);
}

.img-uploader-preview-list {
  width: 100%;
  height: calc(150px + 18px * 2);
  overflow: hidden;
  overflow-x: auto;
  text-align: center;
  white-space: nowrap;
  -webkit-backface-visibility: hidden;
  -webkit-overflow-scrolling: touch;
}

.img-uploader-preview {
  z-index: 2;
  display: inline-block;
  min-height: 150px;
  margin: 10px;
  background: #333;
  border-radius: 10px;
  transition: 0.3s cubic-bezier(0.3, 0, 0.2, 1);
}

.img-uploader-mask {
  position: absolute;
  bottom: 0;
  display: none;
  width: 150px;
  text-align: center;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 1px;
}

.img-uploader-preview:hover {
  transform: scale(1.02);
}

.img-uploader-preview:hover .img-uploader-mask {
  display: block;
}

.img-uploader-delete-btn {
  position: absolute;
  top: 0;
  right: 0;
  display: none;
  width: 25px;
  height: 25px;
  margin: 5px;
}

.img-uploader-preview:hover .img-uploader-delete-btn {
  display: block;
}

.img-uploader-preview .preview-img {
  width: 150px;
  height: 150px;
  overflow: hidden;
}

.img-uploader-label {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100%;
  margin-bottom: 0;
  cursor: pointer;
}

.img-uploader-file-name {
  display: inline-block;
  max-width: 90%;
  padding-top: 10px;
  margin: 0;
  overflow: hidden;
  font-size: 5px;
  color: white;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
}

.head-title {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  margin: 25px 0;
}

.head-container {
  padding: 0 15px;
  margin-bottom: 15px;
  text-align: left;
}
</style>
