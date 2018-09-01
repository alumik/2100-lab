<template>
  <b-breadcrumb class="breadcrumb">
    <div
      v-for="link in links"
      :key="link.id">
      <b-breadcrumb-item
        :text="link.text"
        class="link"
        @click="jump(link.href)"/>
    </div>
    <b-breadcrumb-item
      :text="current.text"
      :active="true"/>
  </b-breadcrumb>
</template>

<script>
export default {
  name: 'BreadCrumb',
  /**
   * items: Array 面包屑所需名称及链接数据
   */
  props: {
    items: {
      type: Array,
      default: null
    }
  },
  /**
   * links: Array, 面包屑中非active部分数据
   * current: object, 面包屑中 active部分数据
   */
  computed: {
    links: function () {
      return this.items.slice(0, this.items.length - 1)
    },
    current: function () {
      return this.items[this.items.length - 1]
    }
  },
  /**
   * 该函数实现点击面包屑跳转。
   */
  methods: {
    jump: function (val) {
      this.$router.push(val)
    }
  }
}
</script>

<style scoped>
.link a {
  color: #337ab7;
}

.link a:focus,
.link a:hover {
  color: #204269;
}

.link::after {
  padding-right: 5px;
  padding-left: 5px;
  color: #999;
  content: '/';
}

.breadcrumb {
  margin: 0;
  background-color: white;
  border-radius: 0;
}
</style>
