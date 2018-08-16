<template>
  <div class="html">
    <AdminNavbar class="navbar"/>
    <div id="body">
      <Menu/>
      <div id="management">
        <BreadCrumb :items="items"/>
        <h1>日志查询</h1>
        <div class="table_div">
          <table class="table table-bordered">
            <thead>
              <tr>
                <th>管理员账号</th>
                <th>开始时间</th>
                <th>结束时间</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <input
                    id="admin"
                    type="text"
                    class="form-control">
                </td>
                <td>
                  <div class="col-md-6">
                    <date-picker
                      v-model="date"
                      :config="options"/>
                  </div>
                </td>
                <td>
                  <div class="col-md-6">
                    <date-picker
                      v-model="date"
                      :config="options"/>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <h4>查询项目</h4>
        <div class="checkbox_div">
          <form>
            <div class="custom-control custom-checkbox custom-control-inline form-group">
              <input
                id="check-a"
                type="checkbox"
                class="custom-control-input form-control"
                name="a">
              <label
                class="custom-control-label form-check-label"
                for="check-a">a</label>
            </div>
            <div class="custom-control custom-checkbox custom-control-inline form-group">
              <input
                id="check-b"
                type="checkbox"
                class="custom-control-input form-control"
                name="b">
              <label
                class="custom-control-label form-check-label"
                for="check-b">b</label>
            </div>
            <div class="custom-control custom-checkbox custom-control-inline form-group">
              <input
                id="check-c"
                type="checkbox"
                class="custom-control-input form-control"
                name="c">
              <label
                class="custom-control-label form-check-label"
                for="check-c">c</label>
            </div>
            <div class="custom-control custom-checkbox custom-control-inline form-group">
              <input
                id="check-d"
                type="checkbox"
                class="custom-control-input form-control"
                name="d">
              <label
                class="custom-control-label form-check-label"
                for="check-d">d</label>
            </div>
            <div class="custom-control custom-checkbox custom-control-inline form-group">
              <input
                id="check-e"
                type="checkbox"
                class="custom-control-input form-control"
                name="e">
              <label
                class="custom-control-label form-check-label"
                for="check-e">e</label>
            </div>
            <br>
            <div class="custom-control custom-checkbox custom-control-inline form-group">
              <input
                id="check-f"
                type="checkbox"
                class="custom-control-input form-control"
                name="f">
              <label
                class="custom-control-label form-check-label"
                for="check-f">f</label>
            </div>
            <div class="custom-control custom-checkbox custom-control-inline form-group">
              <input
                id="check-g"
                type="checkbox"
                class="custom-control-input form-control"
                name="g">
              <label
                class="custom-control-label form-check-label"
                for="check-g">g</label>
            </div>
            <div class="custom-control custom-checkbox custom-control-inline form-group">
              <input
                id="check-h"
                type="checkbox"
                class="custom-control-input form-control"
                name="h">
              <label
                class="custom-control-label form-check-label"
                for="check-h">h</label>
            </div>
            <div class="custom-control custom-checkbox custom-control-inline form-group">
              <input
                id="check-i"
                type="checkbox"
                class="custom-control-input form-control"
                name="h">
              <label
                class="custom-control-label form-check-label"
                for="check-h">i</label>
            </div>
            <div class="custom-control custom-checkbox custom-control-inline form-group">
              <input
                id="check-j"
                type="checkbox"
                class="custom-control-input form-control"
                name="h">
              <label
                class="custom-control-label form-check-label"
                for="check-h">j</label>
            </div>
            <br>
            <button
              type="submit"
              class="btn">查询</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '../components/navbar'
import BreadCrumb from '../../components/breadCrumb'
import Menu from '../components/menu'

export default {
  name: 'LogManagement',
  components: {BreadCrumb, AdminNavbar, Menu},
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin'
      }, {
        text: '日志查询',
        active: true
      }],
      date: new Date(),
      options: {
        format: 'YYYY/MM/DD h:mm:ss',
        useCurrent: true
      }
    }
  }
}
</script>

<style scoped>
  .html {
    height: 100%;
  }

  .navbar {
    min-width: 500px;
  }

  #body {
    display: flex;
    justify-content: space-between;
    min-width: 800px;
    height: calc(100% - 70px);
  }

  #management {
    flex-basis: 100%;
    padding: 0;
  }

  h1 {
    padding-left: 20px;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  .table_div {
    padding-right: 380px;
    padding-left: 20px;
  }

  table {
    text-align: center;
  }

  input {
    width: 180px;
  }

  .col-md-6 {
    align-items: center;
  }

  thead tr {
    align-items: center;
  }

  tr td {
    width: 180px;
  }

  .btn {
    color: white;
    background-color: #8d4e91;
    border-color: #8d6592;
    border-radius: 10px;
    outline: none;
    box-shadow: #8d6592 inset;
  }

  .btn:hover,
  .btn:active {
    background-color: #5e0057;
  }
</style>
