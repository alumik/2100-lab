<template>
  <div>
    <div>
      <AdminNavbar/>
    </div>
    <div class="my-menu">
      <div>
        <Menu/>
      </div>
      <div class="father container-fluid">
        <BreadCrumb :items="items"/>
        <div class="my-row">
          <h2 class="my-list">课程详情</h2>
          <div class="button_group">
            <button
              type="button"
              class="row btn btn-primary btn-sm"
              @click="jump(0)"
            >修改课程</button>
            <button
              v-b-modal.delete
              type="button"
              class="row btn btn-primary btn-sm"
            >删除课程</button>
            <ConfirmModal
              id="delete"
              title="确认删除"
              text="您确定要删除该课程吗？"/>
          </div>
        </div>
        <div class="table_div">
          <table
            class="table table-striped table-hover"
            width="100%">
            <tbody>
              <tr>
                <td class="head-td">
                  课程代码
                </td>
                <td class="content-td">
                  {{ course.ID }}
                </td>
              </tr>
              <tr>
                <td class="head-td">
                  课程名
                </td>
                <td class="content-td">
                  {{ course.name }}
                </td>
              </tr>
              <tr>
                <td class="head-td">
                  阅后即焚时间
                </td>
                <td class="content-td">
                  {{ course.time }}
                </td>
              </tr>
              <tr>
                <td class="head-td">
                  价格
                </td>
                <td class="content-td">
                  {{ course.price }}
                </td>
              </tr>            <tr>
                <td class="head-td">
                  分销金比例
                </td>
                <td class="content-td">
                  {{ course.percent }}
                </td>
              </tr>
              <tr>
                <td class="head-td">
                  添加时间
                </td>
                <td class="content-td">
                  {{ course.add_time }}
                </td>
              </tr>
              <tr>
                <td class="head-td">
                  修改时间
                </td>
                <td class="content-td">
                  {{ course.change_time }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="my-intro">
          <h3 class="text-left">课程简介</h3>
          <p class="text-justify">{{ course.introduction }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
import ConfirmModal from '../components/ConfirmModal'
export default {
  name: 'BackendCourseDetail',
  components: {ConfirmModal, BreadCrumb, Menu, AdminNavbar},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '课程管理',
        href: '/admin/course'
      }, {
        text: '课程详情',
        active: true
      }],
      course: {
        'ID': '123456',
        'name': 'ascmk',
        'time': 'akscnk',
        'price': 'ascmk',
        'percent': 'aslcm',
        'add_time': 'aslcmklamlc',
        'change_time': 'ak njksdjvksnjk',
        'introduction': 'sncklsndkjvbweuiaciusDnmcksndkjcshndovi;jpaoerjvoigeahngvuihwroigrioahnvhios '
      }
    }
  },
  methods: {
    jump: function (id) {
      if (id === 0) {
        this.$router.push({name: 'EditCourse'})
      } else {
        this.$router.push({name: ''})
      }
    }
  }
}
</script>

<style scoped>
  .father {
    min-width: 500px;
    padding: 0;
  }

  .my-menu {
    display: flex;
  }

  .my-list {
    margin-left: 25px;
  }

  .my-row {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .head-td {
    width: 35%;
  }

  .content-td {
    width: 65%;
  }

  .button_group {
    display: flex;
  }

  .my-intro {
    margin-left: 25px;
  }

  .table {
    border: 1px solid #d3d9df;
  }

  .table_div {
    padding-right: 15px;
    padding-left: 15px;
  }

  .btn {
    margin-right: 25px;
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
