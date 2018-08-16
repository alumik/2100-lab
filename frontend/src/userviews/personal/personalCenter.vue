<template>
  <div id="page">
    <UserNavbar @hide="hide"/>
    <div id="main">
      <UserMenu
        :list="list"
        :hidden="hidden"/>
      <div class="info">
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
                variant="outline-success"
                @click="editable">{{ status }}</b-btn>
            </b-input-group-append>
          </b-input-group>
        </b-row>
      </div>
    </div>
  </div>
</template>

<script>
import UserNavbar from '../components/navbar'
import UserMenu from './menu'
export default {
  name: 'PersonalCenter',
  components: {
    UserNavbar,
    UserMenu
  },
  data: function () {
    return {
      hidden: false,
      list: [
        { id: 0, text: '查看学习记录', isActive: false },
        { id: 1, text: '查看订单记录', isActive: false }
      ],
      thumbnail: require('../../assets/404.gif'),
      file: null,
      value: '我们是坠胖的',
      disabled: true,
      status: '修改'
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
      }
      this.disabled = !this.disabled
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
  height: calc(100% - 70px);
}
b-container {
  max-height: 100px;
}
.info {
  margin: 40px 40px;
}
.row {
  align-items: flex-end;
  padding: 10px 0;
  border-bottom: 2px solid #dec1e3;
}
img {
  width: 500px;
  flex-grow: 0;
}
.btn-warning {
  height: 50px;
  width: 120px;
}
.upload {
  position: relative;
  right: 17px;
  bottom: 39px;
  margin: 0;
  padding: 0;
  width: 120px;
  height: 50px;
  opacity: 0;
  -ms-filter: "alpha(opacity=0)";
}
.input-group {

}
</style>
