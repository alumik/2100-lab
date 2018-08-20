<template>
  <Basic>
    <div class="container">
      <img src="../../assets/logo.png">
      <h2>2100实验室</h2>
      <br>
      <b-input-group prepend="手机号">
        <b-form-input type="text"/>
      </b-input-group>
      <br>
      <b-input-group prepend="验证码">
        <b-form-input type="text"/>
        <b-input-group-append>
          <b-btn
            id="send"
            :disabled="disabled"
            variant="outline-success"
            @click="send">{{ status }}{{ second }}</b-btn>
        </b-input-group-append>
      </b-input-group>
      <br>
      <b-button
        id="btn"
        type="submit"
        variant="success"
        @click="login">登录</b-button>
      <b-modal
        v-model="modalShow"
        size="lg"
        title="用户协议"
        centered
        ok-title="我同意"
        cancel-title="返回"
        @ok="handleOk">
        北京陌陌科技有限公司（以下简称“陌陌科技”）在此特别提醒您（用户）在注册成为用户之前，请认真阅读本《用户协议》（以下简称“协议”），确保您充分理解本协议中各条款。
        请您审慎阅读并选择接受或不接受本协议。除非您接受本协议所有条款，否则您无权注册、登录或使用本协议所涉服务。 您的注册、登录、使用等行为将视为对本协议的接受，并同意接受本协议各项条款的约束。
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
export default {
  name: 'Login',
  components: {
    Basic
  },
  data () {
    return {
      status: '获取验证码',
      seconds: 61,
      disabled: false,
      modalShow: false,
      accept: ''
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
  methods: {
    send () {
      this.status = '再次发送 '
      let that = this
      that.seconds = that.seconds - 1
      this.disabled = true
      let t = setInterval(function () {
        that.seconds = that.seconds - 1
        if (that.seconds === -1) {
          that.disabled = false
          that.seconds = 61
          clearInterval(t)
        }
      }, 1000)
    },
    handleOk (evt) {
      if (this.accept === 'accepted') {
        this.$router.push({path: '/personal'})
      }
      evt.preventDefault()
    },
    login () {
      this.modalShow = !this.modalShow
    }
  }
}
</script>

<style scoped>
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
