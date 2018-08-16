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
        {id: 0, text: '查看学习记录', isActive: false},
        {id: 1, text: '查看订单记录', isActive: false}
      ]
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
    height: calc(100% - 70px);
  }
  b-container {
    max-height: 100px;
  }
  .info {
    margin-top: 40px;
    margin-left: 40px;
   }
  .row {
    align-items: flex-end;
    padding: 10px 0;
    border-bottom: 2px solid #dec1e3;
  }
  .mt-3 {
    position: relative;
    left: -114px;
    max-width: 114px;
    min-height: 47px;
    opacity: 0;
    -ms-filter: 'alpha(opacity=0)';
  }
  .custom-file-input:lang(en)~.custom-file-label::after {
    content: "789";
  }
</style>
