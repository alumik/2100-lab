<template>
  <div>
    <UserNavbar/>
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
            variant="outline-success"
            @click="send">{{ status }}{{ seconds !== 61 ? seconds : '' }}</b-btn>
        </b-input-group-append>
      </b-input-group>
      <br>
      <b-button
        id="btn"
        href="/personal"
        type="submit"
        variant="success">登录</b-button>
    </div>
  </div>
</template>

<script>
import UserNavbar from '../components/navbar'
export default {
  name: 'Login',
  components: {
    UserNavbar
  },
  data () {
    return {
      status: '获取验证码',
      seconds: 61
    }
  },
  methods: {
    send () {
      this.status = '再次发送'
      let that = this
      let t = setInterval(function () {
        that.seconds = that.seconds - 1
        if (that.seconds === 0) {
          clearInterval(t)
        }
      }, 1000)
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
