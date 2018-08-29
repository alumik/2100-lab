<template>
  <Basic :items="items">
    <div>
      <div class="my-content">
        <h1>修改课程</h1>
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
        <div class="form-group form-inline">
          <label
            class="form-check-label my-label"
            for="coursename">课程名</label>
          <input
            id="coursename"
            v-model="course.title"
            class="input form-control col-lg-3"
            type="text">
        </div>
        <div class="form-group form-inline">
          <label
            class="form-check-label my-label"
            for="courseID">课程代码</label>
          <input
            id="courseID"
            v-model="course.codename"
            class="input form-control col-lg-3"
            type="text">
        </div>
        <div class="form-group form-inline">
          <div>
            <label
              class="form-check-label my-label"
              for="flare_time">阅后即焚时间</label>
          </div>
          <div
            id="flare_time"
            class="flare_time">
            <div>
              <div
                class="input-group">
                <input
                  id="flare_time_day"
                  v-model="course.expire_duration_day"
                  class="input form-control col-lg-1"
                  type="text">
                <div class="input-group-prepend">
                  <span class="input-group-text">天</span>
                </div>
              </div>
            </div>
            <div>
              <div
                id="input-group-flare"
                class="input-group">
                <input
                  id="flare_time_hour"
                  v-model="course.expire_duration_hour"
                  class="input form-control col-lg-1"
                  type="text">
                <div class="input-group-prepend">
                  <span class="input-group-text">小时</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="form-group form-inline">
          <label
            class="form-check-label my-label"
            for="price">金额</label>
          <div>
            <div class="input-group">
              <input
                id="price"
                v-model="course.price"
                class="input form-control col-lg-1"
                type="text">
              <div class="input-group-prepend">
                <span class="input-group-text">元</span>
              </div>
            </div>
          </div>
        </div>
        <div class="form-inline form-group">
          <label
            class="form-check-label my-label"
            for="percent">分销金比例</label>
          <div>
            <div class="input-group">
              <input
                id="percent"
                v-model="course.reward_percent"
                class="input form-control col-lg-3"
                type="text">
              <div class="input-group-prepend">
                <span
                  class="input-group-text">%</span>
              </div>
            </div>
          </div>
        </div>
        <div class="form-group form-inline">
          <label class="form-check-label my-label">
            可评论
          </label>
          <div class="can-comment">
            <b-form-group>
              <b-form-radio-group
                v-model="course.can_comment"
                :options="comment_options"
                name="radioInline"/>
            </b-form-group>
          </div>
        </div>
        <div class="form-group form-inline">
          <label
            class="form-check-label my-label"
            for="course_content">课程素材</label>
          <div class="my-sync-btn">
            <UploadSourceForEdit
              id="course_content"
              :origin_image_list="course.origin_image_file_list"
              :origin_audio_list="course.origin_audio_file_list"
              :origin_thumb_list="course.origin_thumb_file_list"
              @upload_resource="receive_uploaded_resource"/>
            <PreSortPicture
              :is_uploaded="is_uploaded"
              :choose_image_data_list_origin="image_file_list"
              @update_is_uploaded="is_uploaded=false"
              @reset_is_uploaded="is_uploaded=true"
              @upload_sorted_pic="receive_sorted_pictures"/>
            <SyncPicture
              :audio_file_list="audio_file_list"
              :image_data_list="image_file_list"
              :is_audio_changed="is_audio_changed"
              @sync_picture_audio="receive_sync_data"
            />
          </div>
        </div>
        <div class="form-group">
          <label
            id="intro-label"
            class="form-check-label my-label"
            for="intro">简介</label>
          <textarea
            id="intro"
            v-model="course.description"
            class="form-control col-lg-2"
            rows="6s"/>
        </div>
        <a
          id="save-btn"
          class="btn"
          @click="upload_all_data">
          保存
        </a>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import axios from 'axios'
import UploadSourceForEdit from './upload_source_for_edit'
import PreSortPicture from './pre_sort_picture'
import SyncPicture from './synchronization'
import qs from 'qs'
import Alert from '../../components/alert'
export default {
  name: 'EditCourse',
  components: {
    Alert,
    SyncPicture,
    PreSortPicture,
    UploadSourceForEdit,
    Basic
  },
  data: function () {
    return {
      items: [
        {
          text: '主页',
          href: '/admin/main'
        },
        {
          text: '课程管理',
          href: '/admin/course'
        },
        {
          text: this.$route.query.course_id.toString(),
          href:
            '/admin/course/detail?course_id=' +
            this.$route.query.course_id.toString()
        },
        {
          text: '修改课程',
          active: true
        }
      ],
      course_id: 0,
      course: {
        title: '',
        codename: '',
        expire_duration_day: '',
        expire_duration_hour: '',
        price: '',
        reward_percent: '',
        description: '',
        can_comment: '',
        origin_audio_file_list: [],
        origin_image_file_list: [],
        origin_thumb_file_list: []
      },
      comment_options: [{ text: '是', value: '1' }, { text: '否', value: '0' }],
      thumb_file: '',
      audio_file_list: [],
      image_file_list: [],
      delete_origin_image_index_list: [],
      error_message: '',
      wrong_count_down: 0,
      success_count_down: 0,
      is_uploaded: true,
      is_audio_changed: false,
      is_thumb_change: false
    }
  },
  created () {
    this.course_id = this.$route.query.course_id
    axios
      .get(
        'http://localhost/api/v1/courses/backstage/course-management/get-course-assets/',
        {
          params: {
            course_id: this.course_id
          }
        }
      )
      .then(response => {
        this.initial_data(response.data)
      })
      .catch(error => {
        this.wrong_count_down = 0
        this.success_count_down = 0
        this.error_message = this.init_error_message(
          error.response.data.message
        )
        this.wrong_count_down = 5
      })
  },
  methods: {
    initial_data (data) {
      this.course.title = data.title
      this.course.codename = data.codename
      this.course.expire_duration = data.expire_duration
      this.course.price = data.price
      this.course.reward_percent = data.reward_percent * 100
      this.course.description = data.description
      if (data.can_comment === true) {
        this.course.can_comment = 1
      } else {
        this.course.can_comment = 0
      }
      let duration = data.expire_duration
      this.course.expire_duration_day = Math.floor(duration / (3600 * 24))
      let day = this.course.expire_duration_day
      this.course.expire_duration_hour = Math.floor(
        (duration - day * 24 * 3600) / 3600
      )
      this.course.origin_audio_file_list[0] = data.audio
      this.course.origin_image_file_list = data.images
      this.course.origin_thumb_file_list[0] =
        this.$store.state.address + data.thumbnail
      if (this.course.origin_image_file_list.length > 0) {
        for (let i = 0; i < this.course.origin_image_file_list.length; i++) {
          let addPath = this.$store.state.address
          let originPath = this.course.origin_image_file_list[i].image_path
          this.course.origin_image_file_list[i].image_path =
            addPath + originPath
          this.image_file_list.push({
            origin_index: this.course.origin_image_file_list[i].image_id,
            image: this.course.origin_image_file_list[i].image_path,
            index: i + 1,
            time: ''
          })
        }
      }
      if (this.course.origin_audio_file_list.length > 0) {
        this.course.origin_audio_file_list[0] =
          this.$store.state.address + this.course.origin_audio_file_list[0]
        this.audio_file_list.push(this.course.origin_audio_file_list[0])
      }
    },
    receive_uploaded_resource: function (
      upload_pic_resourse,
      audio_file_list,
      origin_delete_image_index,
      upload_thumb_resource,
      is_thumb_change
    ) {
      this.is_uploaded = true
      if (is_thumb_change === true) {
        this.is_thumb_change = true
        this.thumb_file = upload_thumb_resource[0]['file']
        this.course.origin_thumb_file_list[0] = upload_thumb_resource[0]['data']
      }
      this.image_file_list.length = 0
      if (
        audio_file_list &&
        audio_file_list.length === 1 &&
        audio_file_list[0]
      ) {
        this.is_audio_changed = true
        this.audio_file_list = audio_file_list
        this.course.origin_audio_file_list[0] = audio_file_list[0].name
      }
      for (let i = 1; i <= upload_pic_resourse.length; i++) {
        this.image_file_list.push(upload_pic_resourse[i - 1])
      }
      for (let i = 0; i < origin_delete_image_index.length; i++) {
        this.delete_origin_image_index_list.push(origin_delete_image_index[i])
      }
      let nowLength = this.image_file_list.length
      for (let i = 1; i <= origin_delete_image_index.length; i++) {
        for (let ii = 0; ii < this.course.origin_image_file_list.length; ii++) {
          if (
            this.course.origin_image_file_list[ii].image_id ===
            origin_delete_image_index[i - 1]
          ) {
            this.course.origin_image_file_list.splice(ii, 1)
            break
          }
        }
      }
      for (let i = 1; i <= this.course.origin_image_file_list.length; i++) {
        this.image_file_list.push({
          origin_index: this.course.origin_image_file_list[i - 1].image_id,
          image: this.course.origin_image_file_list[i - 1].image_path,
          index: i + nowLength,
          time: ''
        })
      }
    },
    receive_sorted_pictures: function (sort_image_datalist) {
      this.image_file_list.length = 0
      for (let i = 0; i < sort_image_datalist.length; i++) {
        this.image_file_list.push(sort_image_datalist[i])
      }
    },
    receive_sync_data: function (image_datalist) {
      this.image_file_list = image_datalist
    },
    upload_all_data: function () {
      if (this.verify_data() === true) {
        let form_data = this.initial_form_data()
        axios
          .post(
            'http://localhost/api/v1/courses/backstage/course-management/edit-course/',
            form_data
          )
          .then(response => {
            this.wrong_count_down = 0
            this.success_count_down = 0
            this.error_message = '修改课程成功'
            this.success_count_down = 3
            setTimeout(
              this.$router.push({
                name: 'CourseManagement'
              }),
              3000
            )
          })
          .catch(error => {
            this.wrong_count_down = 0
            this.success_count_down = 0
            this.error_message = this.init_error_message(
              error.response.data.message
            )
            this.wrong_count_down = 5
          })
        axios
          .post(
            'http://localhost/api/v1/courses/backstage/course-management/delete-course-images/',
            qs.stringify(
              {
                delete_list: this.delete_origin_image_index_list
              },
              { arrayFormat: 'repeat' }
            )
          )
          .catch(error => {
            this.wrong_count_down = 0
            this.success_count_down = 0
            this.error_message = this.init_error_message(
              error.response.data.message
            )
            this.wrong_count_down = 5
          })
      }
    },
    initial_form_data: function () {
      let form_data = new FormData()
      form_data.append('course_id', this.course_id)
      form_data.append('title', this.course.title)
      form_data.append('codename', this.course.codename)
      form_data.append('days', this.course.expire_duration_day)
      form_data.append('hours', this.course.expire_duration_hour)
      form_data.append('price', this.course.price)
      form_data.append('can_comment', this.course.can_comment)
      form_data.append('reward_percent', this.course.reward_percent * 0.01)
      form_data.append('description', this.course.description)
      if (this.is_audio_changed === true) {
        form_data.append('audio', this.audio_file_list[0])
      }
      if (this.is_thumb_change === true) {
        form_data.append('thumbnail', this.thumb_file)
      }
      for (let i = 0; i < this.image_file_list.length; i++) {
        let obj = this.image_file_list[i]
        if (obj.image.slice(0, 4) === 'http' && obj.time !== '') {
          form_data.append('image_ids', obj.origin_index)
          form_data.append('load_times_ids', obj.time)
        } else if (obj.image.slice(0, 4) === 'data' && obj.time !== '') {
          form_data.append('image_files', obj.file)
          form_data.append('load_times_files', obj.time)
        }
      }
      return form_data
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
    },
    verify_data () {
      if (
        this.course.codename === '' ||
        this.course.title === '' ||
        parseFloat(this.course.price) < 0 ||
        parseFloat(this.course.reward_percent) < 0
      ) {
        this.wrong_count_down = 5
        this.error_message = '用户输入信息有误'
        return false
      }
      return true
    }
  }
}
</script>

<style scoped>
.my-content {
  padding: 20px;
  margin: 70px 20px 20px;
  text-align: left;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  margin: 25px 15px;
  color: #204269;
  text-align: left;
}

.my-label {
  display: inline-block;
  width: 150px;
  margin-left: 25px;
  text-align: left;
}

.form-group {
  margin-top: 40px;
  margin-bottom: 20px;
}

.flare_time {
  display: flex;
}

label {
  font-size: 14px;
  font-weight: bold;
}

#flare_time_day {
  width: 80px;
  min-width: 80px;
  max-width: 80px;
}

#flare_time_hour {
  width: 70px;
  min-width: 80px;
  max-width: 80px;
}

.input {
  width: 260px;
  min-width: 260px;
  max-width: 260px;
}

.can-comment {
  margin-top: -20px;
}

#input-group-flare {
  display: flex;
}

#intro {
  max-width: 550px;
  margin-left: 25px;
}

#intro-label {
  margin-top: 20px;
  margin-bottom: 20px;
}

#percent {
  width: 217px;
  min-width: 217px;
  max-width: 217px;
}

#price {
  width: 217px;
  min-width: 217px;
  max-width: 217px;
}

#save-btn {
  margin-left: 25px;
  color: white;
  text-align: right;
  background-color: #4db14d;
  border: 1px solid #d3d9df;
}

#save-btn:hover,
#save-btn:active {
  background-color: #449c44;
}

.my-sync-btn {
  display: flex;
  margin-right: -5px;
  margin-left: -5px;
}
</style>
