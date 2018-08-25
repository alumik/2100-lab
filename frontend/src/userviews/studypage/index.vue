<template>
  <Basic>
    <b-alert
      :show="assets_test"
      variant="danger"
      dismissible
      fade
      @dismissed="assets_test=false">
      {{ assets_error_msg }}
    </b-alert>
    <b-alert
      :show="detail_test"
      variant="danger"
      dismissible
      fade
      @dismissed="detail_test=false">
      {{ detail_error_msg }}
    </b-alert>
    <b-alert
      :show="beforedestroy_test"
      variant="danger"
      dismissible
      fade
      @dismissed="beforedestroy_error_msg=false">
      {{ beforedestroy_error_msg }}
    </b-alert>
    <div
      id="content">
      <div
        id="media"
        class="media-style">
        <div
          id="image"
          class="image-style">
          <b-img
            :src="now_picture"
            class="course-image"/>
        </div>
        <div
          id="audio"
          class="audio-style">
          <audio
            ref="player"
            :src="audio_src"
            autoplay
            controls
            preload
            type="audio/mpeg"
            class="audio-player"/>
        </div>
      </div>
      <div role="tablist">
        <b-card>
          <div
            id="introduction">
            <b-row>
              <b-col class="delete-margin text-left-style">
                <h5>
                  {{ course.title }}
                </h5>
              </b-col>
              <b-col class="vote-style">
                {{ up_votes }}
                <a
                  :style="{color: praise_course_color}"
                  class="heart-size"
                  @click="up_vote_course">&#10084;</a>
              </b-col>
            </b-row>
            <div class="delete-margin text-left-style">
              &emsp;&emsp;{{ introduction_text_show }}
            </div>
            <label
              v-if="introduction_brandFold === false"
              id="hide-text">{{ introduction_text_hide }}
            </label>
            <div
              class="text-right-style"
              @click="changeFoldState">
              <label
                id="watch-all"
                class="look-all">{{ introduction_brandFold ? '﹀展开':'︿收起' }}</label>
            </div>
          </div>
        </b-card>
        <b-card
          no-body>
          <b-card-header
            header-tag="header"
            class="p-1"
            role="tab">
            留言板
          </b-card-header>
          <b-card-body>
            <p
              id="message-board"
              class="card-text">
              <MessageBoard :course_id="query_course_id"/>
            </p>
          </b-card-body>
        </b-card>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../components/basic'
import MessageBoard from '../components/messageboard'
import axios from 'axios'

export default {
  name: 'StudyPage',
  components: {
    Basic,
    MessageBoard
  },
  data () {
    return {
      query_course_id: 0,
      assets_test: false,
      assets_error_msg: '',
      detail_test: false,
      detail_error_msg: '',
      up_vote_test: false,
      up_vote_error_msg: '',
      now_picture: '',
      now_picture_index: 0,
      audio_current_time: 0,
      audio_duration: null,
      audio_piece_num: 0,
      introduction_brandFold: true,
      introduction_text_show: '',
      introduction_text_hide: '',
      course: {},
      up_votes: 0,
      beforedestroy_test: false,
      beforedestroy_error_msg: '',
      praise_course_color: '#ccc',
      audio_src: ''
    }
  },
  watch: {
    audio_current_time: function () {
      if (this.audio_current_time === 0) {
        this.now_picture_index = 0
        this.change_picture()
      } else if (this.audio_current_time >=
        this.course.images[this.audio_piece_num - 1].load_time) {
        this.now_picture_index = this.audio_piece_num - 1
        this.change_picture()
      } else {
        for (var i = 1; i < this.audio_piece_num; i++) {
          var first = this.course.images[i - 1].load_time
          var second = this.course.images[i].load_time
          if (this.audio_current_time >= first && this.audio_current_time < second) {
            this.now_picture_index = i - 1
            this.change_picture()
          }
        }
      }
    }
  },
  created: function () {
    let that = this
    that.query_course_id = parseInt(that.$route.query.course_id)
    axios.get('http://localhost:8000/api/v1/courses/forestage/play/get-course-assets?' +
      'course_id=' + that.query_course_id)
      .then(function (response) {
        that.course = response.data
        that.audio_src = that.$store.state.address + that.course.audio
        that.audio_piece_num = that.course.images.length
        for (var i = 0; i < that.course.images.length; i++) {
          that.course.images[i].image_path = that.$store.state.address +
              that.course.images[i].image_path
        }
        that.$refs.player.currentTime = that.course.progress
      }).catch(function (error) {
        if (error.response.data.message === 'Object not found.') {
          that.$router.push({name: 'PageNotFound'})
          that.assets_test = true
          that.assets_error_msg = that.$t('error.object_not_found')
        } else if (error.response.data.message === 'Access denied.') {
          that.assets_test = true
          that.assets_error_msg = that.$t('error.access_denied')
        }
      })
    axios.get('http://localhost:8000/api/v1/courses/forestage/course/get-course-detail?' +
      'course_id=' + that.query_course_id)
      .then(function (response) {
        var data = response.data
        that.up_votes = data.up_votes
        if (data.up_voted === true) {
          that.praise_course_color = '#f00'
        } else if (data.up_voted === false) {
          that.praise_course_color = '#ccc'
        }
      }).catch(function (error) {
        if (error.response.data.message === 'Object not found.') {
          that.detail_test = true
          that.detail_error_msg = that.$t('error.object_not_found')
        }
      })
  },
  mounted () {
    this.audio_current_time = this.$refs.player.currentTime
    this.introduction_text_show = this.course.description ? this.course.description.substring(0, 2) : ''
    this.introduction_text_hide = this.course.description ? this.course.description.substring(2) : ''
    this.addEventListeners()
  },
  beforeDestroy () {
    let that = this
    axios.get('http://localhost:8000/api/v1/courses/forestage/play/save-learning-log/', {params: {
      course_id: that.query_course_id,
      progress: that.audio_current_time
    }}).catch(function (error) {
      if (error.response.data.message === 'Object not found.') {
        that.beforedestroy_test = true
        that.beforedestroy_error_msg = that.$t('error.object_not_found')
      } else if (error.response.data.message === 'Access denied.') {
        that.beforedestroy_message_test = true
        that.beforedestroy_message_error_msg = that.$t('error.access_denied')
      }
    })
  },
  methods: {
    up_vote_course () {
      let that = this
      axios.get('http://localhost:8000/api/v1/courses/forestage/course/up-vote-course?' +
      'course_id=' + that.query_course_id)
        .then(function (response) {
          if (response.data.up_voted === true) {
            that.up_votes = response.data.up_votes
            that.praise_course_color = '#f00'
          } else if (response.data.up_voted === false) {
            that.up_votes = response.data.up_votes
            that.praise_course_color = '#ccc'
          }
        }).catch(function (error) {
          if (error.response.data.message === 'Object not found.') {
            that.up_vote_test = true
            that.up_vote_error_msg = that.$t('error.object_not_found')
          }
        })
    },
    changeFoldState () {
      this.introduction_brandFold = !this.introduction_brandFold
    },
    change_picture: function () {
      let that = this
      that.now_picture = that.course.images[this.now_picture_index].image_path
        ? that.course.images[that.now_picture_index].image_path : ''
    },
    addEventListeners: function () {
      const self = this
      self.$refs.player.addEventListener('timeupdate', self._currentTime)
    },
    removeEventListeners: function () {
      const self = this
      self.$refs.player.removeEventListener('timeupdate', self._currentTime)
    },
    _currentTime: function () {
      const self = this
      self.audio_current_time = parseInt(self.$refs.player.currentTime)
    }
  }
}
</script>

<style>
  .media-style {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 100%;
    height: 80%;
    height: 500px;
    background-image: url('https://picsum.photos/1024/480/?image=58');
  }

  .image-style {
    width: 100%;
    height: 90%;
    padding: 0;
    text-align: center;
  }

  .delete-margin {
    margin: 0;
  }

  .look-all {
    color: #686868;
  }

  .look-all:hover {
    color: #000;
  }

  .course-image {
    width: 60%;
    height: 100%;
  }

  .audio-style {
    width: 100%;
    height: 30px;
    margin-top: 10px;
    text-align: center;
  }

  .text-left-style {
    text-align: left;
  }

  .text-right-style {
    text-align: right;
  }

  .audio-player {
    width: 99%;
    height: 100%;
  }

  .vote-style {
    height: 25px;
    text-align: right;
  }

  .heart-size {
    font-size: 15px;
    color: #ccc;
    cursor: pointer;
  }
</style>
