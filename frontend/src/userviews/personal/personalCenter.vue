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
                :disabled="disabled"
                :state="nameState"
                aria-describedby="inputLiveHelp"/>
              <b-input-group-append>
                <b-btn
                  id="change"
                  variant="outline-success"
                  @click="editable">{{ status }}</b-btn>
              </b-input-group-append>
              <b-form-invalid-feedback id="inputLiveFeedback">
                用户名已存在
              </b-form-invalid-feedback>
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
              prepend="奖励金"
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
          <b-row>
            <b-button
              :disabled="del_disabled"
              size="lg"
              variant="danger"
              @click="Delete">
              删除账号
            </b-button>
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
import axios from 'axios'
import qs from 'qs'

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
      items: [
        {
          text: '个人中心',
          href: '/personal'
        }
      ],
      nameState: true,
      thumbnail: require('../../assets/logo.png'),
      file: null,
      value: this.$store.state.user.username,
      disabled: true,
      status: '修改',
      phone: this.$store.state.phone,
      money: this.$store.state.money,
      time: this.$store.state.time,
      del_disabled: false
    }
  },
  watch: {
    value (n) {
      this.status = '保存'
      this.nameState = true
    }
  },
  mounted () {
    axios
      .get(
        'http://localhost:8000/api/v1/customers/forestage/personal-center/get-reward-coin/'
      )
      .then(res => {
        this.$store.commit('money', (this.money = res.data.reward_coin))
      })
    axios
      .get(
        'http://localhost:8000/api/v1/customers/forestage/auth/get-generate-time/'
      )
      .then(res => {
        function unix (value) {
          function add0 (m) {
            return m < 10 ? '0' + m : m
          }
          let time = new Date(parseInt(value) * 1000)
          let y = time.getFullYear()
          let m = time.getMonth() + 1
          let d = time.getDate()
          let h = time.getHours()
          let s = time.getSeconds()
          return (
            y + '.' + add0(m) + '.' + add0(d) + ' ' + add0(h) + ':' + add0(s)
          )
        }
        this.$store.commit('time', (this.time = unix(res.data.generate_time)))
      })
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
      let that = this
      if (this.status === '修改') {
        this.disabled = !this.disabled
      } else {
        axios
          .post(
            'http://localhost:8000/api/v1/customers/forestage/personal-center/change-username/',
            qs.stringify({ username: this.value }),
            { withCredentials: true }
          )
          .then(res => {
            this.status = '修改'
            this.disabled = !this.disabled
            // console.log(res.data.new_username)
            this.$store.commit('user', {
              is_new_customer: this.$store.state.user.is_new_customer,
              customer_id: this.$store.state.user.customer_id,
              username: this.value,
              avatar: this.$store.state.user.avatar
            })
          })
          .catch(() => {
            // console.log('error: ' + error.message)
            that.nameState = false
          })
      }
    },
    Delete () {
      let that = this
      axios
        .post(
          'http://localhost:8000/api/v1/customers/forestage/personal-center/delete-customer/'
        )
        .then(res => {
          if (res.data.message === 'Object deleted.') {
            this.del_disabled = true
            that.$store.commit('logout')
            that.$router.push({ path: '/' })
          }
        })
    }
  }
}
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
  -ms-filter: 'alpha(opacity=0)';
  opacity: 0;
}

.uneditable {
  text-align: right;
}

.input-group-text {
  justify-content: center;
  width: 100px;
  background-color: white;
}

.money .input-group-text {
  background-color: #ffeaa4;
}

.input-group-append .input-group-text {
  width: auto;
}
</style>
