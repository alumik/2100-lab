<template>
  <Basic>
    <b-alert
      :show="test"
      variant="danger"
      dismissible
      fade
      @dismissed="test = false">
      This alert means that you have connectioned to backend.
    </b-alert>
    <div class="content-style">
      <h5>{{ course.title }}</h5>
    </div>
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
          class="my-4">&emsp; &emsp;分享该课程的二维码，和小伙伴一起学习吧~</p>
        <qrcode
          :options="{ size: 200 }"
          value="share_url"
          class="qrcode-style"/>
        <div class="modal-style">
          <b-btn @click="hide_share_popup">取消</b-btn>
          <b-btn
            variant="primary"
            @click="hide_share_popup">完成分享</b-btn>
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
          value="alipay_url"
          class="qrcode-margin-style"/>
        <qrcode
          :options="{ size: 200 }"
          value="wxpay_url"
          class="qrcode-margin-style"/>
        <b-row>
          <h5 class="alipay-title">支付宝</h5>
          <h5 class="wxpay-title">微信</h5>
        </b-row>
        <div class="modal-style">
          <b-btn @click="hide_pay_popup">取消</b-btn>
          <b-btn
            variant="primary"
            @click="finishPay">完成支付</b-btn>
        </div>
      </b-modal>
    </div>
    <div>
      <b-modal
        id="study-popup"
        hide-footer
        title="注意！">
        <input
          :value="reminder"
          readonly
          class="modal-input">
        <div class="modal-style">
          <b-btn @click="hide_study_popup">取消</b-btn>
          <b-btn
            variant="primary"
            @click="open_study_page(course_id)">我知道了</b-btn>
        </div>
      </b-modal>
    </div>
    <div
      id="profile"
      class="row profile-style">
      <div
        id="image"
        style="height: 100%; width: 50%;">
        <b-img
          :src="course_src"
          fluid
          thumbnail
          alt="Responsive image Thumbnail"
          class="img-thumbnail course-img-style"/>
      </div>
      <div
        id="introduction"
        class="introduction-style">
        <div class="reminder-style">
          <div
            v-if="course.price!=0 && is_paid === false"
            class="row row-style">
            <h6>现价 ￥{{ course.price-user_balance }}  ￥</h6>
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
        <div class="row btn-row-style">
          <div>
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
                size="lg"
                variant="primary"
                class="my-btn">
                立即购买
              </b-button>
              <div/>
            </div>
          </div>
          <div>
            <b-button
              v-b-modal.share-popup
              id="share-button"
              size="lg"
              variant="primary"
              class="my-btn"
              style="margin-right: 5px;"
            >
              分享
            </b-button>
          </div>
          <b-badge
            :title="share_introduction"
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
          <b-button
            id="praise-button"
            size="lg"
            variant="primary"
            class="my-btn"
            @click="add_praise">
            {{ course.up_votes }} 赞
          </b-button>
        </div>
      </div>
    </div>
    <div
      id="course-introduction"
      class="profile-style">
      <h5>课程简介</h5>
      <p>&emsp; &emsp;{{ course.description }}</p>
    </div>
  </Basic>
</template>

<script>
import Basic from '../components/basic'
import axios from 'axios'

export default{
  name: 'CourseDetail',
  components: {
    Basic
  },
  data () {
    return {
      test: false,
      err_msg: '',
      now_time: 0,
      course_src: 'https://picsum.photos/1024/480/?image=54',
      is_paid: false,
      course_id: 0,
      share_url: 'http://www.baidu.com',
      alipay_url: 'http://www.jisuanke.com',
      wxpay_url: 'http://se.jisuanke.com',
      user_balance: 50,
      share_introduction: '        小可爱，你可以通过分享该二维码和' +
        '小朋友一起学习有趣的实验哦~ 分享付费课程给好朋友，如果' +
        '他/她购买该课程，你将会获得奖励金哦~奖励金可以用来购买' +
        '其他有趣的实验课程呢，所以赶紧拿起你的手机进行分享吧(*^▽^*)',
      course: {
        id: 0,
        price: 100,
        title: '小孔成像',
        reward_percent: 0.2,
        up_votes: 100,
        introduction: '',
        src: '',
        expire_duration: 0,
        expire_time: 0
      }
    }
  },
  computed: {
    reminder: function () {
      let that = this
      return '  该课程将于初次点开' + that.course.expire_duration + '小时后不可再观看'
    },
    share_reminder: function () {
      let that = this
      return '分享该课程的二维码，如果小伙伴点击你分享的链接购买课程,\n你就将获得' +
        that.course.price * that.course.reward_percent +
        '奖励金哦！'
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
        console.log(response.data)
        that.course = response.data
      })
  },
  mounted: function () {
  },
  methods: {
    add_praise () {
      axios.get('http://localhost:8000/api/v1/courses/forestage/course/up-vote-course/?course_id=1')
        .then(function (response) {
          // console.log(reponse)
        })
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

<style>
  .profile-style {
    height: 300px;
    margin: 50px;
    text-align: left;
    opacity: 0.9;
  }

  #course-introduction .profile-style {
    height: 250px;
  }

  .modal-style {
    margin-top: 20px;
    text-align: right;
  }

  .content-style {
    margin: 40px 60px;
  }

  .qrcode-margin-style {
    margin-left: 20px;
  }

  .alipay-title {
    margin-left: 100px;
  }

  .wxpay-title {
    margin-left: 180px;
  }

  .my-btn {
    margin-right: 60px;
    font-size: 16px;
  }

  .course-img-style {
    width: 80%;
    height: 100%;
    margin-left: 10px;
  }

  .introduction-style {
    display: flex;
    flex-direction: column;
    width: 50%;
    height: 100%;
    vertical-align: bottom;
  }

  .origin-value {
    text-decoration: line-through;
  }

  .reminder {
    width: 20px;
    height: 20px;
    margin-top: 25px;
    margin-right: 50px;
  }

  .qrcode-style {
    margin-left: 20px;
  }

  .btn-row-style {
    display: flex;
    flex-direction: row;
    width: 100%;
    padding: 3px;
    margin-top: 30px;
  }

  .modal-input {
    width: 100%;
    border: none;
  }
</style>
