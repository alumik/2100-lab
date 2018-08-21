<template>
  <Basic>
    <b-alert
      :show="connection_test"
      variant="danger"
      dismissible
      fade
      @dismissed="connection_test = false">
      This alert means that you have connectioned to backend.
    </b-alert>
    <div
      id="page-title"
      class="content-style">
      <h5>
        {{ course.title }}
      </h5>
    </div>
    <div id="modals">
      <div>
        <b-modal
          id="share-popup"
          hide-footer
          title="分享二维码">
          <textarea
            v-if="course.price!=0"
            :value="share_reminder"
            readonly
            class="my-4 modal-input"/>
          <p
            v-else
            class="my-4">
            &emsp; &emsp;分享该课程的二维码，和小伙伴一起学习吧~
          </p>
          <qrcode
            :options="{ size: 200 }"
            value="share_qrcode_url"
            class="qrcode-style"/>
          <div class="modal-style">
            <b-btn @click="hide_share_popup">
              取消
            </b-btn>
            <b-btn
              variant="primary"
              @click="hide_share_popup">
              完成分享
            </b-btn>
          </div>
        </b-modal>
      </div>
      <div>
        <b-modal
          id="pay-popup"
          hide-footer
          title="购买课程">
          <h5 class="my-4">请选择支付方式</h5>
          <qrcode
            :options="{ size: 200 }"
            value="alipay_qrcode_url"
            class="qrcode-margin-style"/>
          <qrcode
            :options="{ size: 200 }"
            value="wxpay_qrcode_url"
            class="qrcode-margin-style"/>
          <b-row>
            <h5 class="alipay-title">支付宝</h5>
            <h5 class="wxpay-title">微信</h5>
          </b-row>
          <div class="modal-style">
            <b-btn @click="hide_pay_popup">
              取消</b-btn>
            <b-btn
              variant="primary"
              @click="finishPay">
              完成支付</b-btn>
          </div>
        </b-modal>
      </div>
      <div>
        <b-modal
          id="study-popup"
          hide-footer
          title="注意!">
          <input
            :value="time_reminder"
            readonly
            class="modal-input">
          <div class="modal-style">
            <b-btn @click="hide_study_popup">
              取消</b-btn>
            <b-btn
              variant="primary"
              @click="open_study_page(course.id)">
              我知道了</b-btn>
          </div>
        </b-modal>
      </div>
    </div>
    <div
      id="profile"
      class="row profile-style">
      <div
        id="image"
        class="course-img-style">
        <b-img
          :src="course_img_src_example"
          fluid
          thumbnail
          alt="Responsive image Thumbnail"
          class="img-thumbnail"/>
      </div>
      <div
        id="introduction"
        class="introduction-style">
        <div class="reminder-style">
          <div
            v-if="course.price!=0 && is_paid === false"
            class="row row-style">
            <h6>现价 ￥{{ course.price - user_reward_balance }}  ￥</h6>
            <h6 class="origin-value">{{ course.price }}</h6>
          </div>
          <div
            class="row time-style">
            <h6>课程时效 {{ course.expire_duration }} h</h6>
          </div>
          <div
            class="row time-style">
            <h6>距离失效还有 {{ course.expire_time - now_time }} h</h6>
          </div>
        </div>
        <b-row class="button-row">
          <b-col
            id="study-or-pay"
            cols="4">
            <div v-show="course.price === 0 || is_paid === true">
              <b-button
                v-b-modal.study-popup
                id="study-button"
                size="lg"
                variant="primary"
                class="my-btn">
                开始学习
              </b-button>
            </div>
            <div v-show="course.price !== 0 && is_paid === false">
              <b-button
                v-b-modal.pay-popup
                id="pay-button"
                size="sm"
                variant="primary"
                class="my-btn">
                立即购买
              </b-button>
            </div>
          </b-col>
          <b-col cols="4">
            <b-button
              v-b-modal.share-popup
              id="share-button"
              size="sm"
              variant="primary"
              class="my-btn share-margin"
            >
              分享
            </b-button>
            <b-badge
              :title="share_instruction"
              pill
              variant="primary"
              class="reminder"
              data-container="body"
              data-toggle="popover"
              data-content="share_introduction"
              data-placement="top"
            >
              <label>!</label>
            </b-badge>
          </b-col>
          <b-col cols="4">
            <b-button
              id="praise-button"
              size="sm"
              variant="primary"
              class="my-btn"
              @click="add_praise">
              {{ course.up_votes }} 赞
            </b-button>
          </b-col>
        </b-row>
      </div>
      <div
        id="course-introduction"
        class="profile-style">
        <h5>课程简介</h5>
        <p>&emsp; &emsp;{{ course.description }}</p>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../components/basic'
import axios from 'axios'
import './style.css'

export default{
  name: 'CourseDetail',
  components: {
    Basic
  },
  data () {
    return {
      connection_test: false,
      connection_err_msg: 'Server access failed. ',
      course_img_src_example: 'https://picsum.photos/1024/480/?image=54',
      is_paid: false,
      share_qrcode_url: 'http://www.baidu.com',
      alipay_qrcode_url: 'http://www.jisuanke.com',
      wxpay_qrcode_url: 'http://se.jisuanke.com',
      user_reward_balance: 50,
      share_instruction: '        小可爱，你可以通过分享该二维码和' +
        '小朋友一起学习有趣的实验哦~ 分享付费课程给好朋友，如果' +
        '他/她购买该课程，你将会获得奖励金哦~奖励金可以用来购买' +
        '其他有趣的实验课程呢，所以赶紧拿起你的手机进行分享吧(*^▽^*)',
      course: {
        id: 0,
        thumbnail: '',
        title: '小猪佩奇',
        description: '',
        price: 100,
        reward_percent: 0,
        up_votes: 0,
        expire_duration: 0,
        expire_time: 0,
        can_access: false
      }
    }
  },
  computed: {
    time_reminder: function () {
      let that = this
      return '  该课程将于初次点开' + that.course.expire_duration + '小时后不可再观看'
    },
    share_reminder: function () {
      let that = this
      return '分享该课程的二维码，如果小伙伴点击你分享的链接购买课程,\n你就将获得' +
        that.course.price * that.course.reward_percent +
        '奖励金哦！'
    },
    now_time: function () {
      return new Date()
    }
  },
  created () {
    if (typeof (this.$route.query.course_id) === 'undefined') {
      this.$router.push({name: 'BurnedCourse'})
    } else {
      this.course_id = this.$route.query.course_id
    }
    let that = this
    axios.get('http://localhost:8000/api/v1/courses/forestage/course/get-course-detail?course_id=1')
      .then(function (response) {
        that.course = response.data
      })
  },
  mounted: function () {
  },
  methods: {
    add_praise () {
      axios.get('http://localhost:8000/api/v1/courses/forestage/course/up-vote-course/?course_id=1')
    },
    hide_share_popup () {
      this.$root.$emit('bv::hide::modal', 'share-popup')
    },
    hide_pay_popup () {
      this.$root.$emit('bv::hide::modal', 'pay-popup')
    },
    hide_study_popup () {
      this.$root.$emit('bv::hide::modal', 'study-popup')
    },
    finishPay () {
      this.$root.$emit('bv::hide::modal', 'pay-popup')
      this.is_paid = true
    },
    open_study_page: function (id) {
      this.$router.push({name: 'StudyPage', query: {course_id: id}})
    }
  }
}
</script>
