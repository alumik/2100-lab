<template>
  <div>
    <a
      id="pre-sort-btn"
      class="btn"
      @click="show_modal">
      <simple-line-icons
        id="change-icon"
        icon="picture"
        color="white"
        class="icon"/>
      图片预排序
    </a>
    <b-modal
      ref="edit_picture"
      size="lg"
      ok-title="确认"
      cancel-title="取消"
      centered
      no-close-on-esc>
      <div
        slot="modal-header"
        class="w-100">
        <h3 class="float-left">图片预排序</h3>
      </div>
      <div class="my-body">
        <b-row>
          <b-col cols="3"><h5>已排序图片</h5></b-col>
        </b-row>
        <b-container
          fluid
          class="row choose-list">
          <b-row
            v-for="img in sort_image_data_list"
            :key="img.index"
            class="choose-row">
            <b-col>
              <b-img
                :src="img.image"
                fluid
                alt="test-image"
                class="img-thumbnail"
                @click="dropback(img)"/>
            </b-col>
          </b-row>
        </b-container>
        <b-row>
          <b-col cols="3"><h5>未排序图片</h5></b-col>
        </b-row>
        <b-container
          fluid
          class="row choose-list">
          <b-row
            v-for="img in choose_image_data_list"
            :key="img.data"
            class="choose-row"
          >
            <b-col>
              <b-img
                :src="img.image"
                fluid
                alt="test-image"
                class="img-thumbnail"
                @click="dropout(img)"/>
            </b-col>
          </b-row>
        </b-container>
      </div>
      <div
        slot="modal-footer"
        class="w-100">
        <b-row class="define-btn">
          <b-col cols="8"/>
          <b-col cols="2">
            <a
              id="upload-btn"
              class="btn"
              @click="send_modal">
              上传
            </a>
          </b-col>
          <b-col cols="2">
            <a
              id="cancel-btn"
              class="btn"
              @click="hide_modal">
              取消
            </a>
          </b-col>
        </b-row>
      </div>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: 'PreSortPicture',
  /**
   * 预传入信息列表：
   * 预传入图片列表
   * 是否有上传更新标志变量
   */
  props: {
    choose_image_data_list_origin: {
      default: () => {},
      type: Array
    },
    is_uploaded: {
      default: true,
      type: Boolean
    }
  },
  /**
   * @returns {{
   * sort_image_data_list: Array,
   * 排序好图片数据存储区
   * choose_image_data_list: Array,
   * 传入图片信息拷贝的存储区
   * now_index: number,
   * 当前排序图片数量变量
   * is_returned: boolean
   * 结果是否上传标志变量
   * }}
   */
  data: function () {
    return {
      sort_image_data_list: [],
      choose_image_data_list: [],
      now_index: 0,
      is_returned: true
    }
  },
  methods: {
    /**
     * 打开预排序模态框函数
     * 进行数据预处理
     * 如果当前排序结果已上传或者上传图片列表有更新
     * 就重新深拷贝图片信息至存储区
     */
    show_modal () {
      if (this.is_returned === true || this.is_uploaded === true) {
        this.$emit('update_is_uploaded', this.is_uploaded)
        this.is_returned = false
        this.now_index = 0
        this.choose_image_data_list = []
        this.sort_image_data_list = []
        this.choose_image_data_list.length = 0
        for (let i = 0; i < this.choose_image_data_list_origin.length; i++) {
          this.choose_image_data_list.push(
            this.choose_image_data_list_origin[i]
          )
        }
      }
      this.$refs.edit_picture.show()
    },
    /**
     * 将图片从未排序区弹到已排序区处理函数
     * @param img
     */
    dropout (img) {
      let index = img.index
      for (let i = index; i < this.choose_image_data_list.length; i++) {
        this.choose_image_data_list[i].index -= 1
      }
      this.choose_image_data_list.splice(img.index - 1, 1)
      img.index = this.now_index + 1
      this.now_index += 1
      this.sort_image_data_list.push(img)
    },
    /**
     * 将图片从已排序区弹到未排序区处理函数
     * @param img
     */
    dropback (img) {
      this.now_index -= 1
      for (let i = img.index; i < this.sort_image_data_list.length; i++) {
        this.sort_image_data_list[i].index -= 1
      }
      this.sort_image_data_list.splice(img.index - 1, 1)
      img.index = this.choose_image_data_list.length + 1
      this.choose_image_data_list.push(img)
    },
    /**
     * 发送处理结果函数
     * 如果图片全部处理完毕，则发出信号并把排序好的图片列表发到父组件
     * 更新标志变量
     */
    send_modal () {
      if (
        this.sort_image_data_list.length ===
        this.choose_image_data_list_origin.length
      ) {
        this.now_index = 0
        this.$emit('upload_sorted_pic', this.sort_image_data_list.slice())
        this.choose_image_data_list.length = 0
        this.sort_image_data_list.length = 0
        this.$refs.edit_picture.hide()
        this.is_returned = true
      }
    },
    /**
     * 关闭预排序图片模态框函数
     */
    hide_modal () {
      this.$emit('reset_is_uploaded', this.is_uploaded)
      for (let i = 1; i <= this.choose_image_data_list_origin.length; i++) {
        this.choose_image_data_list_origin[i - 1].index = i
      }
      this.$refs.edit_picture.hide()
    }
  }
}
</script>

<style scoped>
.my-body {
  margin-right: 16px;
  margin-left: 16px;
}

.choose-list {
  display: -webkit-box;
  min-height: 200px;
  max-height: 200px;
  padding: 0;
  margin: 0;
  overflow: hidden;
  overflow-x: auto;
  background-color: lightgray;
}

.choose-row {
  width: 200px;
  max-width: 200px;
  height: 200px;
  max-height: 200px;
  padding: 5px;
}

#upload-btn,
#cancel-btn {
  color: white;
  background-color: #337ab7;
}

#upload-btn:hover,
#cancel-btn:hover {
  background-color: #286090;
}

h5 {
  margin-top: 20px;
  margin-bottom: 20px;
}

#pre-sort-btn {
  margin-right: 5px;
  margin-left: 5px;
  color: white;
  background-color: #337ab7;
}

#pre-sort-btn:hover {
  background-color: #286090;
}
</style>
