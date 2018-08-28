<template>
  <Basic>
    <b-alert
      id="created_test_alert"
      :show="created_test"
      variant="danger"
      dismissible
      fade
      @dismissed="created_test = false">
      {{ created_error_msg }}
    </b-alert>
    <b-alert
      id="add_praise_alert"
      :show="add_praise_test"
      variant="danger"
      dismissible
      fade
      @dismissed="add_praise_test = false">
      {{ add_praise_error_msg }}
    </b-alert>
    <div id="modals">
      <div>
        <b-modal
          id="share-popup"
          hide-footer
          title="分享二维码">
          <textarea
            v-if="course.price!=0"
            id="share-popup-textarea"
            :value="share_reminder"
            readonly
            class="my-4 modal-input textarea-style"/>
          <p
            v-else
            class="my-4">
            &emsp; &emsp;分享该课程的二维码，和小伙伴一起学习吧~
          </p>
          <qrcode
            id="share-qrcode"
            :options="{ size: 200 }"
            value="share_qrcode_url"
            class="qrcode-style"/>
          <div class="modal-style">
            <b-btn
              id="share-popup-cancel-button"
              @click="hide_share_popup">
              取消
            </b-btn>
            <b-btn
              id="share-popup-finish-button"
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
                @click="pay_method_chose(1)">支付宝</b-button>
            </b-col>
            <b-col>
              <b-button
                variant="primary"
                @click="pay_method_chose(2)">微信</b-button>
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
            id="time_reminder"
            :value="time_reminder"
            readonly
            class="modal-input">
          <div class="modal-style">
            <b-btn
              id="study-popup-cancel-button"
              @click="hide_study_popup">
              取消</b-btn>
            <b-btn
              id="study-popup-start-button"
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
        id="course-image"
        class="course-img-style">
        <b-img
          :src="$store.state.address+course.thumbnail"
          fluid
          thumbnail
          alt="Responsive image Thumbnail"
          class="img-thumbnail"/>
      </div>
      <div
        id="introduction"
        class="introduction-style">
        <div
          id="page-title"
          class="content-style">
          <h3>
            {{ course.title }}
          </h3>
        </div>
        <div class="price-time">
          <div
            v-if="!course.can_access">
            <h6 v-if="!course.can_access && course.price !== 0">
              <simple-line-icons
                icon="basket-loaded"
                color="#ffd706"
                class="icon"
                size="small"/> 现价 ￥{{ get_now_price() }}  </h6>
            <h6
              v-if="!isNaN($store.state.user.reward_coin) &&
              $store.state.user.reward_coin != 0.00">&emsp;&emsp;￥
              <label
                v-if="!isNaN(course.price)"
                class="origin-value">{{ course.price }}</label>
            </h6>
          </div>
          <div>
            <h6
              v-if="course.expire_duration !==0 &&
              !isNaN(course.expire_duration)">
              <simple-line-icons
                icon="clock"
                color="#ffd706"
                class="icon"
                size="small"/> 课程时效
              {{ change_duration_to_timestamp(course.expire_duration) }}
            </h6>
          </div>
          <div>
            <h6
              v-if="course.expire_time !== null &&
              course.expire_duration !==0">
              距离失效还有 {{ left_time }}</h6>
          </div>
        </div>
        <div class="button-row">
          <b-button
            v-show="course.can_access || (!course.can_access
            && $store.state.status === false && course.price===0)"
            id="study-button"
            size="sm"
            variant="primary"
            class="my-btn"
            @click="start_study">
            开始学习
          </b-button>
          <b-button
            v-show="!course.can_access && course.price !== 0"
            id="pay-button"
            size="sm"
            variant="primary"
            class="my-btn"
            @click="handle_pay_operate">
            立即购买
          </b-button>
          <b-button
            v-b-modal.share-popup
            id="share-button"
            :title="share_instruction"
            size="sm"
            variant="primary"
            class="my-btn share-margin"
          >
            分享
          </b-button>
          <b-button
            id="praise-button"
            :style="{background: praise_color,
                     border: praise_border_color}"
            size="sm"
            class="my-btn"
            @click="add_praise">
            {{ course.up_votes }} 赞
          </b-button>
        </div>
      </div>
    </div>
    <div class="detail">
      <div
        id="detail-introduction"
        class="container">
        <h5>课程简介</h5>
        <p>{{ course.description }}</p>
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

export default {
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
      share_instruction:
        '        小可爱，你可以通过分享该二维码和' +
        '小朋友一起学习有趣的实验哦~ 分享付费课程给好朋友，如果' +
        '他/她购买该课程，你将会获得奖励金哦~奖励金可以用来购买' +
        '其他有趣的实验课程呢，所以赶紧拿起你的手机进行分享吧(*^▽^*)',
      course: {},
      created_test: false,
      created_error_msg: '',
      add_praise_test: false,
      add_praise_error_msg: '',
      praise_color: '#007bff',
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
      if (that.course.expire_duration !== 0) {
        return (
          '  该课程将于初次点开' +
          that.change_duration_to_timestamp(that.course.expire_duration) +
          '后不可再观看'
        )
      } else {
        return '该课程将永久开放'
      }
    },

    share_reminder: function () {
      let that = this
      return (
        '分享该课程的二维码，如果小伙伴点击你分享的链接购买课程,' +
        '\n你就将获得' +
        that.course.price * that.course.reward_percent +
        '奖励金哦！'
      )
    }
  },
  created () {
    let that = this
    that.query_course_id = that.$route.query.course_id
    if (typeof that.$route.query.referer_id !== 'undefined') {
      that.referer_id = that.$route.query.referer_id
        ? that.$route.query.referer_id
        : ''
    }
    axios
      .get(
        'http://localhost/api/v1/courses/forestage/course/' +
        'get-course-detail/',
        {
          params: {
            course_id: that.query_course_id,
            referer_id: that.referer_id
          }
        }
      )
      .then(function (response) {
        that.course = response.data
        that.course.price = parseFloat(response.data.price)
        that.course.reward_percent =
          parseFloat(response.data.reward_percent)
        if (that.course.up_voted === true) {
          that.praise_color = 'green'
          that.praise_border_color = 'green'
        } else {
          that.praise_color = '#007bff'
          that.praise_border_color = '#007bff'
        }
      })
      .catch(function (error) {
        if (error.response.data.message === 'Object not found.') {
          that.$router.push({ name: 'PageNotFound' })
          that.created_test = true
          that.created_error_msg = that.$t('error.object_not_found')
        }
      })
    that.user_status = that.$store.state.status
    that.share_qrcode_url =
      shareQrcodeHost +
      '?course_id=' +
      that.query_course_id +
      '&' +
      'referer_id=' +
      that.$store.state.user.customer_id
  },
  mounted () {
    mygenerator = setInterval(this.generate_left_time, 1000)
  },
  methods: {
    generate_left_time () {
      let due = new Date(this.course.expire_time)
      let now = new Date()
      let substract = Math.floor((due - now) / 1000)
      if (substract <= 0) {
        clearInterval(mygenerator)
      }
      let days = Math.floor(substract / (3600 * 24))
      let hours = Math.floor((substract - days * (3600 * 24)) / 3600)
      let minutes = Math.floor(
        (substract - days * (3600 * 24) - hours * 3600) / 60
      )
      let seconds = substract - days * (3600 * 24) - hours * 3600 - minutes * 60
      if (days >= 0 && hours >= 0 && minutes >= 0 && seconds >= 0) {
        this.left_time =
          days + '天' + hours + '小时' + minutes + '分钟' + seconds + '秒'
      } else {
        this.left_time = '0天0小时0分钟0秒'
      }
    },
    change_duration_to_timestamp (duration) {
      const days = Math.floor(duration / (3600 * 24))
      const hours = Math.floor((duration - days * (3600 * 24)) / 3600)
      if (days > 0 && hours > 0) {
        return days + '天' + hours + '小时'
      } else if (days > 0 && hours === 0) {
        return days + '天'
      } else if (days === 0 && hours > 0) {
        return hours + '小时'
      } else if (days === 0 && hours === 0) {
        return ''
      }
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
      if (that.$store.state.status === false) {
        this.$root.$emit('bv::show::modal', 'log-popup')
      } else {
        axios
          .get(
            'http://localhost/api/v1/courses/forestage/course/up-vote-course/' +
              '?course_id=' +
              that.query_course_id
          )
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
          })
          .catch(function (error) {
            if (error.response.data.message === 'Object not found.') {
              that.add_praise_test = true
              that.add_praise_error_msg = that.$t('error.object_not_found')
            }
          })
      }
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
      that.pay_remind_color = 'black'
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
        axios
          .post(
            'http://localhost/api/v1/courses/forestage/course/' +
            'buy-course/',
            qs.stringify({
              course_id: that.query_course_id,
              payment_method: that.pay_method
            })
          )
          .then(function (response) {
            if (response.data.message === 'Success.') {
              that.course.can_access = true
            }
          })
          .catch(function (error) {
            if (error.response.data.message === 'Object not found.') {
              that.finishPay_test = true
              that.finishPay_error_msg = that.$t('error.object_not_found')
            } else if (
              error.response.data.message ===
              'This course has already been purchased.'
            ) {
              that.finishPay_test = true
              that.finishPay_error_msg = that.$t(
                'error.course_already_purchased'
              )
            }
          })
      }
    },
    open_study_page: function (id) {
      this.$router.push({
        name: 'StudyPage',
        query: { course_id: parseInt(id) }
      })
    },
    open_log: function (id) {
      this.$router.push({
        name: 'Login',
        params: { source: 'coursedetail', course_id: id }
      })
    },
    handle_pay_operate: function () {
      if (this.$store.state.status === true) {
        this.$root.$emit('bv::show::modal', 'pay-popup')
      } else {
        this.$root.$emit('bv::show::modal', 'log-popup')
      }
    },
    start_study: function () {
      if (
        this.course.expire_time !== null &&
        this.course.expire_duration !== 0
      ) {
        let due = new Date(this.course.expire_time)
        let now = new Date()
        let substract = Math.floor((due - now) / 1000)
        if (substract <= 0) {
          this.$router.push({ name: 'BurnedCourse' })
        }
      }
      if (this.$store.state.status === true) {
        this.$root.$emit('bv::show::modal', 'study-popup')
      } else {
        this.$root.$emit('bv::show::modal', 'log-popup')
      }
    },
    get_now_price: function () {
      if (this.$store.state.user.reward_coin > this.course.price) {
        return 0
      } else {
        return this.course.price - this.$store.state.user.reward_coin
      }
    }
  }
}
</script>
