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
  props: {
    items: {
      type: Array,
      default: null
    }
  },
  computed: {
    links: function () {
      return this.items.slice(0, this.items.length - 1)
    },
    current: function () {
      return this.items[this.items.length - 1]
    }
  },
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
    color: #23527c;
  }

  .link::after {
    padding-right: 5px;
    padding-left: 5px;
    color: #999;
    content: '/';
  }

  .breadcrumb {
    background-color: white;
    border-radius: 0;
    margin: 0;
  }
</style>
