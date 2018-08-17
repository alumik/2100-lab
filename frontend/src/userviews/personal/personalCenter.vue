<template>
  <div id="page">
    <UserNavbar @hide="hide"/>
    <div id="main">
      <UserMenu
        :list="list"
        :hidden="hidden"/>
      <div class="info">
        <BreadCrumb :items="items"/>
        <b-row>
          <b-img
            thumbnail
            fluid
            src="https://picsum.photos/250/250/?image=54"
            alt="Thumbnail" />
          <button
            type="button"
            class="btn btn-warning btn-lg imgbtn">
            修改头像</button>
          <b-form-file
            v-model="file2"
            :class="{'active': active, 'mt-3': true}"
            plain/>
        </b-row>
        <b-row>
          <b-img
            thumbnail
            fluid
            src="https://picsum.photos/250/250/?image=54"
            alt="Thumbnail" />
          <button
            type="button"
            class="btn btn-warning btn-lg imgbtn">
            修改头像</button>
        </b-row>
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
      thumbnail: require('../../assets/404.gif'),
      file: null,
      value: '我们是坠胖的',
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
  margin: 40px 40px;
}
.breadcrumb {
  margin-top: -20px;
  margin-left: -15px;
}
.row {
  align-items: flex-end;
  padding: 10px 0;
  border-bottom: 2px solid #dec1e3;
}
img {
  /*max-width: 500px;*/
  max-height: 300px;
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
.uneditable {
  text-align: right;
}
.input-group-text {
  background-color: #efe4eb;
}
.money .input-group-text {
  background-color: #efe67f;
}
</style>
