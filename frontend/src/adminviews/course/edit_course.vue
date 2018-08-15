<template>
  <div>
    <div>
      <AdminNavbar style="min-width: 500px;"/>
    </div>
    <div style="display: flex;">
      <div>
        <Menu/>
      </div>
      <div class="father container-fluid">
        <BreadCrumb :items="items"/>
        <div class="my-row">
          <h2 class="text-left">修改课程</h2>
        </div>
        <form class="text-left son">
          <div class="form-group form-inline">
            <label
              class="form-check-label my-label"
              for="coursename">课程名</label>
            <input
              id="coursename"
              v-model="course.name"
              class="input form-control col-lg-3"
              type="text">
          </div>
          <div class="form-group form-inline">
            <label
              class="form-check-label my-label"
              for="courseID">课程代码</label>
            <input
              id="courseID"
              v-model="course.ID"
              class="input form-control col-lg-3"
              type="text">
          </div>
          <div class="form-group form-inline">
            <label
              class="form-check-label my-label"
              for="course_content">课程素材</label>
            <div
              id="course_content"
              class="button-group">
              <button
                type="button"
                class="col-lg-8 btn btn-primary btn-sm"
                @click="edit_course"
              >管理资料</button>
              <button
                type="button"
                class="col-lg-8 btn btn-primary btn-sm"
                style="margin-left: 25px; max-width: 10rem;"
                @click="delete_course"
              >同步音频/图片</button>
            </div>
          </div>
          <div class="form-group form-inline">
            <div>
              <label
                class="form-check-label my-label"
                for="flare_time">阅后即焚时间</label>
            </div>
            <div style="display: flex;">
              <div>
                <div
                  class="input-group"
                  style="display: flex;">
                  <input
                    id="flare_time"
                    v-model="course.time"
                    class="input form-control col-lg-1"
                    type="text"
                    style="width: 80px; min-width: 80px; max-width: 80px;">
                  <div class="input-group-prepend">
                    <span class="input-group-text">天</span>
                  </div>
                </div>
              </div>
              <div>
                <div
                  class="input-group"
                  style="display: flex;">
                  <input
                    id="flare_time_1"
                    v-model="course.time"
                    class="input form-control col-lg-1"
                    type="text"
                    style="width: 70px; min-width: 70px; max-width: 70px;">
                  <div class="input-group-prepend">
                    <span class="input-group-text">小时</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="form-group form-inline">
            <label
              class="form-check-label my-label"
              for="price">金额</label>
            <div>
              <div class="input-group">
                <input
                  id="price"
                  v-model="course.price"
                  class="input form-control col-lg-1"
                  type="text"
                  style="width: 210px; min-width: 210px; max-width: 210px;">
                <div class="input-group-prepend">
                  <span class="input-group-text">元</span>
                </div>
              </div>
            </div>
          </div>
          <div class="form-group form-inline">
            <label
              class="form-check-label my-label"
              for="can_review">可评论</label>
            <div
              id="can_review"
              style="display: flex;">
              <label for="Yes"><input
                id="Yes"
                v-model="course.can_review"
                type="radio"
                name="optn"
                value="Yes"
              >是</label>
              <label for="No"><input
                id="No"
                v-model="course.can_review"
                type="radio"
                name="optn"
                value="No"
                style="margin-left: 100px;">否</label>
            </div>
          </div>
          <div class="form-inline">
            <label
              class="form-check-label my-label"
              for="percent">分销金比例</label>
            <div>
              <div class="input-group">
                <input
                  id="percent"
                  v-model="course.percent"
                  class="input form-control col-lg-3"
                  style="width: 210px; min-width: 210px; max-width: 210px;"
                  type="text">
                <div class="input-group-prepend">
                  <span
                    class="input-group-text">%</span>
                </div>
              </div>
            </div>
          </div>
          <div class="form-group">
            <label
              id="intro-l"
              class="form-check-label my-label"
              for="intro">简介</label>
            <textarea
              id="intro"
              v-model="course.introduction"
              class="form-control col-lg-2"
              rows="6s"/>
          </div>
          <button
            type="submit"
            class="btn btn-primary my-btn">保存</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
export default {
  name: 'EditCourse',
  components: {BreadCrumb, Menu, AdminNavbar},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '课程管理',
        href: '/admin/course'
      }, {
        text: 'A001',
        href: '/admin/course/detail'
      }, {
        text: '修改课程',
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
        'introduction': 'sncklsndkjvbweuiaciusDnmcksndkjcshndovi;jpaoerjvoigeahngvuihwroigrioahnvhios',
        'can_review': 'Yes'
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

  .my-row {
    margin-top: 40px;
    margin-bottom: 40px;
    margin-left: 20px;
  }

  .my-label {
    display: inline-block;
    width: 150px;
    margin-left: 20px;
    text-align: left;
  }

  .button-group {
    display: flex;
    flex-direction: row;
    justify-content: left;
    max-width: 8rem;
  }

  .input {
    width: 260px;
    min-width: 260px;
    max-width: 260px;
  }

  .my-btn,
  #intro {
    max-width: 405px;
    margin-left: 20px;
  }

  #intro-l {
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .son {
    margin-left: 50px;
  }

</style>
