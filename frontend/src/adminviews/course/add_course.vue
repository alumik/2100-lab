<template>
  <Basic :items="items">
    <div>
      <div class="my-content">
        <h2>新增课程</h2>
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
          <label
            class="form-check-label my-label"
            for="course_content">课程素材</label>
          <UploadSource
            id="course_content"
            @uploadResource="receive_uploaded_resource"/>
          <PreSortPicture
            :choose_image_data_list_origin="image_file_list.slice()"
            :is_uploaded="is_uploaded"
            @update_is_uploaded="is_uploaded=false"
            @reset_is_uploaded="is_uploaded=true"
            @uploadSortedPic="receive_sorted_pictures"
          />
          <SyncPicture
            :audio_file_list="audio_file_list"
            :image_data_list="image_file_list"
            :is_audio_changed="true"
            @sync_picture_audio="receive_sync_data"
          />
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
        <div class="form-group form-inline">
          <label
            class="form-check-label my-label"
            for="can_review">
            可评论
          </label>
          <div id="can_review">
            <label for="Yes">
              <input
                id="Yes"
                type="radio"
                checked
                name="optn"
                @click="update_can_comment(1)"
              >是
            </label>
            <label for="No">
              <input
                id="No"
                type="radio"
                name="optn"
                @click="update_can_comment(0)"
              >否
            </label>
          </div>
        </div>
        <div class="form-inline">
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
        <button
          class="btn my-btn"
          @click="upload_all_data">保存</button>
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
      can_comment: '',
      reward_percent: '',
      description: '',
      is_uploaded: true
    }
  },
  methods: {
    update_can_comment: function (data) {
      this.can_comment = data
    },
    receive_uploaded_resource: function (uploadPicResourse, audioFileList) {
      this.is_uploaded = true
      if (audioFileList.length === 1) {
        this.audio_file_list[0] = audioFileList[0]
      }
      this.image_file_list = uploadPicResourse
    },
    receive_sorted_pictures (sortedPic) {
      this.image_file_list.length = 0
      for (let i = 1; i <= sortedPic.length; i++) {
        this.image_file_list.push(sortedPic[i - 1])
        this.image_file_list[i - 1].index = i
      }
    },
    receive_sync_data (imageDataList) {
      this.image_file_list = imageDataList
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
  margin: 40px;
  text-align: left;
}

.my-label {
  display: inline-block;
  width: 150px;
  text-align: left;
}

.flare_time {
  display: flex;
}

#flare_time_day {
  width: 80px;
  min-width: 80px;
  max-width: 80px;
}

#flare_time_hour {
  width: 70px;
  min-width: 70px;
  max-width: 70px;
}

.input {
  width: 260px;
  min-width: 260px;
  max-width: 260px;
}

#can_review {
  display: flex;
}

#input-group-flare {
  display: flex;
}

.my-btn,
#intro {
  max-width: 405px;
}

#No {
  margin-left: 100px;
}

#intro-label {
  margin-top: 20px;
  margin-bottom: 20px;
}

#percent {
  width: 210px;
  min-width: 210px;
  max-width: 210px;
}

#price {
  width: 210px;
  min-width: 210px;
  max-width: 210px;
}

.btn {
  color: white;
  background-color: #8d4e91;
  border-color: #8d6592;
  border-radius: 10px;
  outline: none;
  box-shadow: #8d6592 inset;
}

.btn:hover,
.btn:active {
  background-color: #5e0057;
}
</style>
