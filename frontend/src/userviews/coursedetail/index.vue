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
      <b-modal
        id="share-popup"
        ref="modal"
        title="分享说明"
        ok-title="我知道了"
        cancel-title="取消"
        centered
        @ok="hide_share_popup"
        @cancel="hide_share_popup">
        <p
          id="share-remind"
          class="my-4">
          {{ share_instruction }}
        </p>
        <p
          v-if="course.price !== 0"
          class="my-4">
          {{ share_reminder }}
        </p>
        <p
          v-else
          class="my-4">
          分享该免费课程，和小伙伴一起徜徉在实验的海洋里吧！
        </p>
      </b-modal>
      <b-modal
        id="log-popup"
        ref="modal"
        title="注意！"
        ok-title="登录"
        cancel-title="取消"
        centered
        @ok="open_log(query_course_id)"
        @cancel="hide_log_popup">
        <p>请先登录！</p>
      </b-modal>
      <b-modal
        id="pay-popup"
        ref="modal"
        title="购买课程"
        ok-title="完成支付"
        cancel-title="取消"
        @cancel="hide_pay_popup"
        @ok="finishPay">
        <p
          v-if="!pay_method_chosen"
          id="pay-select"
          :style="{color: pay_remind_color}"
          class="my-4">请选择支付方式</p>
        <div
          v-if="pay_method_chosen === false"
          class="pay-method-style">
          <img
            class="pay-image"
            src="../../assets/alipay.png"
            @click="pay_method_chose(1)">
          <img
            class="pay-image"
            src="../../assets/weixin.png"
            @click="pay_method_chose(2)">
        </div>
        <div v-if="pay_method_chosen">
          <qrcode
            :options="{ size: 200 }"
            value="pay_qrcode_url"
            class="qrcode-margin-style"/>
        </div>
      </b-modal>
      <b-modal
        id="study-popup"
        ref="modal"
        title="注意!"
        ok-title="我知道了"
        cancel-title="取消"
        @ok="open_study_page(course.course_id)"
        @cancel="hide_study_popup">
        <input
          id="time_reminder"
          :value="time_reminder"
          readonly
          class="modal-input">
      </b-modal>
      <b-modal
        id="using-reward-popup"
        ref="modal"
        title="注意!"
        ok-title="我知道了"
        cancel-title="取消"
        @ok="using_reward_finish_pay"
        @cancel="hide_using_reward_popup">
        <input
          id="using-reward"
          value="确定使用奖励金购买该课程？"
          readonly
          class="modal-input">
      </b-modal>
    </div>
    <div class="container">
      <div id="profile">
        <div
          id="course-image"
          class="course-img-style">
          <b-img
            :src="course.thumbnail ? $store.state.address+course.thumbnail : ''"
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
              <h6
                v-if="!course.can_access &&
                course.price !== 0">
                <simple-line-icons
                  icon="basket-loaded"
                  color="#ffd706"
                  class="icon"
                  size="small"/> 现价 ￥{{ get_now_price() }}  </h6>
              <h6 v-else>
                <simple-line-icons
                  icon="basket-loaded"
                  color="#ffd706"
                  class="icon"
                  size="small"/>该课程为免费课程。
              </h6>
              <h6
                v-if="!isNaN($store.state.user.reward_coin) &&
                $store.state.user.reward_coin != 0.00">￥
                <label
                  v-if="!isNaN(course.price)"
                  class="origin-value">{{ course.price }}</label>
              </h6>
            </div>
            <div>
              <h6
                v-if="course.expire_duration !==0 &&
                  !isNaN(course.expire_duration) &&
                  $store.state.user.is_vip === false &&
                $store.state.user.is_staff === false">
                <simple-line-icons
                  icon="clock"
                  color="#ffd706"
                  class="icon"
                  size="small"/> 课程时效
                {{ change_duration_to_timestamp(course.expire_duration) }}
              </h6>
              <h6
                v-else-if="$store.state.user.is_vip !== true
                && $store.state.user.is_staff === false">
                <simple-line-icons
                  icon="clock"
                  color="#ffd706"
                  class="icon"
                  size="small"/>
                该课程为永久课程。
              </h6>
            </div>
            <div>
              <h6
                v-if="course.expire_time !== null &&
                  course.expire_duration !==0 &&
                  $store.state.user.is_vip === false &&
                $store.state.user.is_staff === false">
                距离失效还有 {{ left_time }}</h6>
            </div>
          </div>
          <SocialShare
            :url="share_qrcode_url"
            class="share"
          />
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
              size="sm"
              variant="primary"
              class="my-btn share-margin"
            >
              分享说明
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
    </div>
    <div class="detail">
      <div
        id="detail-introduction"
        class="container wrap-style">
        <h5>课程简介</h5>
        <p>{{ course.description }}</p>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../components/basic'
import axios from 'axios'
import qs from 'qs'
import SocialShare from '../components/social_share'

const shareQrcodeHost = 'http://localhost:8080/coursedetail'
var mygenerator = null

export default {
  name: 'CourseDetail',
  components: {
    Basic,
    SocialShare
  },
  /**
   * @return {
   * user_status: Boolean, 用户状态[登录/未登录]
   * query_course_id: Boolean, 查询该课程详情使用的课程id
   * pay_qrcode_url: String, 二维码支付链接
   * share_instruction: String, 分享机制说明
   * course: Object, 显示课程详情的课程对象
   * created_test: Boolean, 后端获取数据判断
   * created_error_msg: String, 后端读取课程详情失败返回的错误信息
   * add_praise_test: Boolean, 点赞操作与后端连接判断
   * add_praise_error_msg: String, 后端进行点赞操作失败返回的错误信息
   * praise_color: String, 课程点赞心形字符颜色
   * praise_border_color: String, 课程点赞心形字符边框
   * pay_method: Number, 用户支付方式选择：0，奖励金，1，支付宝，2，微信
   * pay_method_chosen: Boolean, 是否已选择支付方式
   * pay_remind_color: String, 支付提醒字体颜色
   * finishPay_test: Boolean, 支付测试
   * finishPay_error_msg: String, 支付失败返回错误信息
   * share_qrcode_url: String, 分享二维码链接
   * referer_id: String, 分享用户ID
   * left_time: String， 用户观看课程剩余时间
   * can_paid_using_reward: Boolean，是否可以使用奖励金支付
   } */
  data () {
    return {
      user_status: null,
      query_course_id: 0,
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
      left_time: '',
      can_paid_using_reward: false
    }
  },
  computed: {
    /**
     * 时间提醒
     * 如果课程有效时间不为0 则返回课程时效
     * 如果课程有效时间为0，则返回提示该课程为“永久开放” */
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
    /**
     * 分享提醒
     * 返回奖励金提醒 */
    share_reminder: function () {
      let that = this
      return (
        '    分享该课程，如果小伙伴点击你分享的课程并购买,' +
        '\n你就将获得' +
        that.course.price * that.course.reward_percent +
        '奖励金哦！'
      )
    }
  },
  /**
   * 获取课程详情数据
   * 首先通过route query获取用户查询的课程id
   * 并获取分享链接用户id
   * 若有分享用户，则将id传给后端
   * 若没有分享用户，则将空值传给后端
   * 向后端发送课程ID和分享用户ID
   * 获取课程详情后同时渲染响应点赞状态
   * 课程查询失败将返回失败原因
   * 获取分享用户ID生成分享二维码的链接 */
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
        that.course.reward_percent = parseFloat(response.data.reward_percent)
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
  /**
   * 设定计时器
   * 绑定函数和时间间隔 */
  mounted () {
    mygenerator = setInterval(this.generate_left_time, 1000)
  },
  methods: {
    /**
     * 计算剩余时间
     * 获取阅后即焚时间
     * 返回距离截止时间的时间差
     * 将时间转为“天/时/分/秒”
     * 当时间差为0，则停止计时
     * 将返回“0天0时0分0秒” */
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
    /**
     * 将时间间隔转为时刻 */
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
    /**
     * 支付方式选择
     * 如果支付方式为1，则返回支付宝支付二维码
     * 如果支付方式为2，则返回微信支付二维码 */
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
    /**
     * 给课程点赞
     * 如果用户还未登录，则跳转到登录窗口
     * 如果用户已登录，则向后端发送点赞请求
     * 如果点赞成功，课程点赞数加一，点赞状态变为已点赞
     * 如果二次点赞，课程点赞数减一，点赞状态变为未点赞
     * 如果点赞失败，返回点赞失败信息 */
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
    /**
     * 关闭分享弹窗 */
    hide_share_popup () {
      this.$root.$emit('bv::hide::modal', 'share-popup')
    },
    /**
     * 关闭使用奖励金弹窗 */
    hide_using_reward_popup () {
      this.$root.$emit('bv::hide::modal', 'using-reward-popup')
    },
    /**
     * 关闭支付弹窗
     * 如果支付方式已选择，则恢复到为选择的状态，提示字体恢复为黑色
     * 如果支付方式未选择，关闭支付窗口 */
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
    /**
     * 完成支付
     * 支付方式如果未选择
     * 支付提醒字体为红色
     * 支付方式如果已选择
     * 则关闭支付窗口
     * 并向后端发送支付请求，传送课程ID和支付方式
     * 如支付成功，则支付状态变为已支付
     * 如支付失败，则返回失败信息 */
    finishPay () {
      let that = this
      if (this.pay_method_chosen === false) {
        this.pay_remind_color = 'red'
      } else {
        this.$root.$emit('bv::hide::modal', 'pay-popup')
        axios
          .post(
            'http://localhost/api/v1/courses/forestage/course/' + 'buy-course/',
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
    /**
     * 使用奖励金支付
     * 向后端传送课程id及支付方式0
     * 如发送成功，课程状态为可以观看
     * 如发送失败，返回失败信息 */
    using_reward_finish_pay () {
      let that = this
      axios
        .post(
          'http://localhost/api/v1/courses/forestage/course/' + 'buy-course/',
          qs.stringify({
            course_id: that.query_course_id,
            payment_method: 0
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
            that.finishPay_error_msg = that.$t('error.course_already_purchased')
          }
        })
    },
    /**
     * 打开学习页面
     * 页面跳转至学习页面，并传送课程id */
    open_study_page: function (id) {
      this.$router.push({
        name: 'StudyPage',
        query: { course_id: parseInt(id) }
      })
    },
    /**
     * 打开登录页面
     * 跳转至登录页面
     * 传送登录来源为课程详情页
     * 传送课程ID，方便登录后的跳转 */
    open_log: function (id) {
      this.$router.push({
        name: 'Login',
        params: { source: 'coursedetail', course_id: id }
      })
    },
    /**
     * 处理支付操作
     * 如果使用奖励金支付，则弹出奖励金支付窗口
     * 如果奖励金不足，弹出普通支付窗口
     * 如果未登录，弹出登录提示窗口 */
    handle_pay_operate: function () {
      if (this.can_paid_using_reward === true) {
        this.$root.$emit('bv::show::modal', 'using-reward-popup')
      } else if (this.$store.state.status === true) {
        this.$root.$emit('bv::show::modal', 'pay-popup')
      } else {
        this.$root.$emit('bv::show::modal', 'log-popup')
      }
    },
    /**
     * 开始学习
     * 如果课程时效不为空且不为0
     *    如果已焚毁，跳转至已焚毁页面
     *    如果未焚毁，判断用户是否已登录
     *       如果已登录，则跳转至课程学习页面
     *       如果未登录，则弹出登录提示框 */
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
    /**
     * 显示课程现价
     * 如果用户奖励金金额大于课程原价
     * 则奖励金支付方式优先
     * 如果用户奖励金金额不足课程原价
     * 则返回课程原价和用户奖励金的差价 */
    get_now_price: function () {
      if (this.$store.state.user.reward_coin > this.course.price) {
        this.can_paid_using_reward = true
        return 0
      } else {
        return this.course.price - this.$store.state.user.reward_coin
      }
    }
  }
}
</script>

<style scoped>
#profile {
  display: flex;
  align-items: stretch;
  justify-content: center;
  padding: 20px 0;
  margin: 50px;
}

.origin-value {
  text-decoration: line-through;
}

#course-image,
#introduction {
  width: 28%;
  height: 250px;
  margin: 0 50px;
}

#course-image {
  overflow: hidden;
  vertical-align: middle;
}

p,
h6 {
  text-indent: 2rem;
}

.img-thumbnail {
  width: 400px;
  height: 250px;
}

.share {
  margin-left: 1rem;
}

.wrap-style {
  word-break: normal;
  word-wrap: break-word;
}

h3,
h5,
p {
  text-align: left;
}

h3 {
  font-weight: bold;
}

#introduction {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  text-align: left;
}

.price-time {
  padding: 10px 20px;
}

h6 {
  margin: 3px 0;
}

.button-row {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.my-btn {
  width: 80px;
  height: 40px;
  margin-right: 20px;
  font-size: 16px;
}

.pay-method-style {
  display: flex;
  justify-content: center;
  height: 100px;
}

.modal-input {
  width: 100%;
  border: none;
}

.textarea-style {
  height: 60px;
  resize: none;
  outline: none;
}

.detail {
  height: calc(100% - 360px);
  padding: 5% 0;
  background-color: #eee;
}

#detail-introduction {
  width: 58%;
  padding: 20px 50px;
  background-color: white;
}

h5,
p {
  margin-bottom: 10px;
}

#pay-select {
  font-size: 20px;
  text-align: center;
}

.pay-image {
  width: 100px;
  height: 100px;
  margin: 0 10px;
  cursor: pointer;
}

@media (max-width: 950px) {
  #profile {
    display: block;
    padding: 10px 0;
    margin: 2px;
  }

  #course-image,
  #introduction {
    width: 80%;
    height: 250px;
    padding: 5px;
  }

  #introduction {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
    text-align: center;
  }

  .detail {
    margin: 0;
  }

  #detail-introduction {
    width: 75%;
    padding: 20px;
  }

  .button-row {
    justify-content: center;
  }

  .my-btn {
    margin: 0 5px;
  }
}
</style>
