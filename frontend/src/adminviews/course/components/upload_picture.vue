<!--suppress ALL -->
<template>
  <div
    ref="uploader"
    class="img-uploader"
    @drop="handleDrop">
    <p
      v-if="!hasImages"
      class="img-uploader-placeholder">{{ placeholder }}</p>
    <div
      v-if="hasImages"
      class="img-uploader-preview-list">
      <div
        v-for="(data,index) in imageDataList"
        :key="index"
        class="img-uploader-preview">

        <div class="preview-img">
          <img :src="data">
        </div>
        <div
          v-if="hasImages"
          class="img-uploader-mask">
          <p
            class="img-uploader-file-name"
            @click="openInput()">{{ fileNameList[index] }}</p>
        </div>
        <img
          src="../../../assets/logo.png"
          class="img-uploader-delete-btn"
          @click="deleteImg(index)">
      </div>
    </div>

    <label
      v-if="!hasImages"
      :for="inputId"
      class="img-uploader-label"/>
    <input
      ref="input"
      :id="inputId"
      type="file"
      class="hidden-input"
      accept="image/gif,image/jpeg,image/jpg,image/png,image/svg"
      multiple="multiple"
      @change="handleFileChange">
    <div
      v-if="errorText.length"
      class="img-uploader-error">{{ errorText }}</div>
    <div
      v-if="countText.length"
      class="img-uploader-count">{{ countText }}</div>
  </div>
</template>

<script>
import resizeImage from './resize'

export default {
  name: 'UploadPicture',
  props: {
    placeholder: {
      default: '点击上传图片',
      type: String
    },
    onChange: {
      default: (files) => {
        if (files) {
        }
      },
      type: Function
    },
    maxSize: {
      default: 3072,
      type: Number
    }
  },
  data () {
    return {
      inputId: '',
      imageDataList: [],
      fileNameList: [],
      errorText: '',
      countText: ''
    }
  },
  computed: {
    hasImages () {
      return this.imageDataList.length > 0
    },
    sizeFormatted () {
      let result = 0
      if (this.maxSize < 1024) {
        result = this.maxSize + 'K'
      } else {
        result = (this.maxSize / 1024).toFixed(this.maxSize % 1024 > 0 ? 2 : 0) + 'M'
      }
      return result
    }
  },
  mounted () {
    this.inputId = this.id || Math.round(Math.random() * 100000);
    ['drop', 'dragenter', 'dragover', 'dragleave'].forEach((eventName) => {
      this.preventDefaultEvent(eventName)
    })
  },
  methods: {
    handleFileChange () {
      let input = this.$refs.input
      let files = input.files
      this.handleFile(files)
    },
    handleDrop (e) {
      let files = e.dataTransfer.files
      this.handleFile(files)
    },
    preventDefaultEvent (eventName) {
      document.addEventListener(eventName, function (e) {
        e.preventDefault()
      }, false)
    },
    openInput () {
      this.$refs.input.click()
    },
    deleteImg (index) {
      this.imageDataList.splice(index, 1)
      this.errorText = ''
      this.countText = `${this.imageDataList.length}张图片`
    },
    handleFile (files) {
      if (files && files.length > 0) {
        this.fileNameList.length = 0
        this.imageDataList.length = 0
      }
      for (let i = 0; i < files.length; i++) {
        let file = files[i]
        let size = Math.floor(file.size / 1024)
        if (size > this.maxSize) {
          this.countText = ''
          this.errorText = `文件大小不能超过${this.sizeFormatted}`
          return false
        }
        this.fileNameList.push(file.name)
      }

      if (files && files.length > 0) {
        this.errorText = ''
        this.countText = `${files.length}张图片`
      }
      this.onChange && this.onChange(files)
      this.$emit('onChange', files)

      this.preview(files)
    },
    preview (files) {
      let _this = this
      if (!files || !window.FileReader) return

      for (let i = 0; i < files.length; i++) {
        let file = files[i]
        let reader = new FileReader()
        reader.onload = function (e) {
          resizeImage(e.target.result, 150, 150, function (result) {
            _this.imageDataList.push(result)
          })
        }
        reader.readAsDataURL(file)
      }
    }
  }
}
</script>

<style scoped>
  .hidden-input {
    display: none;
  }

  .img-uploader {
    position: relative;
    width: auto;
    min-width: 260px;
    max-width: 800px;
    height: calc(150px + 25px * 2);
    background: #ebebeb;
    border-radius: 5px;
  }

  .img-uploader-placeholder {
    position: absolute;
    top: 50%;
    width: 100%;
    margin: 0;
    font-size: 15px;
    color: #aaa;
    text-align: center;
    transform: translate(0%, -50%);
  }

  .img-uploader-preview-list {
    width: 100%;
    height: calc(150px + 18px * 2);
    margin: 5px 10px;
    overflow: hidden;
    overflow-x: auto;
    text-align: center;
    white-space: nowrap;
    -webkit-backface-visibility: hidden;
    -webkit-perspective: 1000;
    -webkit-overflow-scrolling: touch;
  }

  .img-uploader-preview {
    z-index: 2;
    display: inline-block;
    min-height: 150px;
    margin: 10px;
    background: #333;
    border-radius: 10px;
    transition: 0.3s cubic-bezier(0.3, 0, 0.2, 1);
  }

  .img-uploader-preview:hover {
    transform: scale(1.02);
  }

  .img-uploader-mask {
    position: absolute;
    bottom: 0;
    display: none;
    width: 150px;
    text-align: center;
    background: rgba(0, 0, 0, 0.6);
    border-radius: 1px;
  }

  .img-uploader-delete-btn {
    position: absolute;
    top: 0;
    right: 0;
    display: none;
    width: 25px;
    height: 25px;
    margin: 5px;
  }

  .img-uploader-preview:hover .img-uploader-mask {
    display: block;
  }

  .img-uploader-preview:hover .img-uploader-delete-btn {
    display: block;
  }

  .img-uploader-preview .preview-img {
    width: 150px;
    height: 150px;
    overflow: hidden;
  }

  .img-uploader-label {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    margin-bottom: 0;
    cursor: pointer;
  }

  .img-uploader-file-name {
    display: inline-block;
    max-width: 90%;
    padding-top: 10px;
    margin: 0;
    overflow: hidden;
    font-size: 5px;
    color: white;
    text-overflow: ellipsis;
    white-space: nowrap;
    cursor: pointer;
  }

  .img-uploader-error {
    position: absolute;
    bottom: -28px;
    width: 100%;
    font-size: 12px;
    color: #e55;
  }

  .img-uploader-count {
    position: absolute;
    bottom: -28px;
    width: 100%;
    font-size: 12px;
    color: #573e51;
  }
</style>
