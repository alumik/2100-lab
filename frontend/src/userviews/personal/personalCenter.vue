<template>
  <div id="page">
    <UserNavbar @hide="hide"/>
    <div id="main">
      <UserMenu
        :list="list"
        :hidden="hidden"/>
      <div class="info">
        <BreadCrumb :items="items"/>
        <div class="content">
          <b-row>
            <b-img
              :src="thumbnail"
              thumbnail
              fluid
              alt="Thumbnail" />
            <button
              type="button"
              class="btn btn-warning btn-lg">
              修改头像
              <b-form-file
                v-model="file"
                :class="{'upload': true}"
                plain
                @change="change"/>
            </button>
          </b-row>
          <b-row>
            <b-input-group
              size="lg"
              prepend="昵称">
              <b-form-input
                v-model="value"
                :disabled="disabled"/>
              <b-input-group-append>
                <b-btn
                  id="change"
                  variant="outline-success"
                  @click="editable">{{ status }}</b-btn>
              </b-input-group-append>
            </b-input-group>
          </b-row>
          <b-row>
            <b-input-group
              size="lg"
              prepend="手机号">
              <b-form-input
                v-model="phone"
                class="uneditable"
                disabled/>
            </b-input-group>
          </b-row>
          <b-row>
            <b-input-group
              class="money"
              size="lg"
              prepend="奖励金余额"
              append="币">
              <b-form-input
                v-model="money"
                class="uneditable"
                disabled/>
            </b-input-group>
          </b-row>
          <b-row >
            <b-input-group
              size="lg"
              prepend="注册时间">
              <b-form-input
                v-model="time"
                class="uneditable"
                disabled/>
            </b-input-group>
          </b-row>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserNavbar from '../components/navbar'
import UserMenu from './menu'
import BreadCrumb from '../../components/breadCrumb'
export default {
  name: 'PersonalCenter',
  components: {
    UserNavbar,
    UserMenu,
    BreadCrumb
  },
  data: function () {
    return {
      hidden: false,
      list: [
        { id: 0, text: '查看学习记录', isActive: false },
        { id: 1, text: '查看订单记录', isActive: false }
      ],
      items: [{
        text: '个人中心',
        href: '/personal'
      }
      ],
      thumbnail: require('../../assets/logo.png'),
      file: null,
      value: this.$store.state.user.username,
      disabled: true,
      status: '修改',
      phone: 18309351612,
      money: 10,
      time: Date()
    }
  },
  methods: {
    hide: function () {
      this.hidden = !this.hidden
    },
    change: function (event) {
      let reader = new FileReader()
      reader.readAsDataURL(event.target.files[0])
      let that = this
      reader.onloadend = function () {
        that.thumbnail = reader.result
      }
    },
    editable: function () {
      if (this.status === '修改') {
        this.status = '保存'
      } else {
        this.status = '修改'
        console.log(this.value)
        this.$store.commit('user', {
          is_new_customer: this.$store.state.user.is_new_customer,
          customer_id: this.$store.state.user.customer_id,
          username: this.value,
          avatar: this.$store.state.user.avatar
        })
      }
      this.disabled = !this.disabled
    }
  }}
</script>

<style scoped>
  #page {
    height: 100%;
  }

  #main {
    display: flex;
    height: 100%;
  }

  .info {
    flex-grow: 1;
  }

  .content {
    max-width: 600px;
    padding: 20px;
    margin-left: 40px;
  }

  .row {
    align-items: flex-end;
    padding: 10px 0;
  }

  img {
    flex-grow: 0;
    max-height: 300px;
  }

  .btn-warning {
    width: 120px;
    height: 50px;
  }

  .upload {
    position: relative;
    right: 17px;
    bottom: 39px;
    width: 120px;
    height: 50px;
    padding: 0;
    margin: 0;
    -ms-filter: "alpha(opacity=0)";
    opacity: 0;
  }

  .uneditable {
    text-align: right;
  }

  .input-group-text {
    background-color: white;
  }

  .money .input-group-text {
    background-color: #ffeaa4;
  }
</style>
