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
          <b-btn variant="outline-success">获取验证码</b-btn>
        </b-input-group-append>
      </b-input-group>
      <br>
      <b-button
        id="btn"
        href="/#/personal"
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
  }
}
</script>

<style scoped>
  .container {
    border: 1px solid #ccc;
    -webkit-box-shadow: 0px 3px 30px rgba(0, 0, 0, 0.1) inset;
    -webkit-border-bottom-right-radius: 6px 50px;
    border-radius: 10px;
    display: block;
    width: 350px;
    margin: 100px auto;
  }
  img {
    width: 80%;
    height: 80%;
  }
  #btn {
    margin-bottom: 10px;
  }
</style>