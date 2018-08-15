<template>
  <div
    id="studypage"
    style="width: 100%;">
    <UserNavbar/>
    <div
      id="content"
      style="width: 100%;">
      <div
        id="media"
        class="media-style">
        <div
          id="course-name"
          style="height: 10%; width: 100%; text-align: center;">
          <h3 style="color: #fff;">{{ course.name }}</h3>
        </div>
        <div
          id="image"
          style="height: 70%; width: 100%; text-align: center;">
          <b-img
            :src="course.image[0]"
            style="height: 100%; width: 70%;"/>
        </div>
        <div style="height: 20%; width: 100%; text-align: center;">
          <audio
            controls
            style="height: 100%; width: 99%;" >
            <source
              src="./media/test.mp3"
              type="audio/mpeg">
            Your browser does not support the audio element.
          </audio>
        </div>
      </div>
      <div
        id="introduction"
        style="width: 100%; border: 1px solid #999;">
        <div>
          <b-btn
            v-b-toggle.collapse3
            class="m-1">课程简介</b-btn>
          <b-collapse
            id="collapse3"
            visible>
            <b-card>
              &emsp; &emsp;{{ course.introduction }}
            </b-card>
          </b-collapse>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserNavbar from '../components/navbar'

export default {
  name: 'StudyPage',
  components: {
    UserNavbar
  },
  data () {
    return {
      course: {
        image: [
          require('../homepage/image/1.jpg'),
          require('../homepage/image/2.jpg'),
          require('../homepage/image/3.jpg'),
          require('../homepage/image/4.jpg')
        ],
        audio: require('./media/test.mp3'),
        introduction: '盼望着，盼望着，东风来了，春天的脚步近了。\n' +
          '一切都像刚睡醒的样子，欣欣然张开了眼。山朗润起来了，' +
          '水涨起来了，太阳的脸红起来了。\n' +
          '小草偷偷地从土地里钻出来，嫩嫩的，绿绿的。园子里，田野里，' +
          '瞧去，一大片一大片满是的。坐着，躺着，打两个滚，踢几脚球，赛几趟跑，' +
          '捉几回迷藏。风轻悄悄的，草软绵绵的。\n' +
          '桃树，杏树，梨树，你不让我，我不让你，都开满了花赶趟儿。' +
          '红的像火，粉的像霞，白的像雪。花里带着甜味；闭了眼，树上仿佛已经' +
          '满是桃儿，杏儿，梨儿。花下成千成百的蜜蜂嗡嗡的闹着，大小的蝴蝶' +
          '飞来飞去。野花遍地是：杂样儿，有名字的，没名字的，散在草丛里像眼' +
          '睛像星星，还眨呀眨的。\n' +
          '“吹面不寒杨柳风”，不错的，像母亲的手抚摸着你，风里带着些' +
          '新翻的泥土的气息，混着青草味儿，还有各种花的香，都在微微润湿的空' +
          '气里酝酿。鸟儿将巢安在繁花嫩叶当中，高兴起来了，呼朋引伴的卖弄清' +
          '脆的歌喉，唱出婉转的曲子，跟清风流水应和着。牛背上牧童的短笛，' +
          '这时候也成天嘹亮的响着。',
        name: '我们是坠胖的'
      }
    }
  }
}
</script>

<style>
  .media-style {
    width: 100%;
    height: 80%;
    background-image: url('./media/background.jpg');
  }
</style>
