<template>
  <div>
    <AdminNavbar/>
    <BreadCrumb :items="items"/>
    <Pagination :rows="rows"/>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import BreadCrumb from '../../components/breadCrumb'
import Pagination from '../../components/pagination'
export default {
  name: 'MessageManagement',
  components: { AdminNavbar, BreadCrumb, Pagination },
  data () {
    return {
      items: [{
        text: 'Admin',
        to: { name: 'AdminNavBar' }
      }, {
        text: 'Manage',
        active: true
      }],
      rows: 20
    }
  }
}
</script>
