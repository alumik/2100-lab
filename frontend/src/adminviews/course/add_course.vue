<template>
  <Basic :items="items">
    <div class="my-content">
      <h2>新增课程</h2>
      <form>
        <div class="form-group form-inline">
          <label
            class="form-check-label my-label"
            for="coursename">课程名</label>
          <input
            id="coursename"
            class="input form-control col-lg-3"
            type="text">
        </div>
        <div class="form-group form-inline">
          <label
            class="form-check-label my-label"
            for="courseID">课程代码</label>
          <input
            id="courseID"
            class="input form-control col-lg-3"
            type="text">
        </div>
        <div class="form-group form-inline">
          <label
            class="form-check-label my-label"
            for="course_content">课程素材</label>
          <UploadSource id="course_content"/>
        </div>
        <div class="form-group form-inline">
          <div>
            <label
              class="form-check-label my-label"
              for="flare_time">阅后即焚时间</label>
          </div>
          <div
            id="flare_time"
            class="flare_time">
            <div>
              <div
                class="input-group">
                <input
                  id="flare_time_day"
                  class="input form-control col-lg-1"
                  type="text">
                <div class="input-group-prepend">
                  <span class="input-group-text">天</span>
                </div>
              </div>
            </div>
            <div>
              <div
                id="input-group-flare"
                class="input-group">
                <input
                  id="flare_time_hour"
                  class="input form-control col-lg-1"
                  type="text">
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
                class="input form-control col-lg-1"
                type="text">
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
          <div id="can_review">
            <label for="Yes"><input
              id="Yes"
              type="radio"
              name="optn"
              value="Yes"
            >是</label>
            <label for="No"><input
              id="No"
              type="radio"
              name="optn"
              value="No"
            >否</label>
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
                class="input form-control col-lg-3"
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
            id="intro-label"
            class="form-check-label my-label"
            for="intro">简介</label>
          <textarea
            id="intro"
            class="form-control col-lg-2"
            rows="6s">&nbsp;</textarea>
        </div>
        <button
          type="submit"
          class="btn my-btn">保存</button>
      </form>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'
import UploadSource from './upload_source'
export default {
  name: 'AddCourse',
  components: {UploadSource, Basic},
  data: function () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '课程管理',
        href: '/admin/course'
      }, {
        text: '新增课程',
        active: true
      }]
    }
  }
}
</script>

<style scoped>
  .my-content {
    margin: 40px;
    text-align: left;
  }

  .my-label {
    display: inline-block;
    width: 150px;
    text-align: left;
  }

  .flare_time {
    display: flex;
  }

  #flare_time_day {
    width: 80px;
    min-width: 80px;
    max-width: 80px;
  }

  #flare_time_hour {
    width: 70px;
    min-width: 70px;
    max-width: 70px;
  }

  .input {
    width: 260px;
    min-width: 260px;
    max-width: 260px;
  }

  #can_review {
    display: flex;
  }

  #input-group-flare {
    display: flex;
  }

  .my-btn,
  #intro {
    max-width: 405px;
  }

  #No {
    margin-left: 100px;
  }

  #intro-label {
    margin-top: 20px;
    margin-bottom: 20px;
  }

  #percent {
    width: 210px;
    min-width: 210px;
    max-width: 210px;
  }

  #price {
    width: 210px;
    min-width: 210px;
    max-width: 210px;
  }

  .btn {
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
