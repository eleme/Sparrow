<template>
  <div>
    <div class="tile is-ancestor">
      <div class="tile is-parent is-12">
        <article class="tile is-child box">
          <h4 class="title">活跃度</h4>
          <ve-line :data="dailyActiveData"></ve-line>
        </article>
      </div>
    </div>
    <div class="tile is-ancestor">
      <div class="tile is-parent is-6">
        <article class="tile is-child box">
          <h4 class="title">周活跃用户排行</h4>
          <table class="table is-striped">
            <thead>
            <tr>
              <th>排名</th>
              <th>用户名</th>
              <th>访问量</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(info, index) in topActiveActiveUserData" :key="info.user_id">
              <td>
                {{ index + 1 }}
              <td>
                {{ info.username }}
              </td>
              <td>
                {{ info.count }}
              </td>
            </tr>
            </tbody>
          </table>
        </article>
      </div>
      <div class="tile is-parent is-6">
        <article class="tile is-child box">
          <h4 class="title">周 API Mock 排行</h4>
          <table class="table is-striped">
            <thead>
            <tr>
              <th>排名</th>
              <th>API</th>
              <th>Mock 数</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(info, index) in topActiveApisInfo" :key="info.user_id">
              <td>
                {{ index + 1 }}
              <td>
                {{ info.path }}
              </td>
              <td>
                {{ info.count }}
              </td>
            </tr>
            </tbody>
          </table>
        </article>
      </div>
    </div>
  </div>
</template>

<script>
  import Chart from 'vue-bulma-chartjs'
  import VeLine from 'v-charts/lib/line'
  import {request} from '../network.js'
  import * as notification from '../notification.js'

  export default {
    components: {
      Chart,
      VeLine
    },

    data () {
      return {
        dailyActiveData: {
          columns: [],
          rows: []
        },
        topActiveActiveUserData: [],
        topActiveApisInfo: []
      }
    },

    created () {
      request('frontend/action/daily_active', {
        method: 'get'
      }).then((response) => {
        this.dailyActiveData = {
          columns: ['日期', '访问量', 'Mock次数'],
          rows: []
        }
        this.dailyActiveData.rows = response.data
      }).catch((response) => {
        notification.toast({
          message: response.message,
          type: 'danger',
          duration: 2000
        })
      })

      request('frontend/action/top_active_users_info', {
        method: 'get'
      }).then((response) => {
        this.topActiveActiveUserData = response.data
      }).catch((response) => {
        notification.toast({
          message: response.message,
          type: 'danger',
          duration: 2000
        })
      })

      request('frontend/action/top_active_apis_info', {
        method: 'get'
      }).then((response) => {
        this.topActiveApisInfo = response.data
      }).catch((response) => {
        notification.toast({
          message: response.message,
          type: 'danger',
          duration: 2000
        })
      })
    },

    computed: {},

    mounted () {
    }
  }
</script>

<style lang="scss" scoped>
</style>
