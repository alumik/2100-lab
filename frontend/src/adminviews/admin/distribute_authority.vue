<template>
  <Basic :items="items">
    <div class="my-content">
      <div>
        <h2>分配权限</h2>
        <h4 class="my-text">管理员账号：{{ admin.ID }}</h4>
        <div>
          <h4 class="my-text">权限选择：</h4>
          <b-form-group class="my-form-group">
            <b-form-checkbox
              v-model="allSelected"
              aria-describedby="flavours"
              aria-controls="flavours"
              @change="toggleAll"
            >
              <h4>{{ allSelected ? '取消超级管理员权限' : '超级管理员权限' }}</h4>
            </b-form-checkbox>
            <b-form-checkbox-group
              id="flavors"
              v-model="selected"
              :options="flavours"
              stacked
              size="lg"
              name="flavs"
              class="ml-4"
              aria-label="Individual flavours"
            />
            <b-button
              class="btn"
            >提交</b-button>
          </b-form-group>
        </div>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
export default {
  name: 'DistributeAuthority',
  components: {Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '管理员管理',
        href: '/admin/adminmanagement'
      }, {
        text: this.$route.query.admin_id.toString(),
        href: '/admin/adminmanagement/detail?admin_id=' + this.$route.query.admin_id.toString()
      }, {
        text: '分配权限',
        active: true
      }],
      admin: {
        ID: 'DingQuan'
      },
      flavours: ['用户评论管理权限', '课程管理权限', '客户管理权限', '日志权限', '订单管理权限', '管理员管理权限'],
      selected: [],
      allSelected: false
    }
  },
  watch: {
    selected () {
      this.allSelected = false
    }
  },
  methods: {
    toggleAll (checked) {
      this.selected = checked ? this.flavours.slice() : []
    }
  }
}
</script>

<style scoped>
  .my-content {
    margin: 40px;
    text-align: left;
  }

  .my-form-group {
    margin-top: 40px;
  }

  .my-text {
    margin-top: 50px;
  }

  .btn {
    margin-top: 250px;
    color: white;
    background-color: #8d4e91;
    border-color: #8d6592;
    border-radius: 10px;
    outline: none;
    box-shadow: #8d6592 inset;
  }

  .btn:hover,
  .btn:active {
    background-color: #5e0057;
  }
</style>
