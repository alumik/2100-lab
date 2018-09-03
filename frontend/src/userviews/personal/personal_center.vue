<template>
  <div id="page">
    <UserNavbar @hide="hide"/>
    <div id="main">
      <UserMenu
        :list="list"
        :hidden="hidden"/>
      <div class="info">
        <BreadCrumb :items="items"/>
        <Alert
          :count_down="wrong_count_down"
          :instruction="wrong"
          variant="danger"
          @decrease="wrong_count_down-1"
          @zero="wrong_count_down=0"/>
        <Alert
          :count_down="success_count_down"
          :instruction="success"
          variant="success"
          @decrease="success_count_down-1"
          @zero="success_count_down=0"/>
        <div class="content">
          <b-row class="avatar_related">
            <div class="img-height">
              <b-img
                :src="avatar"
                thumbnail
                fluid
                class="userimg"
                alt="Thumbnail"/>
              <b-form-file
                v-model="file"
                :class="{'upload': true}"
                class="avatar-style"
                plain
                title="更换头像"
                accept="image/*"
                @change="change"/>
            </div>
          </b-row>
          <b-row>
            <b-input-group
              size="lg"
              prepend="昵称">
              <b-form-input
                v-model="value"
                :disabled="disabled"
                :state="name_state"
                aria-describedby="inputLiveHelp"/>
              <b-input-group-append>
                <b-btn
                  id="change"
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
          <b-row class="delete">
            <b-button
              v-b-modal.modal
              :disabled="del_disabled">
              删除账号
            </b-button>
            <b-modal
              id="modal"
              centered
              hide-footer
              title="您确认删除自己的账号吗？">
              <b-form-input
                v-model="input_phone"
                type="text"
                placeholder="请输入自己的手机号"/>
              <b-btn
                block
                @click="Delete">确认删除</b-btn>
            </b-modal>
          </b-row>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserNavbar from '../components/navbar'
import UserMenu from './menu'
import BreadCrumb from '../../components/bread_crumb'
import axios from 'axios'
import qs from 'qs'
import Alert from '../../components/alert'

export default {
  name: 'PersonalCenter',
  components: {
    Alert,
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
      name_state: true,
      avatar: '',
      file: '',
      value: this.$store.state.user.username,
      disabled: true,
      status: '修改',
      phone: this.$store.state.user.phone_number,
      money: this.$store.state.user.reward_coin,
      time: this.$store.state.user.date_joined,
      del_disabled: false,
      input_phone: '',
      wrong_count_down: 0,
      wrong: '',
      dismiss_second: 5,
      success_count_down: 0,
      success: ''
    }
  },
  watch: {
    value () {
      this.status = '保存'
      this.name_state = true
    }
  },
  mounted () {
    axios
      .get(
        'http://localhost/api/v1/customers/forestage/personal-center/' +
        'get-customer-detail/'
      )
      .then(res => {
        this.$store.commit('status')
        this.$store.commit('user', res.data)
        this.avatar = this.$store.state.address +
          this.$store.state.user.avatar
        this.value = this.$store.state.user.username
        this.phone = this.$store.state.user.phone_number
        this.money = this.$store.state.user.reward_coin
        this.time = this.$store.state.user.date_joined
          .toString()
          .substring(0, 19)
          .replace('T', ' ')
        this.$store.commit('date_joined', this.time)
      })
      .catch(error => {
        this.wrong = error.response.data.message
        this.wrong_count_down = this.dismiss_second
      })
  },
  methods: {
    /**
     * 进行左侧菜单栏的显示或隐藏
     */
    hide: function () {
      this.hidden = !this.hidden
    },
    /**
     * 进行改变头像的操作
     * @param event {vent} 事件
     */
    change: function (event) {
      let that = this
      let data = new FormData()
      data.set('new_avatar', event.target.files[0])
      axios
        .post(
          'http://localhost/api/v1/customers/forestage/personal-center/' +
          'change-avatar/',
          data
        )
        .then(res => {
          this.$store.commit('avatar', res.data.new_avatar)
          that.avatar = this.$store.state.address + res.data.new_avatar
          this.success = '头像上传成功'
          this.success_count_down = this.dismiss_second
          this.$router.push({ path: '/personal' })
        })
    },
    /**
     * 进行修改昵称的操作
     */
    editable: function () {
      let that = this
      if (this.status === '修改') {
        this.disabled = !this.disabled
      } else {
        axios
          .post(
            'http://localhost/api/v1/customers/forestage/' +
            'personal-center/change-username/',
            qs.stringify({ username: this.value }),
            { withCredentials: true }
          )
          .then(res => {
            this.status = '修改'
            this.disabled = !this.disabled
            this.$store.commit('username', this.value)
          })
          .catch(() => {
            that.name_state = false
          })
      }
    },
    /**
     * 进行删除自己账号的操作
     */
    Delete () {
      let that = this
      if (that.$store.state.user.phone_number === that.input_phone) {
        axios
          .post(
            'http://localhost/api/v1/customers/forestage/' +
            'personal-center/delete-customer/'
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
}
</script>

<style scoped>
.was-validated .form-control:valid,
.form-control.is-valid,
.was-validated .custom-select:valid,
.custom-select.is-valid {
  border-color: #ced4da;
}

.img-height {
  height: 200px;
}

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
  max-width: 500px;
  padding: 20px;
  margin-left: 40px;
  text-align: center;
}

.avatar-style {
  bottom: 180px !important;
  left: 25px !important;
  width: 150px !important;
  height: 150px !important;
}

.row {
  align-items: flex-end;
  padding: 10px 0;
  margin-bottom: 10px;
}

.userimg {
  width: 200px;
  height: 200px;
  margin-right: 20px;
  border-radius: 50%;
}

.avatar_related {
  justify-content: center;
  margin-bottom: 30px;
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
  text-align: left;
}

.input-group-text {
  justify-content: center;
  width: 100px;
  background-color: white;
}

.input-group-append .input-group-text {
  width: auto;
}

[placeholder='请输入自己的手机号'] {
  margin-bottom: 15px;
}

.delete {
  text-align: right;
}

@media (max-width: 500px) {
  .content {
    padding: 20px;
    margin-left: 0;
  }
}
</style>
