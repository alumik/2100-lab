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
              <b-row class="my-row">
                <div class="my-row">
                  <div
                    v-for="image in originImageList"
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
                      src="../../assets/logo.png"
                      class="img-uploader-delete-btn"
                      @click="deleteOriginImg(image.hero_id)">
                  </div>
                  <div
                    ref="uploader"
                    class="img-uploader"
                    @drop="handleDrop">
                    <p
                      v-if="!hasImages"
                      class="img-uploader-placeholder">{{ placeholder }}</p>
                    <div
                      v-if="hasImages"
                      class="img-uploader-preview-list">
                      <div
                        v-for="(data,index) in imageDataList"
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
                          v-if="hasImages"
                          class="img-uploader-mask">
                          <p
                            class="img-uploader-file-name"
                            @click="openInput()">
                            {{ placeholder }}</p>
                        </div>
                        <img
                          src="../../assets/logo.png"
                          class="img-uploader-delete-btn"
                          @click="deleteImg(index)">
                      </div>
                    </div>
                    <label
                      v-if="!hasImages"
                      for="inputID"
                      class="img-uploader-label"/>
                    <input
                      id="inputID"
                      ref="input"
                      class="input-image col-lg-12"
                      type="file"
                      accept="image/gif,image/jpeg,image/jpg,image/png,image/svg"
                      multiple="multiple"
                      @change="handleFileChange">
                  </div>
                </div>
              </b-row>
              <b-row align-v="start">
                <b-col>
                  <h5 class="text-left">
                    输入文字
                  </h5>
                </b-col>
              </b-row>
              <div>
                <textarea
                  id="intro"
                  v-model="input_content"
                  class="form-control col-lg-12"
                  rows="6s"/>
              </div>
            </b-container>
            <div
              slot="modal-footer"
              class="w-100">
              <b-row class="define-btn">
                <b-col cols="8"/>
                <b-col cols="2">
                  <b-button
                    @click="uploadData">上传</b-button>
                </b-col>
                <b-col cols="2">
                  <b-button
                    @click="hideModal">取消</b-button>
                </b-col>
              </b-row>
            </div>
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
                </div>
              </td>
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
import qs from 'qs'
import Basic from '../basic/basic'
import Pagination from '../../components/pagination'
import resizeImage from './resize'
export default {
  name: 'CourseManagement',
  components: {Pagination, Basic},
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
      page: 1,

      placeholder: '点击上传图片',
      originImageList: [],
      imageDataList: [],
      fileNameList: [],
      deleteOriginList: [],
      input_content: ''
    }
  },
  computed: {
    hasImages () {
      return this.imageDataList.length > 0
    },
    sizeFormatted () {
      let result = 0
      if (this.maxSize < 1024) {
        result = this.maxSize + 'K'
      } else {
        result =
          (this.maxSize / 1024).toFixed(this.maxSize % 1024 > 0 ? 2 : 0) + 'M'
      }
      return result
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
          _course.push({'course_id': data['course_id'],
            'codename': data['codename'],
            'title': data['title'],
            'updated_at': data['updated_at'].substring(0, 10)})
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
        axios.get('http://localhost:8000/api/v1/courses/forestage/main/get-heroes/').then(
          response => {
            this.originImageList = response.data.content
            for (let i = 0; i < this.originImageList.length; i++) {
              this.originImageList[i].image = this.$store.state.address.concat(this.originImageList[i].image)
            }
          }
        )
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
    },
    preventDefaultEvent (eventName) {
      document.addEventListener(
        eventName,
        function (e) {
          e.preventDefault()
        },
        false
      )
    },
    handleFileChange () {
      let input = this.$refs.input
      let files = input.files
      this.preview(files)
    },
    handleDrop (e) {
      let files = e.dataTransfer.files
      this.preview(files)
    },
    openInput () {
      this.$refs.input.click()
    },
    deleteImg (index) {
      this.imageDataList.splice(index, 1)
      this.fileNameList.splice(index, 1)
    },
    preview (files) {
      let _this = this
      if (!files || !window.FileReader) return

      for (let i = 0; i < files.length; i++) {
        let file = files[i]
        let reader = new FileReader()
        reader.onload = function (e) {
          resizeImage(e.target.result, 150, 150, function (result) {
            _this.imageDataList.push(result)
            _this.fileNameList.push(file)
          })
        }
        reader.readAsDataURL(file)
      }
    },
    uploadData () {
      let updateText = this.input_content.split('\n')
      let formdata = new FormData()
      for (let i = 0; i < this.fileNameList.length; i++) {
        formdata.append('heroes', this.fileNameList[i])
        formdata.append('captions', updateText[i])
      }
      axios.post('http://localhost:8000/api/v1/courses/backstage/course-management/add-hero/', formdata)
      axios.post('http://localhost:8000/api/v1/courses/backstage/course-management/delete-hero/',
        qs.stringify({
          delete_list: this.deleteOriginList
        }, {arrayFormat: 'repeat'}))
    },
    deleteOriginImg (index) {
      this.deleteOriginList.push(index)
      let i = -1
      for (i = 0; i < this.originImageList.length; i++) {
        if (this.originImageList[i].hero_id === index) {
          break
        }
      }
      this.originImageList.splice(i, 1)
    },
    hideModal () {
      this.$refs.upload_picture.hide()
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

  .my-row {
    width: 100%;
    padding: 0;
    margin: 0;
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

  .input-image {
    display: none;
  }

  .img-uploader {
    position: relative;
    width: auto;
    min-width: 260px;
    max-width: 800px;
    height: calc(150px + 25px * 2);
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
</style>
