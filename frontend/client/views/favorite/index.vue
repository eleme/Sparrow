<template>
  <div>
    <div class="tile is-ancestor">
      <div class="tile is-parent">
        <article class="tile is-child box">
          <h4 class="title">收藏 API 列表</h4>
          <api-list :apis="apisData.apis"></api-list>
          <el-pagination
            layout="prev, pager, next"
            :page-size="apisData.limit"
            :total="apisData.total"
            @current-change="pageChange">
          </el-pagination>
        </article>
      </div>
    </div>
  </div>
</template>

<script>
  import Chart from 'vue-bulma-chartjs'
  import ApiList from '../components/APIList'
  import {request} from '../network.js'
  import * as notification from '../notification.js'
  import { Pagination } from 'element-ui'

  export default {
    components: {
      Chart,
      ApiList,
      Pagination
    },

    data () {
      return {
        apisData: {}
      }
    },

    created () {
      this.loadFavoriteApis(1)
    },

    computed: {},

    methods: {
      loadFavoriteApis (page) {
        request('/frontend/favorite/list', {
          params: {
            current_page: page,
            limit: 10
          }
        })
          .then((response) => {
            this.apisData = response.data
          })
          .catch((response) => {
            notification.toast({
              message: response.message,
              type: 'danger',
              duration: 2000
            })
          })
      },

      pageChange (currentPage) {
        this.loadFavoriteApis(currentPage)
      }
    }
  }
</script>

<style scoped>
</style>
