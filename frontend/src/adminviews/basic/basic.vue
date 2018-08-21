<template>
  <div>
    <AdminNavbar/>
    <div class="my-menu">
      <Menu
        :lists="lists"
        @jump="jump"/>
      <div class="container-fluid my-container">
        <div class="my-bread">
          <BreadCrumb :items="items"/>
        </div>
        <slot/>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import Menu from '../components/menu'
import BreadCrumb from '../../components/breadCrumb'
export default {
  name: 'Basic',
  components: {BreadCrumb, Menu, AdminNavbar},
  props: {
    items: {
      type: Array,
      default: null
    }
  },
  data () {
    return {
      lists: [
        {id: 1, text: this.$t('menu.course'), isActive: false, path: '/admin/course'},
        {id: 2, text: this.$t('menu.message'), isActive: false, path: '/admin/message'},
        {id: 3, text: this.$t('menu.user'), isActive: false, path: '/admin/user'},
        {id: 4, text: this.$t('menu.order'), isActive: false, path: '/admin/order'},
        {id: 5, text: this.$t('menu.admin'), isActive: false, path: '/admin/adminmanagement'},
        {id: 6, text: this.$t('menu.data'), isActive: false, path: '/admin/data'},
        {id: 7, text: this.$t('menu.log'), isActive: false, path: '/admin/log'}
      ]}
  },
  methods: {
    jump (id) {
      for (let list = 0; list < 7; list = list + 1) {
        this.lists[list].isActive = false
      }
      this.lists[id - 1].isActive = true
    }
  }
}
</script>

<style scoped>
  .my-menu {
    display: flex;
  }

  .my-container {
    padding: 0;
    margin-left: 200px;
  }

  @media (max-width: 768px) {
    .my-container {
      margin-left: 0;
    }
  }
</style>
