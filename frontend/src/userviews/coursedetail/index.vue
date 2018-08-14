<template>
  <body
    style="width: 100%;">
    <UserNavbar/>
    <div style="margin-left: 10px;">
      <h3>课程详情</h3>
    </div>
    <div
      id="profile"
      class="row profile-style"
      style="height: 300px;">
      <div
        id="image"
        style="height: 100%; width: 50%;">
        <b-img
          :src="course.src"
          fluid
          thumbnail
          alt="Responsive image Thumbnail"
          class="img-thumbnail"
          style="height: 100%; width: 80%; margin-left: 10px;"/>
      </div>
      <div
        id="introduction"
        style="width: 50%;">
        <h3
          id="coursename"
          class="row"
          style="margin-top: 10px; positon: relative;">
          课程：{{ course.name }}</h3>
        <div class="row row-btn-style">
          <div
            id="studybutton"
            class="row-btn">
            <div v-if="course.value === 0">
              <b-button
                size="lg"
                variant="primary">
                开始学习
              </b-button>
            </div>
            <div v-else>
              <b-button
                size="lg"
                variant="primary">
                立即购买
              </b-button>
              <div/>
            </div>
          </div>
          <div
            id="sharebutton"
            class="row-btn">
            <b-button
              size="lg"
              variant="primary"
              class="row-btn">
              分享
            </b-button>
          </div>
          <b-badge
            pill
            variant="primary"
            class="reminder"
          >
            !</b-badge>
          <b-button
            size="lg"
            variant="primary"
            class="row-btn praise">
            <h style="color: lawngreen; font-size: 18px;">
              {{ course.num_of_praise }}
            </h>
            赞</b-button>
        </div>
        <div style="margin-top: 30px;">
          <div
            v-if="course.value!=0"
            class="row"
            style="position: relative;">
            <h5>现价 ￥{{ course.value-user_balance }}  ￥</h5>
            <h5 style="text-decoration: line-through;">{{ course.value }}</h5>
          </div>
          <div
            class="row"
            style="position: relative;">
            <h5>课程时效 {{ course.validate_time }} h</h5>
          </div>
          <div
            class="row"
            style="position: relative;">
            <h5>距离失效还有 {{ course.time_to_end }} h</h5>
          </div>
        </div>
      </div>
    </div>
    <div
      id="course-introduction"
      class="profile-style"
      style="height: 250px;">
      <h3>课程简介</h3>
      <p>&emsp; &emsp;{{ course.introduction }}</p>
    </div>
  </body>
</template>

<script>
import UserNavbar from '../components/navbar'

export default{
  name: 'CourseDetail',
  components: {
    UserNavbar
  },
  data () {
    return {
      user_balance: 50,
      course: {
        name: '小孔成像',
        value: 0,
        num_of_praise: 100,
        introduction: '近几年来，父亲和我都是东奔西走，家中光景是一日不如一日。' +
          '他少年出外谋生，独力支持，做了许多大事。哪知老境却如此颓唐！他触目伤怀' +
          '，自然情不能自已。情郁于中，自然要发之于外；家庭琐屑便往往触他之怒。' +
          '他待我渐渐不同往日。但最近两年不见，他终于忘却我的不好，只是惦记着我，' +
          '惦记着他的儿子。我北来后，他写了一信给我，信中说道：“我身体平安，' +
          '惟膀子疼痛厉害，举箸14提笔，诸多不便，大约大去之期15不远矣。”我读到此处，' +
          '在晶莹的泪光中，又看见那肥胖的、青布棉袍黑布马褂的背影。唉！' +
          '我不知何时再能与他相见！',
        src: require('../components/image/1.jpg'),
        validate_time: 24,
        time_to_end: 24
      }
    }
  }
}
</script>

<style>
  .profile-style {
    margin: 10px;
    border: 3px solid #f00;
    -webkit-box-shadow: 10px 8px 10px 3px #999;
    -moz-box-shadow: 10px 8px 10px 3px #000;
    box-shadow: 10px 8px 10px 3px #999;
    opacity: 0.9;
  }

  .row-btn {
    margin-right: 50px;
  }

  .reminder {
    position: absolute;
    bottom: 3px;
    left: 240px;
    height: 30%;
    margin-left: 10px;
  }

  .row-btn-style {
    position: relative;
    width: 100%;
    padding: 3px;
    margin-top: 30px;
  }
</style>
