<template>
  <div class="share-zone">
    <simple-line-icons
      icon="share"
      size="small"/>
    <a
      :href="sina_url"
      target="_blank">
      <img
        class="share-icon"
        src="../../assets/sina1.svg">
    </a>
    <a
      :href="qq_url"
      target="_blank">
      <img
        class="share-icon"
        src="../../assets/qq1.svg">
    </a>
    <b-dropdown
      dropup
      variant="link"
      class="weixin"
      size="lg"
      no-caret>
      <template slot="button-content">
        <img
          class="share-icon"
          src="../../assets/wechat1.svg">
      </template>
      <qrcode
        :options="{ size: 150 }"
        :value="url"/>
    </b-dropdown>
    <a
      :href="zone_url"
      target="_blank">
      <img
        class="zone-icon"
        src="../../assets/zone1.svg">
    </a>
  </div>
</template>

<script>
export default {
  name: 'SocialShare',
  props: {
    url: {
      type: String,
      default () {
        return ''
      }
    }
  },
  computed: {
    /**
     * 返回新浪微博跳转链接 */
    sina_url: function () {
      return 'http://v.t.sina.com.cn/share/share.php?url=' + this.url + '&title=\'2100实验室\''
    },
    /**
     * 返回腾讯qq跳转链接 */
    qq_url: function () {
      return 'http://connect.qq.com/widget/shareqq/index.html?title=2100实验室&url=' + this.url
    },
    /**
     * 返回qq空间跳转链接 */
    zone_url: function () {
      return 'http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url=' + this.url + '&title=\'2100实验室\''
    }
  }
}

</script>

<style scoped>
.share-zone {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  width: 230px;
  height: 40px;
}

.weixin >>> button {
  padding: 0;
}

.share-icon {
  width: 40px;
  height: 40px;
}

.zone-icon {
  width: 45px;
  height: 45px;
}

.zone-icon:hover {
  -ms-transform: scale(1.2, 1.2);
  -webkit-transform: scale(1.2, 1.2);
  transform: scale(1.2, 1.2);
}

.share-icon:hover {
  -ms-transform: scale(1.2, 1.2);
  -webkit-transform: scale(1.2, 1.2);
  transform: scale(1.2, 1.2);
}

</style>
