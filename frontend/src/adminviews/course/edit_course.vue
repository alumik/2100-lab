<template>
  <Basic :items="items">
    <div class="my-content">
      <h2>修改课程</h2>
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
        <label
          class="form-check-label my-label"
          for="course_content">课程素材</label>
        <UploadSourceForEdit
          id="course_content"
          :origin_image_list="course.origin_image_file_list"
          :origin_audio_list="course.origin_audio_file_list"
          @uploadResource="receive_uploaded_resource"/>
        <PreSortPicture
          :is_uploaded="is_uploaded"
          :choose_image_data_list_origin="image_file_list"
          @update_is_uploaded="is_uploaded=false"
          @uploadSortedPic="receive_sorted_pictures"/>
        <SyncPicture
          :audio_file_list="audio_file_list"
          :image_data_list="image_file_list"
          :is_audio_changed="is_audio_changed"
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
      <div class="form-group form-inline">
        <label
          class="form-check-label my-label"
          for="can_review">可评论</label>
        <div
          id="can_review">
          <label for="Yes"><input
            id="Yes"
            ref="Yes"
            type="radio"
            name="optn"
            @click="update_can_comment(1)"
          >是</label>
          <label for="No"><input
            id="No"
            ref="No"
            type="radio"
            name="optn"
            @click="update_can_comment(0)"
          >否</label>
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
      <div class="form-group">
        <label
          id="intro-label"
          class="form-check-label my-label"
          for="intro">简介</label>
        <textarea
          id="intro"
          v-model="course.description"
          class="form-control col-lg-2"
          rows="6s">&nbsp;</textarea>
      </div>
      <button
        class="btn my-btn"
        @click="upload_all_data">保存</button>
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
export default {
  name: 'EditCourse',
  components: {SyncPicture, PreSortPicture, UploadSourceForEdit, Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '课程管理',
        href: '/admin/course'
      }, {
        text: this.$route.query.course_id.toString(),
        href: '/admin/course/detail?course_id=' + this.$route.query.course_id.toString()
      }, {
        text: '修改课程',
        active: true
      }],
      course_id: 0,
      course: {
        'title': '',
        'codename': '',
        'expire_duration_day': '',
        'expire_duration_hour': '',
        'price': '',
        'reward_percent': '',
        'description': '',
        'can_comment': '',
        'origin_audio_file_list': [],
        'origin_image_file_list': []
      },
      audio_file_list: [],
      image_file_list: [],
      delete_origin_image_index_list: [],
      is_uploaded: true,
      is_audio_changed: false
    }
  },
  created () {
    this.course_id = this.$route.query.course_id
    axios.get('http://localhost:8000/api/v1/courses/backstage/course-management/get-course-assets/',
      {
        params: {
          'course_id': this.course_id
        }
      }
    ).then(
      response => {
        this.initial_data(response.data)
      }
    )
  },
  methods: {
    initial_data (data) {
      this.course.title = data.title
      this.course.codename = data.codename
      this.course.expire_duration = data.expire_duration
      this.course.price = data.price
      this.course.reward_percent = data.reward_percent * 100
      this.course.description = data.description
      this.course.can_comment = data.can_comment
      let duration = data.expire_duration
      this.course.expire_duration_day = Math.floor(duration / (3600 * 24))
      let day = this.course.expire_duration_day
      this.course.expire_duration_hour = Math.floor((duration - day * 24 * 3600) / 3600)
      this.course.origin_audio_file_list[0] = data.audio
      this.course.origin_image_file_list = data.images
      if (this.course.can_comment === true) {
        this.$refs.Yes.checked = true
      } else if (this.course.can_comment === false) {
        this.$refs.No.checked = true
      }
      if (this.course.origin_image_file_list.length > 0) {
        for (let i = 0; i < this.course.origin_image_file_list.length; i++) {
          let addPath = this.$store.state.address
          let originPath = this.course.origin_image_file_list[i].image_path
          this.course.origin_image_file_list[i].image_path = addPath + originPath
          this.image_file_list.push({
            'origin_index': this.course.origin_image_file_list[i].image_id,
            'image': this.course.origin_image_file_list[i].image_path,
            'index': i + 1,
            'time': ''
          })
        }
      }
      if (this.course.origin_audio_file_list.length > 0) {
        this.course.origin_audio_file_list[0] = this.$store.state.address + this.course.origin_audio_file_list[0]
        this.audio_file_list.push(this.course.origin_audio_file_list[0])
      }
    },
    update_can_comment: function (data) {
      this.course.can_comment = data
    },
    receive_uploaded_resource: function (uploadPicResourse, audioFileList, originDeleteImageIndex) {
      this.is_uploaded = true
      this.image_file_list.length = 0
      if (audioFileList && audioFileList.length === 1 && audioFileList[0]) {
        this.is_audio_changed = true
        this.audio_file_list = audioFileList
        this.course.origin_audio_file_list[0] = audioFileList[0].name
      }
      for (let i = 1; i <= uploadPicResourse.length; i++) {
        this.image_file_list.push(uploadPicResourse[i - 1])
      }
      for (let i = 0; i < originDeleteImageIndex.length; i++) {
        this.delete_origin_image_index_list.push(originDeleteImageIndex[i])
      }
      let nowLength = this.image_file_list.length
      for (let i = 1; i <= originDeleteImageIndex.length; i++) {
        for (let ii = 0; ii < this.course.origin_image_file_list.length; ii++) {
          if (this.course.origin_image_file_list[ii].image_id === originDeleteImageIndex[i - 1]) {
            this.course.origin_image_file_list.splice(ii, 1)
            break
          }
        }
      }
      for (let i = 1; i <= this.course.origin_image_file_list.length; i++) {
        this.image_file_list.push({
          'origin_index': this.course.origin_image_file_list[i - 1].image_id,
          'image': this.course.origin_image_file_list[i - 1].image_path,
          'index': i + nowLength,
          'time': ''
        })
      }
    },
    receive_sorted_pictures: function (sortImageDataList) {
      this.image_file_list.length = 0
      for (let i = 0; i < sortImageDataList.length; i++) {
        this.image_file_list.push(sortImageDataList[i])
      }
    },
    receive_sync_data: function (imageDataList) {
    },
    upload_all_data: function () {
      let formdata = new FormData()
      formdata.append('course_id', this.course_id)
      formdata.append('title', this.course.title)
      formdata.append('codename', this.course.codename)
      formdata.append('days', this.course.expire_duration_day)
      formdata.append('hours', this.course.expire_duration_hour)
      formdata.append('price', this.course.price)
      formdata.append('can_comment', this.course.can_comment)
      formdata.append('reward_percent', this.course.reward_percent * 0.01)
      formdata.append('description', this.course.description)
      if (this.is_audio_changed === true) {
        formdata.append('audio', this.audio_file_list[0])
      }
      for (let i = 0; i < this.image_file_list.length; i++) {
        let obj = this.image_file_list[i]
        if (obj.image.slice(0, 4) === 'http' && obj.time !== '') {
          formdata.append('image_ids', obj.origin_index)
          formdata.append('load_times_ids', obj.time)
        } else if (obj.image.slice(0, 4) === 'data' && obj.time !== '') {
          formdata.append('image_files', obj.file)
          formdata.append('load_times_files', obj.time)
        }
      }
      axios.post('http://localhost:8000/api/v1/courses/backstage/course-management/edit-course/', formdata).then(
        response => {
          console.log(response.data.message)
        }
      ).catch(
        error => {
          console.log(error)
        }
      )
      axios.post('http://localhost:8000/api/v1/courses/backstage/course-management/delete-course-images/',
        qs.stringify({
          'delete_list': this.delete_origin_image_index_list
        }, {arrayFormat: 'repeat'})).then(
        response => {
          console.log(response.data.message)
        }
      ).catch(
        error => {
          console.log(error)
        }
      )
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
