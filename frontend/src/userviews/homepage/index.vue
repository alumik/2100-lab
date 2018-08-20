<template>
  <body>
    <div class="navbar-style">
      <UserNavbar/>
    </div>
    <div class="homepage-container">
      <div class="carousel-container">
        <b-carousel
          id="carousel"
          :interval="2000"
          controls
          indicators
          img-responsive
          background="#ababab"
        >
          <b-carousel-slide
            class="height-change"
            caption="First slide"
            name="carousel-pic-1"
            text="Nulla vitae elit libero, a pharetra augue mollis interdum."
            img-src="https://picsum.photos/1024/300/?image=30"/>
          <b-carousel-slide
            class="height-change"
            caption="First slide"
            name="carousel-pic-2"
            text="Nulla vitae elit libero, a pharetra augue mollis interdum."
            img-src="https://picsum.photos/1024/300/?image=31"/>
          <b-carousel-slide
            class="height-change"
            caption="First slide"
            name="carousel-pic-3"
            text="Nulla vitae elit libero, a pharetra augue mollis interdum."
            img-src="https://picsum.photos/1024/300/?image=32"/>
          <b-carousel-slide
            class="height-change"
            caption="First slide"
            name="carousel-pic-4"
            text="Nulla vitae elit libero, a pharetra augue mollis interdum."
            img-src="https://picsum.photos/1024/300/?image=33"/>
        </b-carousel>
      </div>
      <div class="recommend-list">
        <RecommendList
          :courselist="freecourselist"
          list_title="免费课程"/>
        <RecommendList
          :courselist="paidcourselist"
          list_title="付费课程"/>
      </div>
    </div>
  </body>
</template>

<script>
import Basic from '../components/basic'
import UserNavbar from '../components/navbar'
import RecommendList from '../components/recommendList'
import axios from 'axios'

export default {
  name: 'Homepage',
  components: {
    UserNavbar,
    Basic,
    RecommendList
  },
  data () {
    return {
      freecourselist: [
        {
          id: 1,
          name: '数据库',
          introduction: '床前明月光',
          src: 'https://picsum.photos/1024/480/?image=54',
          value: 0
        },
        {
          id: 2,
          name: '数据结构',
          introduction: '疑是地上霜',
          src: 'https://picsum.photos/1024/480/?image=54',
          value: 0
        },
        {
          id: 3,
          name: '线性代数',
          introduction: '举头望明月',
          src: 'https://picsum.photos/1024/480/?image=58',
          value: 0
        },
        {
          id: 4,
          name: '离散数学',
          introduction: '低头思故乡',
          src: 'https://picsum.photos/1024/480/?image=55',
          value: 0
        },
        {
          id: 5,
          name: '概率论',
          introduction: '春眠不觉晓',
          src: 'https://picsum.photos/1024/480/?image=55',
          value: 0
        }
      ],
      paidcourselist: [
        {
          id: 6,
          name: '数据库',
          introduction: '床前明月光',
          src: 'https://picsum.photos/1024/480/?image=58',
          value: 100
        },
        {
          id: 7,
          name: '数据结构',
          introduction: '疑是地上霜',
          src: 'https://picsum.photos/1024/480/?image=54',
          value: 90
        },
        {
          id: 8,
          name: '线性代数',
          introduction: '举头望明月',
          src: 'https://picsum.photos/1024/480/?image=54',
          value: 80
        },
        {
          id: 9,
          name: '离散数学',
          introduction: '低头思故乡',
          src: 'https://picsum.photos/1024/480/?image=51',
          value: 70
        },
        {
          id: 10,
          name: '概率论',
          introduction: '春眠不觉晓',
          src: 'https://picsum.photos/1024/480/?image=52',
          value: 60
        }
      ]
    }
  },
  created: function () {
    axios.get('http://localhost:8000/api/v1/courses/course/get-recent-courses')
      .then(function (response) {
        // console.log(response)
      }).catch(function (error) {
        alert(error)
      })
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .homepage-container {
    margin-right: 0;
    margin-left: 0;
    border-width: 0.2rem;
  }

  .navbar-style {
    position: fixed;
    z-index: 999;
    width: 100%;
  }

  .recommend-list {
    width: 100%;
    padding: 1rem;
    margin: 0;
  }
</style>
