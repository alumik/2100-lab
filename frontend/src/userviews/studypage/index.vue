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
    <div class="study-background">
      <div
        class="container">
        <div id="content">
          <div
            id="media"
            class="media-style">
            <div class="sub-media">
              <div>
                <div
                  id="image"
                  class="image-style">
                  <b-img
                    src="https://picsum.photos/400/250/?image=410"
                    class="course-image"/>
                <!--<b-img-->
                <!--:src="now_picture"-->
                <!--class="course-image"/>-->
                </div>
                <div class="audio-style">
                  <audio
                    id="audio"
                    ref="player"
                    :src="audio_src"
                    autoplay
                    controls
                    preload
                    type="audio/mpeg"
                    class="audio-player"/>
                </div>
              </div>
            </div>
          </div>
          <div id="introduction">
            <div class="introduction-style">
              <div
                class="delete-margin text-left-style">
                <div style="font-size: 1.7rem;">{{ course.title }}&emsp;
                </div>
                <div
                  v-b-toggle.course-description
                  id="watch-all"
                  @click="changeFoldState">
                  <simple-line-icons
                    v-if="introduction_brandFold === true"
                    icon="arrow-down"
                    size="small"
                    color="#009966"/>
                  <simple-line-icons
                    v-else
                    icon="arrow-up"
                    size="small"
                    color="#FF6600"/>课程简介
                </div>
              </div>
              <div class="vote-style">
                {{ up_votes }}
                <a
                  :style="{color: praise_course_color}"
                  class="heart-size"
                  @click="up_vote_course">&#10084;</a>
              </div>
            </div>
            <b-collapse
              id="course-description"
              class="mt-2">
              <div class="text-align-left">&emsp;&emsp;
                {{ course.description }}</div>
            </b-collapse>
          </div>
          <hr>
          <MessageBoard
            id="message-board"
            :course_id="query_course_id"/>
        </div>
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
      course: {},
      up_votes: 0,
      beforedestroy_test: false,
      beforedestroy_error_msg: '',
      praise_course_color: '#ccc',
      audio_src: '',
      isExpand: '90px'
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
          if (this.audio_current_time >= first && this.audio_current_time <
            second) {
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
    axios.get('http://localhost/api/v1/courses/forestage/play/' +
      'get-course-assets?' +
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
    axios.get('http://localhost/api/v1/courses/forestage/course/' +
      'get-course-detail?' +
      'course_id=' + that.query_course_id)
      .then(function (response) {
        var data = response.data
        that.up_votes = data.up_votes
        if (data.up_voted === true) {
          that.praise_course_color = '#F60'
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
    this.addEventListeners()
  },
  beforeDestroy () {
    let that = this
    axios.get('http://localhost/api/v1/courses/forestage/play/' +
      'save-learning-log/', {params: {
      course_id: that.query_course_id,
      progress: that.audio_current_time
    }}).catch(function (error) {
      if (error.response.data.message === 'Object not found.') {
        that.beforedestroy_test = true
        that.beforedestroy_error_msg = that.$t('error.object_not_found')
      } else if (error.response.data.message === 'Access denied.') {
        that.beforedestroy_message_test = true
        that.beforedestroy_message_error_msg =
          that.$t('error.access_denied')
      }
    })
  },
  methods: {
    up_vote_course () {
      let that = this
      axios.get('http://localhost/api/v1/courses/forestage/course/' +
        'up-vote-course?' +
      'course_id=' + that.query_course_id)
        .then(function (response) {
          if (response.data.up_voted === true) {
            that.up_votes = response.data.up_votes
            that.praise_course_color = '#F60'
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
      that.now_picture =
        that.course.images[this.now_picture_index].image_path
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
.introduction-style {
  display: flex;
  flex-direction: row;
  flex-grow: 2;
  flex-shrink: 2;
  align-items: center;
  margin: 2rem 0;
}

.audio-style {
  height: 2.5rem;
  vertical-align: center;
}

.text-align-left {
  text-align: left;
}

  .study-background {
    min-height: calc(100vh - 170px);
    padding: 0 5rem;
    background-color: #f7f7f7;
  }

.media-style {
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
  height: 50%;
  padding: 1rem 0 0 0;
}

.image-style {
  width: 100%;
  height: 100%;
  padding: 0;
  text-align: center;
}

.course-image {
  width: 100%;
  height: 100%;
}

.sub-media {
  width: 70%;
  height: 90%;
  text-align: center;
}

.delete-margin {
  margin: 0;
  cursor: pointer;
}

.text-left-style {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-right: 1rem;
  text-align: left;
}

.audio-player {
  width: 100%;
  height: 2rem;
  color: #222;
}

.vote-style {
  height: 25px;
  text-align: right;
}

.heart-size {
  font-size: 18px;
  color: #ccc;
  cursor: pointer;
}

.container {
  padding: 0 3rem;
  background-color: #fff;
}

@media (max-width: 500px) {
  .study-background {
    padding: 0;
  }

  .container {
    padding: 0;
    background-color: #fff;
  }
}
</style>
