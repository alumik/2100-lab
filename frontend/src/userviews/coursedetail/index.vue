<template>
  <Basic>
    <b-alert
      :show="created_test"
      variant="danger"
      dismissible
      fade
      @dismissed="created_test = false">
      {{ created_error_msg }}
    </b-alert>
    <b-alert
      :show="add_praise_test"
      variant="danger"
      dismissible
      fade
      @dismissed="add_praise_test = false">
      {{ add_praise_error_msg }}
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
          id="log-popup"
          hide-footer
          title="注意！">
          <p>请先登录！</p>
          <div class="modal-style">
            <b-btn @click="hide_log_popup">
              取消
            </b-btn>
            <b-btn
              variant="primary"
              @click="open_log(query_course_id)">
              登录
            </b-btn>
          </div>
        </b-modal>
      </div>
      <div>
        <b-modal
          id="pay-popup"
          hide-footer
          title="购买课程">
          <h5
            v-if="!pay_method_chosen"
            :style="{color: pay_remind_color}"
            class="my-4">请选择支付方式</h5>
          <b-row
            v-if="pay_method_chosen === false"
            class="pay-method-style">
            <b-col>
              <b-button
                variant="primary"
                @click="pay_method_chose(0)">支付宝</b-button>
            </b-col>
            <b-col>
              <b-button
                variant="primary"
                @click="pay_method_chose(1)">微信</b-button>
            </b-col>
          </b-row>
          <div v-if="pay_method_chosen">
            <qrcode
              :options="{ size: 200 }"
              value="pay_qrcode_url"
              class="qrcode-margin-style"/>
            <p>{{ pay_method === 1 ? '支付宝': '微信' }}</p>
          </div>
          <div class="modal-style">
            <b-btn @click="hide_pay_popup">
              取消</b-btn>
            <b-btn
              variant="primary"
              @click="finishPay">
              完成支付
            </b-btn>
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
              @click="open_study_page(course.course_id)">
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
            v-if="!course.can_access"
            class="row row-style">
            <h6>现价 ￥{{ course.price - user_reward_balance }}  ￥</h6>
            <h6 class="origin-value">{{ course.price }}</h6>
          </div>
          <div
            class="row time-style">
            <h6 v-if="course.expire_duration !==0">
              课程时效 {{ change_duration_to_timestamp(course.expire_duration) }}
            </h6>
          </div>
          <div
            class="row time-style">
            <h6 v-if="course.expire_time !== null">距离失效还有 {{ left_time }}</h6>
          </div>
        </div>
        <b-row class="button-row">
          <b-col
            id="study-or-pay"
            cols="4">
            <div v-show="course.can_access">
              <b-button
                id="study-button"
                size="sm"
                variant="primary"
                class="my-btn"
                @click="start_study">
                开始学习
              </b-button>
            </div>
            <div v-show="!course.can_access">
              <b-button
                id="pay-button"
                size="sm"
                variant="primary"
                class="my-btn"
                @click="handle_pay_operate">
                立即购买
              </b-button>
            </div>
          </b-col >
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
              :style="{background: praise_color, border: praise_border_color}"
              size="sm"
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
import qs from 'qs'

const shareQrcodeHost = 'http://localhost:8080/coursedetail'
var mygenerator = null

export default{
  name: 'CourseDetail',
  components: {
    Basic
  },
  data () {
    return {
      user_status: null,
      query_course_id: 0,
      connection_test: false,
      connection_err_msg: 'Server access failed. ',
      course_img_src_example: 'https://picsum.photos/1024/480/?image=54',
      pay_qrcode_url: 'http://www.jisuanke.com',
      user_reward_balance: 50,
      share_instruction: '        小可爱，你可以通过分享该二维码和' +
        '小朋友一起学习有趣的实验哦~ 分享付费课程给好朋友，如果' +
        '他/她购买该课程，你将会获得奖励金哦~奖励金可以用来购买' +
        '其他有趣的实验课程呢，所以赶紧拿起你的手机进行分享吧(*^▽^*)',
      course: { },
      created_test: false,
      created_error_msg: '',
      add_praise_test: false,
      add_praise_error_msg: '',
      praise_color: 'green',
      praise_border_color: 'green',
      pay_method: 0,
      pay_method_chosen: false,
      pay_remind_color: 'black',
      finishPay_test: false,
      finishPay_error_msg: '',
      share_qrcode_url: '',
      referer_id: '',
      left_time: ''
    }
  },
  computed: {
    time_reminder: function () {
      let that = this
      return '  该课程将于初次点开' +
        that.change_duration_to_timestamp(that.course.expire_duration) + '小时后不可再观看'
    },
    share_reminder: function () {
      let that = this
      return '分享该课程的二维码，如果小伙伴点击你分享的链接购买课程,\n你就将获得' +
        that.course.price * that.course.reward_percent +
        '奖励金哦！'
    }
  },
  created () {
    let that = this
    if (typeof (that.$route.query.course_id) === 'undefined') {
      that.$router.push({name: 'BurnedCourse'})
    } else {
      that.query_course_id = that.$route.query.course_id
      if (typeof (that.$route.query.course_id) !== 'undefined') {
        that.referer_id = that.$route.query.referer_id ? that.$route.query.referer_id : ''
      }
    }
    axios.get('http://localhost:8000/api/v1/courses/forestage/course/get-course-detail/' +
      '?course_id=' + that.query_course_id)
      .then(function (response) {
        that.course = response.data
        that.course.price = parseFloat(response.data.price)
      }).catch(function (error) {
        that.created_test = true
        that.created_error_msg = error
      })
    that.user_status = that.$store.state.status
    that.share_qrcode_url = shareQrcodeHost + '?course_id=' +
      that.query_course_id + '&' + 'referer_id=' + that.$store.state.user.customer_id
  },
  mounted () {
    mygenerator = setInterval(this.generate_left_time, 1000)
  },
  methods: {
    generate_left_time () {
      let due = new Date(this.course.expire_time)
      let now = new Date()
      let substract = Math.floor((due - now) / 1000)
      if (substract === 0) {
        clearInterval(mygenerator)
      }
      let days = Math.floor(substract / (3600 * 24))
      let hours = Math.floor((substract - days * (3600 * 24)) / 3600)
      let minutes = Math.floor((substract - days * (3600 * 24) - hours * 3600) / 60)
      let seconds = substract - days * (3600 * 24) - hours * 3600 - minutes * 60
      this.left_time = days + '天' + hours + '小时' + minutes + '分钟' + seconds + '秒'
    },
    change_duration_to_timestamp (duration) {
      const hours = Math.floor(duration / 3600)
      const minutes = Math.floor((duration - hours * 3600) / 60)
      const seconds = duration - hours * 3600 - minutes * 60
      return hours + '小时' + minutes + '分钟' + seconds + '秒'
    },
    pay_method_chose (payMethod) {
      if (payMethod === 1) {
        this.pay_method = 1
        this.pay_qrcode_url = 'www.baidu.com'
      } else if (payMethod === 2) {
        this.pay_method = 2
        this.pay_qrcode_url = 'se.jisuanke.com'
      }
      this.pay_method_chosen = true
    },
    add_praise () {
      let that = this
      axios.get('http://localhost:8000/api/v1/courses/forestage/course/up-vote-course/' +
        '?course_id=' + that.query_course_id)
        .then(function (response) {
          if (response.data.up_voted === true) {
            that.course.up_votes = response.data.up_votes
            that.praise_color = 'green'
            that.praise_border_color = 'green'
          } else if (response.data.up_voted === false) {
            that.course.up_votes = response.data.up_votes
            that.praise_color = '#007bff'
            that.praise_border_color = '#007bff'
          }
        }).catch(function (error) {
          that.add_praise_test = true
          that.add_praise_error_msg = error
        })
    },
    hide_share_popup () {
      this.$root.$emit('bv::hide::modal', 'share-popup')
    },
    hide_pay_popup () {
      let that = this
      if (that.pay_method_chosen === true) {
        that.pay_method_chosen = false
        that.pay_remind_color = 'black'
      } else {
        this.$root.$emit('bv::hide::modal', 'pay-popup')
      }
    },
    hide_log_popup () {
      this.$root.$emit('bv::hide::modal', 'log-popup')
    },
    hide_study_popup () {
      this.$root.$emit('bv::hide::modal', 'study-popup')
    },
    finishPay () {
      let that = this
      if (this.pay_method_chosen === false) {
        this.pay_remind_color = 'red'
      } else {
        this.$root.$emit('bv::hide::modal', 'pay-popup')
        axios.post('http://localhost:8000/api/v1/courses/forestage/course/buy-course/',
          qs.stringify({
            course_id: that.query_course_id,
            payment_method: that.pay_method,
            referer_id: that.referer_id
          })).then(function (response) {
          if (response.data.message === 'Success.') {
            that.course.can_access = true
          } else alert('请先完成支付')
        }).catch(function (error) {
          that.finishPay_test = true
          that.finishPay_error_msg = error
        })
      }
    },
    open_study_page: function (id) {
      this.$router.push({name: 'StudyPage', query: {course_id: id}})
    },
    open_log: function (id) {
      this.$router.push({name: 'Login', params: {source: 'coursedetail', course_id: id}})
    },
    handle_pay_operate: function () {
      if (this.$store.state.status === true) {
        this.$root.$emit('bv::show::modal', 'pay-popup')
      } else {
        this.$root.$emit('bv::show::modal', 'log-popup')
      }
    },
    start_study: function () {
      if (this.$store.state.status === true) {
        this.$root.$emit('bv::show::modal', 'study-popup')
      } else {
        this.$root.$emit('bv::show::modal', 'log-popup')
      }
    }
  }
}
</script>
