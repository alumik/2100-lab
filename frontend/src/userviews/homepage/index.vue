<template>
  <div>
    <UserNavbar/>
    <div class="homepage-container">
      <div
        class="slide-show"
        @mousemove="clearInv"
        @mouseout="runInv">
        <div class="slide-img">
          <img :src="slides[nowIndex].src">
        </div>
        <h2>{{ slides[nowIndex].title }}</h2>
        <ul class ="slide-pages">
          <li @click="goto(preIndex)">&lt;</li>
          <li
            @v-for="(item,index) in slides"
            @click="goto(index)"/>
          <li @click="goto(nextIndex)">&gt;</li>
        </ul>
      </div>
    </div>
    <RecommendList
      :courselist="freecourselist"
      list_title="免费课程列表"/>
    <RecommendList
      :courselist="paidcourselist"
      list_title="付费课程列表"/>
  </div>

</template>

<script>
import UserNavbar from '../components/navbar'
import RecommendList from '../components/recommendList'

export default {
  name: 'Homepage',
  components: {
    UserNavbar,
    RecommendList
  },
  data () {
    return {
      freecourselist: [
        {
          id: 1,
          name: '数据库',
          introduction: '床前明月光',
          src: require('./image/1.jpg'),
          value: 0
        },
        {
          id: 2,
          name: '数据结构',
          introduction: '疑是地上霜',
          src: require('./image/2.jpg'),
          value: 0
        },
        {
          id: 3,
          name: '线性代数',
          introduction: '举头望明月',
          src: require('./image/3.jpg'),
          value: 0
        },
        {
          id: 4,
          name: '离散数学',
          introduction: '低头思故乡',
          src: require('./image/4.jpg'),
          value: 0
        },
        {
          id: 5,
          name: '概率论',
          introduction: '春眠不觉晓',
          src: require('./image/1.jpg'),
          value: 0
        }
      ],
      paidcourselist: [
        {
          id: 6,
          name: '数据库',
          introduction: '床前明月光',
          src: require('./image/1.jpg'),
          value: 100
        },
        {
          id: 7,
          name: '数据结构',
          introduction: '疑是地上霜',
          src: require('./image/2.jpg'),
          value: 90
        },
        {
          id: 8,
          name: '线性代数',
          introduction: '举头望明月',
          src: require('./image/3.jpg'),
          value: 80
        },
        {
          id: 9,
          name: '离散数学',
          introduction: '低头思故乡',
          src: require('./image/4.jpg'),
          value: 70
        },
        {
          id: 10,
          name: '概率论',
          introduction: '春眠不觉晓',
          src: require('./image/1.jpg'),
          value: 60
        }
      ],
      slides: [
        {
          src: require('./image/1.jpg'),
          title: '欢迎小朋友来到2100实验室'
        },
        {
          src: require('./image/2.jpg'),
          title: '这里是小实验的天堂'
        },
        {
          src: require('./image/3.jpg'),
          title: '陪伴你度过2100天美好的时光'
        },
        {
          src: require('./image/4.jpg'),
          title: '从小培养实验兴趣'
        }
      ],
      inv: 1500,
      nowIndex: 0,
      nowsrc: './image/4.jpg'
    }
  },
  computed: {
    preIndex () {
      if (this.nowIndex === 0) {
        return this.slides.length - 1
      } else {
        return this.nowIndex - 1
      }
    },
    nextIndex () {
      if (this.nowIndex === this.slides.length - 1) {
        return 0
      } else {
        return this.nowIndex + 1
      }
    }
  },
  mounted () {
    console.log(this.slides)
    this.runInv()
  },
  methods: {
    goto (index) {
      this.nowIndex = index
    },
    runInv () {
      this.invId = setInterval(() => {
        this.goto(this.nextIndex)
      }, this.inv)
    },
    clearInv () {
      clearInterval(this.invId)
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .homepage-container {
    background-color: #fff;
  }

  img {
    display: inline-block;
    width: 1305px;
    height: 400px;
  }

  .slide-show {
    position: relative;
    width: 1305px;
    height: 400px;
    overflow: hidden;
  }

  .slide-img {
    width: 100%;
  }

  .slide-img img {
    position: relative;
    top: 0;
    width: 100%;
  }

  .slide-show h2 {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 30px;
    padding-left: 15px;
    line-height: 30px;
    color: #fff;
    text-align: left;
    background-color: #000;
    opacity: 0.5;
  }

  .slide-pages {
    position: absolute;
    right: 15px;
    bottom: 10px;
  }

  .slide-pages li {
    display: inline-block;
    padding: 0 10px;
    color: #fff;
    cursor: pointer;
  }

  .slide-pages li .on {
    text-decoration: underline;
  }
</style>
