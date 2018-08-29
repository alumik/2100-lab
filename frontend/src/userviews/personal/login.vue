<template>
  <Basic>
    <div class="container">
      <b-navbar-brand>
        <img
          id="logoimg"
          src="../../assets/2100logo.png">
      </b-navbar-brand>
      <b-input-group prepend="手机号">
        <b-form-input
          v-model="phone"
          :state="phone_state"
          type="text"/>
        <b-form-invalid-feedback id="inputLiveFeedback">
          手机号码不正确！
        </b-form-invalid-feedback>
      </b-input-group>
      <br>
      <b-input-group
        prepend="验证码"
        @keyup.enter="login">
        <b-form-input
          v-model="code"
          :state="code_state"
          type="text"
          aria-describedby="inputLiveFeedback"/>
        <b-input-group-append>
          <b-btn
            id="send"
            :disabled="code_disabled"
            variant="outline-success"
            @click="send">{{ status }}{{ second }}</b-btn>
        </b-input-group-append>
        <b-form-invalid-feedback id="inputLiveFeedback">
          验证码不正确！
        </b-form-invalid-feedback>
      </b-input-group>
      <br>
      <b-button
        id="btn"
        :disabled="log_disabled"
        type="submit"
        variant="success"
        @click="login"
      >登录
      </b-button>
      <b-modal
        v-model="modal_show"
        :ok-disabled="ok_disabled"
        size="lg"
        title="用户协议"
        centered
        ok-title="我同意"
        cancel-title="我不同意"
        @ok="handleOk"
        @cancel="handleCancel">
        {{ content }}
        <br>
        <b-form-checkbox
          id="checkbox"
          v-model="accept"
          value="accepted">
          我同意该协议
        </b-form-checkbox>
      </b-modal>
    </div>
  </Basic>
</template>

<script>
import Basic from '../components/basic'
import axios from 'axios'
import qs from 'qs'
export default {
  name: 'Login',
  components: {
    Basic
  },
  data () {
    return {
      phone: '',
      code: '',
      correct_code: '',
      status: '获取验证码',
      code_state: true,
      phone_state: true,
      seconds: 61,
      log_disabled: true,
      code_disabled: false,
      new_customer: false,
      ok_disabled: true,
      modal_show: false,
      accept: '',
      content: '',
      course_id: -1
    }
  },
  computed: {
    second () {
      if (this.seconds < 61) {
        return this.seconds + 's'
      }
      return ''
    }
  },
  watch: {
    accept: function (o) {
      if (o === 'accepted') {
        this.ok_disabled = false
      } else {
        this.ok_disabled = true
      }
    },
    phone: function (n) {
      if (n.length > 11) {
        this.phone_state = false
      } else {
        this.phone_state = true
      }
    },
    code: function (n) {
      if (n.length > 6) {
        this.code_state = false
      } else {
        this.code_state = true
      }
    }
  },
  mounted () {
    if (this.$route.params.source === 'coursedetail') {
      this.course_id = this.$route.params.course_id
    } else if (this.$store.state.status) {
      this.$router.push({ path: '/' })
    }
  },
  methods: {
    send () {
      let that = this
      that.code_disabled = true
      axios
        .post(
          'http://localhost/api/v1/customers/forestage/auth/' +
            'get-verification-code/',
          qs.stringify({
            phone_number: this.phone
          }),
          { withCredentials: true }
        )
        .then(response => {
          alert(response.data.verification_code)
          that.new_customer = response.data.is_new_customer
          that.status = '再次发送 '
          this.log_disabled = false
          that.seconds = that.seconds - 1
          let time = setInterval(function () {
            that.seconds = that.seconds - 1
            if (that.seconds === -1) {
              that.code_disabled = false
              that.seconds = 61
              clearInterval(time)
            }
          }, 1000)
        })
        .catch(error => {
          if (error) {
            that.code_disabled = false
            that.phone_state = false
          }
        })
    },
    handleOk (evt) {
      axios
        .post(
          'http://localhost/api/v1/customers/forestage/auth/' +
            'authenticate-customer/',
          qs.stringify({
            phone_number: this.phone.toString(),
            verification_code: this.code.toString()
          }),
          { withCredentials: true }
        )
        .then(response => {
          this.$store.commit('status')
          this.$store.commit('username', response.data.username)
          this.$store.commit('phone', this.phone)
          this.$store.commit('avatar', response.data.avatar)
          if (this.course_id !== -1) {
            this.$router.push({
              path: '/coursedetail',
              query: { course_id: this.course_id }
            })
          }
          this.$router.push({ path: '/' })
        })
        .catch(error => {
          this.modal_show = !this.modal_show
          if (error.response.data.message === 'Different phone number.') {
            this.phone_state = false
          } else if (
            error.response.data.message === 'Wrong verification code.'
          ) {
            this.code_state = false
          } else {
            alert('请刷新重试')
          }
        })
    },
    handleCancel (evt) {
      axios.post('http://localhost/api/v1/core/auth/logout/', {
        withCredentials: true
      })
    },
    login () {
      let that = this
      if (that.new_customer) {
        axios
          .post(
            'http://localhost/api/v1/customers/forestage/auth/' + 'get-eula/'
          )
          .then(res => {
            this.content = res.data.content
          })
        this.modal_show = !this.modal_show
      } else {
        axios
          .post(
            'http://localhost/api/v1/customers/forestage/auth/' +
              'authenticate-customer/',
            qs.stringify({
              phone_number: this.phone.toString(),
              verification_code: this.code.toString()
            }),
            { withCredentials: true }
          )
          .then(response => {
            this.$store.commit('status')
            this.$store.commit('username', response.data.username)
            this.$store.commit('phone', this.phone)
            this.$store.commit('avatar', response.data.avatar)
            if (this.course_id !== -1) {
              this.$router.push({
                path: '/coursedetail',
                query: { course_id: this.course_id }
              })
            }
            this.$router.push({ path: '/' })
          })
          .catch(error => {
            if (error.response.data.message === 'Different phone number.') {
              that.phone_state = false
            } else if (
              error.response.data.message === 'Wrong verification code.'
            ) {
              this.code_state = false
            } else {
              alert('请刷新重试')
            }
          })
      }
    }
  },
  async beforeRouteEnter (to, from, next) {
    let response = await axios.post(
      'http://localhost/api/v1/core/auth/is-authenticated/',
      {
        withCredentials: true
      }
    )
    let status = response.data.is_authenticated
    next(vm => {
      if (status) {
        next('/')
      } else {
        next()
      }
    })
  }
}
</script>

<style scoped>
.navbar-brand {
  margin: 20px auto;
}

#logoimg {
  width: 300px;
  min-height: 100px;
  margin: 20px auto;
}

.container {
  display: block;
  width: 350px;
  margin: 100px auto;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 5px 6px 5px rgba(0, 0, 0, 0.1);
}

img {
  width: 80%;
  height: 80%;
}

#btn {
  margin-bottom: 10px;
}
</style>
