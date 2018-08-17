<template>
  <div class="button-group">
    <b-button @click="showModal">
      管理资料
    </b-button>
    <b-modal
      ref="upload_source"
      size="lg"
      centered
      no-close-on-esc>
      <div
        slot="modal-header"
        class="w-100">
        <h3 class="float-left">课程资料</h3>
      </div>
      <form>
        <b-container>
          <b-row
            id="audio-row">
            <b-col cols="2"><h5>音频资料</h5></b-col>
            <b-col cols="8"><input
              type="text"
              class="text-left audio-input"
            ></b-col>
            <b-col
              id="upload-btn"
              cols="2">
            <b-button>上传</b-button></b-col>
          </b-row>
          <b-row
            align-v="center">
            <b-col><h5 class="text-left">图片资料</h5></b-col>
          </b-row>
          <b-row>
            <UploadPicture/>
          </b-row>
        </b-container>
      </form>
      <div
        slot="modal-footer"
        class="w-100">
        <b-row class="define-btn">
          <b-col cols="8"/>
          <b-col cols="2">
            <b-button
              @click="hideModal">上传</b-button>
          </b-col>
          <b-col cols="2">
            <b-button
              @click="hideModal">取消</b-button>
          </b-col>
        </b-row>
      </div>
    </b-modal>
    <b-btn
      id="sync-btn"
    >同步音频/图片</b-btn>
  </div>
</template>

<script>
import UploadPicture from './upload_picture'
export default {
  name: 'UploadSource',
  components: {UploadPicture},
  methods: {
    showModal () {
      this.$refs.upload_source.show()
    },
    hideModal () {
      this.$refs.upload_source.hide()
    }
  }
}
</script>

<style scoped>
  .button-group {
    display: flex;
    flex-direction: row;
    justify-content: left;
    max-width: 8rem;
  }

  .audio-input {
    width: 100%;
  }

  .define-btn {
    display: flex;
    flex-direction: row;
    justify-content: right;
  }

  #sync-btn {
    margin-left: 43px;
  }
</style>
