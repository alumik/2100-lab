<template>
  <Basic :items="items">
    <div>
      <div class="my-content">
        <h1>新增课程</h1>
        <div class="form-group form-inline">
          <label
            class="form-check-label my-label"
            for="coursename">课程名</label>
          <input
            id="coursename"
            v-model="title"
            class="input form-control col-lg-3"
            type="text">
        </div>
        <div class="form-group form-inline">
          <label
            class="form-check-label my-label"
            for="courseID">课程代码</label>
          <input
            id="courseID"
            v-model="codename"
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
                  v-model="days"
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
                  v-model="hours"
                  class="input form-control col-lg-1"
                  type="text">
                <div class="input-group-prepend">
                  <span class="input-group-text">
                    小时
                  </span>
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
                v-model="prices"
                class="input form-control col-lg-1"
                type="text">
              <div class="input-group-prepend">
                <span class="input-group-text">
                  元
                </span>
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
                v-model="reward_percent"
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
                v-model="can_comment"
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
            <UploadSource
              id="course_content"
              @upload_resource="receive_uploaded_resource"/>
            <PreSortPicture
              :choose_image_data_list_origin="image_file_list.slice()"
              :is_uploaded="is_uploaded"
              @update_is_uploaded="is_uploaded=false"
              @reset_is_uploaded="is_uploaded=true"
              @upload_sorted_pic="receive_sorted_pictures"
            />
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
            v-model="description"
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
import UploadSource from './upload_source'
import PreSortPicture from './pre_sort_picture'
import SyncPicture from './synchronization'
import axios from 'axios'
export default {
  name: 'AddCourse',
  components: { SyncPicture, PreSortPicture, UploadSource, Basic },
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
          text: '新增课程',
          active: true
        }
      ],
      audio_file_list: [],
      image_file_list: [],
      title: '',
      codename: '',
      days: '',
      hours: '',
      prices: '',
      can_comment: '1',
      comment_options: [
        { text: '是', value: '1' },
        { text: '否', value: '0' }
      ],
      reward_percent: '',
      description: '',
      is_audio_changed: false,
      is_uploaded: true
    }
  },
  methods: {
    receive_uploaded_resource: function (upload_pic_resourse, audio_file_list) {
      this.is_uploaded = true
      if (audio_file_list.length === 1) {
        this.audio_file_list[0] = audio_file_list[0]
        this.is_audio_changed = true
      }
      this.image_file_list = upload_pic_resourse
    },
    receive_sorted_pictures (sorted_pic) {
      this.image_file_list.length = 0
      for (let i = 1; i <= sorted_pic.length; i++) {
        this.image_file_list.push(sorted_pic[i - 1])
        this.image_file_list[i - 1].index = i
      }
    },
    receive_sync_data (image_data_list) {
      this.image_file_list = image_data_list
    },
    upload_all_data () {
      let formdata = new FormData()
      for (let i = 0; i < this.image_file_list.length; i++) {
        formdata.append('images', this.image_file_list[i].file)
        formdata.append('load_times', this.image_file_list[i].time)
      }
      formdata.append('audio', this.audio_file_list[0])
      formdata.append('title', this.title)
      formdata.append('codename', this.codename)
      formdata.append('days', this.days)
      formdata.append('hours', this.hours)
      formdata.append('price', this.prices)
      formdata.append('can_comment', this.can_comment)
      formdata.append('reward_percent', this.reward_percent * 0.01)
      formdata.append('description', this.description)
      axios
        .post(
          'http://localhost:8000/api/v1/courses/backstage/course-management/add-course/',
          formdata
        )
        .then(response => {
          console.log(response.data.message)
        })
        .catch(error => {
          console.log(error)
        })
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
