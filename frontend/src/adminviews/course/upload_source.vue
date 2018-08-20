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
        <h3 class="float-left">上传课程资料</h3>
      </div>
      <form>
        <b-container>
          <b-row
            id="audio-row">
            <b-col cols="2"><h5>音频资料</h5></b-col>
            <b-col cols="8"><input
              v-model="fileNameList"
              type="text"
              class="text-left audio-input"
            ></b-col>
            <b-col
              cols="2">
              <b-button @click="openEntrance">打开</b-button>
            </b-col>
            <input
              id="upload-file"
              ref="input"
              type="file"
              accept="audio/mp3"
              multiple="multiple"
              @change="handleFileChange">
          </b-row>
          <b-row
            align-v="center">
            <b-col><h5 class="text-left">图片资料</h5></b-col>
          </b-row>
          <b-row>
            <UploadPicture upload_category="upload course pictures"/>
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
    <b-button
      id="sync-btn"
      @click="showModalSync"
    >同步音频/图片</b-button>
  </div>
</template>

<script>
import UploadPicture from './upload_picture'
export default {
  name: 'UploadSource',
  components: {UploadPicture},
  data () {
    return {
      inputId: '',
      audioDataList: [],
      fileNameList: [],
      errorText: '',
      countText: ''
    }
  },
  methods: {
    openEntrance () {
      this.$refs.input.click()
    },
    handleFileChange () {
      let input = this.$refs.input
      let files = input.files
      this.handleFile(files)
    },
    handleFile (files) {
      if (files && files.length > 0) {
        this.fileNameList.length = 0
        this.audioDataList.length = 0
      }
      for (let i = 0; i < files.length; i++) {
        let file = files[i]
        this.fileNameList.push(file.name)
      }
      if (files && files.length > 0) {
        this.countText = `${files.length}条音频`
      }
      this.preview(files)
    },
    preview (files) {
      let _this = this
      if (!files || !window.FileReader) return

      _this.audioDataList.push(files)
    },
    showModal () {
      this.$refs.upload_source.show()
    },
    hideModal () {
      this.$refs.upload_source.hide()
    },
    showModalSync () {
      this.$router.push({name: 'SyncPicture'})
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

  #upload-file {
    display: none;
  }

  #sync-btn {
    margin-left: 43px;
  }
</style>
