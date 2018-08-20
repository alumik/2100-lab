<template>
  <Basic
    :items="items"
    class="my-basic">
    <div>
      <h1>日志查询</h1>
      <div class="table-div">
        <table class="table">
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
                  v-model="admin_id"
                  type="text"
                  class="form-control">
              </td>
              <td>
                <div class="col-md-6">
                  <date-picker
                    v-model="begin_date"
                    :config="options"/>
                </div>
              </td>
              <td>
                <div class="col-md-6">
                  <date-picker
                    v-model="end_date"
                    :config="options"/>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <h4>查询项目</h4>
      <form class="checkbox-div">
        <b-form-group>
          <b-form-checkbox-group
            id="row1"
            v-model="select1"
            :options="options1"
            name="row1"/>
        </b-form-group>
        <b-form-group>
          <b-form-checkbox-group
            id="row2"
            v-model="select2"
            :options="options2"
            name="row2"/>
        </b-form-group>
      </form>
      <div class="button-group">
        <button
          type="submit"
          class="btn"
          @click="to_detail">查询</button>
      </div>
    </div>
  </Basic>
</template>

<script>
import Basic from '../basic/basic'

export default {
  name: 'LogManagement',
  components: { Basic },
  data () {
    return {
      items: [{
        text: '主页',
        href: '/admin/main'
      }, {
        text: '日志查询',
        active: true
      }],
      begin_date: new Date(),
      end_date: new Date(),
      options: {
        format: 'YYYY/MM/DD h:mm:ss',
        useCurrent: true
      },
      admin_id: '',
      select1: '',
      options1: [
        { text: 'A', value: 'a' },
        { text: 'B', value: 'b' },
        { text: 'C', value: 'c' },
        { text: 'D', value: 'd' },
        { text: 'E', value: 'e' }
      ],
      select2: '',
      options2: [
        { text: 'F', value: 'f' },
        { text: 'G', value: 'g' },
        { text: 'H', value: 'h' },
        { text: 'I', value: 'i' },
        { text: 'J', value: 'j' }
      ],
      page_jump: false
    }
  },
  methods: {
    to_detail: function () {
      this.page_jump = true
      this.$router.push({ name: 'LogDetail',
        query: {
          admin_id: this.admin_id,
          begin_date: Date.parse(this.begin_date) / 1000,
          end_date: Date.parse(this.end_date) / 1000,
          select: this.select1 + ',' + this.select2
        }
      })
    }
  }
}
</script>

<style scoped>
  .my-basic {
    min-width: 700px;
  }

  h1,
  h4 {
    padding-left: 20px;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: left;
  }

  .table-div {
    padding-left: 20px;
  }

  table {
    width: 400px;
    text-align: center;
  }

  input {
    width: 178px;
  }

  .col-md-6 {
    align-items: center;
  }

  tr {
    align-items: center;
  }

  tr td {
    width: 180px;
  }

  .checkbox-div {
    padding-left: 20px;
    text-align: left;
  }

  .button-group {
    display: flex;
    justify-content: flex-start;
    padding-left: 20px;
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
