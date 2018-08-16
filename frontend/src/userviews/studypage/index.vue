<template>
  <div
    id="studypage"
    class="width-style">
    <UserNavbar/>
    <div
      id="content"
      class="width-style">
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
            controls
            preload
            class="audio-player">
            <source
              src="./media/background.mp3"
              type="audio/mpeg">
          </audio>
        </div>
      </div>
      <div role="tablist">
        <b-card
          no-body
          class="mb-1">
          <b-card-header
            header-tag="header"
            class="p-1"
            role="tab">
            <b-btn
              v-b-toggle.accordion1
              block
              href="#"
              variant="info">课程简介</b-btn>
          </b-card-header>
          <b-collapse
            id="accordion1"
            visible
            accordion="my-accordion"
            role="tabpanel">
            <b-card-body>
              <p
                class="card-text text-style">
                &emsp; &emsp;{{ course.introduction }}
              </p>
            </b-card-body>
          </b-collapse>
        </b-card>
        <b-card
          no-body
          class="">
          <b-card-header
            header-tag="header"
            class="p-1"
            role="tab">
            <b-btn
              v-b-toggle.accordion2
              block
              href="#"
              variant="info">留言板</b-btn>
          </b-card-header>
          <b-collapse
            id="accordion2"
            accordion="my-accordion"
            role="tabpanel"
            class="width-style">
            <b-card-body>
              <p
                class="card-text width-style">
                <MessageBoard/>
              </p>
            </b-card-body>
          </b-collapse>
        </b-card>
      </div>
    </div>
  </div>
</template>

<script>
import UserNavbar from '../components/navbar'
import MessageBoard from '../components/messageboard'

export default {
  name: 'StudyPage',
  components: {
    UserNavbar,
    MessageBoard
  },
  data () {
    return {
      now_picture: '',
      now_index: 0,
      time_num: 0,
      ctime: null,
      dtime: null,
      course: {
        time_list: [0, 10, 20, 30],
        image: [
          require('../homepage/image/1.jpg'),
          require('../homepage/image/2.jpg'),
          require('../homepage/image/3.jpg'),
          require('../homepage/image/4.jpg')
        ],
        audio: '',
        introduction: '盼望着，盼望着，东风来了，春天的脚步近了。\n' +
            '　　一切都像刚睡醒的样子，欣欣然张开了眼。山朗润起来了，' +
            '水涨起来了，太阳的脸红起来了。\n' +
            '　　小草偷偷地从土地里钻出来，嫩嫩的，绿绿的。园子里，田野里，' +
            '瞧去，一大片一大片满是的。坐着，躺着，打两个滚，踢几脚球，' +
            '赛几趟跑，捉几回迷藏。风轻悄悄的，草软绵绵的。',
        name: '我们是坠胖的'
      }
    }
  },
  watch: {
    ctime: function () {
      if (this.ctime === 0) {
        this.now_index = 0
        this.change_picture()
      } else if (this.ctime >= this.course.time_list[this.time_num - 1]) {
        this.now_index = this.time_num - 1
        this.change_picture()
      } else {
        for (var i = 1; i < this.time_num; i++) {
          var first = this.course.time_list[i - 1]
          var second = this.course.time_list[i]
          if (this.ctime >= first && this.ctime < second) {
            this.now_index = i - 1
            this.change_picture()
          }
        }
      }
    }
  },
  mounted () {
    this.ctime = this.$refs.player.currentTime
    this.time_num = this.course.time_list.length
    this.addEventListeners()
  },
  methods: {
    change_picture: function () {
      this.now_picture = this.course.image[this.now_index]
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
      self.ctime = parseInt(self.$refs.player.currentTime)
    }
  },
  beforeDestroyed () {
    this.removeEventListeners()
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
    background-image: url('./media/background.jpg');
  }

  .image-style {
    width: 100%;
    height: 90%;
    padding: 0;
    text-align: center;
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

  .audio-player {
    width: 99%;
    height: 100%;
  }

  .text-style {
    text-align: left;
  }

  .width-style {
    width: 100%;
  }
</style>
