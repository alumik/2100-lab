<template>
  <Basic
    id="studypage"
    class="width-style">
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
              src=""
              type="audio/mpeg">
          </audio>
        </div>
      </div>
      <div role="tablist">
        <b-card>
          <div
            id="introduction"
            class="text-left-style">
            <label class="delete-margin">
              <h5>{{ course.name }}{{ this.$route.query.course_id }}</h5>
              &emsp;&emsp;{{ text_show }}</label>
            <label
              v-if="brandFold === false"
              id="hide-text">{{ text_hide }}</label>
          </div>
          <div
            class="text-right-style"
            @click="changeFoldState">
            <label
              id="watch-all"
              class="look-all">{{ brandFold ? '﹀展开':'︿收起' }}</label>
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
              class="card-text width-style">
              <MessageBoard/>
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
      course_id: 1,
      now_picture: '',
      now_index: 0,
      time_num: 0,
      ctime: null,
      dtime: null,
      brandFold: true,
      text_show: '',
      text_hide: '',
      course: {
        time_list: [0, 10, 20, 30],
        image: [
          'https://picsum.photos/1024/480/?image=58'
        ],
        audio: '',
        introduction: '桃树、杏树、梨树，你不让我，我不让你，都开满了花赶趟儿。' +
          '红的像火，粉的像霞，白的像雪。花里带着甜味儿；闭了眼，树上仿佛已经满是' +
          '桃儿、杏儿、梨儿。花下成千成百的蜜蜂嗡嗡地闹着，大小的蝴蝶飞来飞去。野花' +
          '遍地是：杂样儿，有名字的，没名字的，散在草丛里，像眼睛，像星星，还眨呀眨的。\n' +
          '“吹面不寒杨柳风”，不错的，像母亲的手抚摸着你。风里带来些新翻的泥土的气息，' +
          '混着青草味儿，还有各种花的香，都在微微润湿的空气里酝酿。鸟儿将巢安在繁花嫩叶当中，' +
          '高兴起来了，呼朋引伴地卖弄清脆的喉咙，唱出宛转的曲子，与轻风流水应和着。' +
          '牛背上牧童的短笛，这时候也成天嘹亮地响着。',
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
  created: function () {
    if (typeof (this.$route.query.course_id) === 'undefined') {
      this.$router.push({name: 'BurnedCourse'})
    } else {
      this.course_id = this.$route.query.course_id
    }
    axios.get('http://localhost:8000/api/v1/courses/forestage/play/get-course-assets?course_id=1')
      .then(function (response) {
      }).catch(function (error) {
        alert(error)
      })
  },
  mounted () {
    this.ctime = this.$refs.player.currentTime
    this.time_num = this.course.time_list.length
    this.text_show = this.course.introduction.substring(0, 138)
    this.text_hide = this.course.introduction.substring(138)
    this.addEventListeners()
  },
  methods: {
    changeFoldState () {
      this.brandFold = !this.brandFold
    },
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

  .width-style {
    width: 100%;
  }
</style>
