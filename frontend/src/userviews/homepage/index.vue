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
  </div>

</template>

<script>
import UserNavbar from '../components/navbar'

export default {
  name: 'Homepage',
  components: {
    UserNavbar
  },
  data () {
    return {
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
