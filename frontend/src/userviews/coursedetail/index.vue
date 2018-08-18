<template>
  <body
    class="width-style">
    <UserNavbar/>
    <div class="content-style">
      <h5>{{ course.name }}</h5>
    </div>
    <div>
      <b-modal
        id="share-popup"
        hide-footer
        title="分享二维码">
        <p
          v-if="course.value!=0"
          class="my-4">&emsp; &emsp;分享该课程的二维码，如果小伙伴点击
          你分享的链接购买课程，你就将获得奖励金哦！</p>
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
          style="border:none; width: 100%;">
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
          :src="course.src"
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
            v-if="course.value!=0 && is_paid === false"
            class="row row-style">
            <h6>现价 ￥{{ course.value-user_balance }}  ￥</h6>
            <h6 class="origin-value">{{ course.value }}</h6>
          </div>
          <div
            class="row time-style">
            <h6>课程时效 {{ course.validate_time }} h</h6>
          </div>
          <div
            class="row time-style">
            <h6>距离失效还有 {{ course.time_to_end }} h</h6>
          </div>
        </div>
        <div class="row btn-row-style">
          <div>
            <div v-show="course.value === 0 || is_paid === true">
              <b-button
                v-b-modal.study-popup
                size="lg"
                variant="primary"
                class="my-btn">
                开始学习
              </b-button>
            </div>
            <div v-show="course.value !== 0 && is_paid === false">
              <b-button
                v-b-modal.pay-popup
                size="lg"
                variant="primary"
                class="my-btn">
                立即购买
              </b-button>
              <div/>
            </div>
          </div>
          <div
            id="sharebutton">
            <b-button
              v-b-modal.share-popup
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
            size="lg"
            variant="primary"
            class="my-btn"
            @click="course.num_of_praise+=1">
            {{ course.num_of_praise }} 赞
          </b-button>
        </div>
      </div>
    </div>
    <div
      id="course-introduction"
      class="profile-style">
      <h5>课程简介</h5>
      <p>&emsp; &emsp;{{ course.introduction }}</p>
    </div>
  </body>
</template>

<script>
import UserNavbar from '../components/navbar'

export default{
  name: 'CourseDetail',
  components: {
    UserNavbar
  },
  data () {
    return {
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
        name: '小孔成像',
        value: 100,
        num_of_praise: 100,
        introduction: '近几年来，父亲和我都是东奔西走，家中光景是一日不如一日。' +
          '他少年出外谋生，独力支持，做了许多大事。哪知老境却如此颓唐！他触目伤怀' +
          '，自然情不能自已。情郁于中，自然要发之于外；家庭琐屑便往往触他之怒。' +
          '他待我渐渐不同往日。但最近两年不见，他终于忘却我的不好，只是惦记着我，' +
          '惦记着他的儿子。我北来后，他写了一信给我，信中说道：“我身体平安，' +
          '惟膀子疼痛厉害，举箸14提笔，诸多不便，大约大去之期15不远矣。”我读到此处，' +
          '在晶莹的泪光中，又看见那肥胖的、青布棉袍黑布马褂的背影。唉！' +
          '我不知何时再能与他相见！',
        src: 'https://picsum.photos/1024/480/?image=54',
        validate_time: 25,
        time_to_end: 24
      }
    }
  },
  computed: {
    reminder: function () {
      return '  该课程将于初次点开' + this.course.validate_time + '小时后不可再观看'
    }
  },
  created () {
    if (typeof (this.$route.params.course_id) === 'undefined') {
      this.$router.push({name: 'BurnedCourse'})
    } else {
      this.course_id = this.$route.params.course_id
    }
  },
  methods: {
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
      this.$router.push({name: 'StudyPage', params: {course_id: id}})
    }
  }
}
</script>

<style>
  .profile-style {
    height: 300px;
    margin: 50px;
    opacity: 0.9;
  }

  #course-introduction .profile-style {
    height: 250px;
  }

  .modal-style {
    margin-top: 20px;
    text-align: right;
  }

  .width-style {
    width: 100%;
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
    margin-left: 130px;
  }

  .btn-row-style {
    display: flex;
    flex-direction: row;
    width: 100%;
    padding: 3px;
    margin-top: 30px;
  }
</style>
