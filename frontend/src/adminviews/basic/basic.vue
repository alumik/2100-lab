<template>
  <div class="basic">
    <AdminNavbar @hide="hide"/>
    <div class="my-menu">
      <Menu
        :lists="lists"
        :hidden="hidden"
        @blur="hide"
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
  components: { BreadCrumb, Menu, AdminNavbar },
  props: {
    items: {
      type: Array,
      default: null
    }
  },
  data () {
    return {
      hidden: false,
      lists: [
        {
          id: 1,
          text: this.$t('menu.course'),
          isActive: false,
          path: '/admin/course'
        },
        {
          id: 2,
          text: this.$t('menu.message'),
          isActive: false,
          path: '/admin/message'
        },
        {
          id: 3,
          text: this.$t('menu.user'),
          isActive: false,
          path: '/admin/user'
        },
        {
          id: 4,
          text: this.$t('menu.order'),
          isActive: false,
          path: '/admin/order'
        },
        {
          id: 5,
          text: this.$t('menu.log'),
          isActive: false,
          path: '/admin/log'
        },
        {
          id: 6,
          text: this.$t('menu.data'),
          isActive: false,
          path: '/admin/data/total'
        },
        {
          id: 7,
          text: this.$t('menu.admin'),
          isActive: false,
          path: '/admin/adminmanagement'
        }
      ]
    }
  },
  mounted () {
    let that = this
    document.addEventListener('click', e => {
      if (
        e.target.id !== 'sidebar' &&
        e.target.id !== 'hide-button' &&
        e.target.id !== 'hide-span'
      ) {
        that.hidden = false
      }
    })
  },
  methods: {
    hide () {
      this.hidden = !this.hidden
    },
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
.basic {
  background-color: #e9ecf3;
}

.my-menu {
  display: flex;
}

.my-container {
  width: calc(100% - 200px);
  padding: 0;
  margin-left: 200px;
}

@media (max-width: 991px) {
  .my-container {
    width: 100%;
    margin-left: 0;
  }
}
</style>
