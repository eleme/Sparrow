<template>
  <div>
    <div class="bar">
      <router-link class="is-3" :to="{ path: '/template/create'}">
        <button class="button is-primary">添加</button>
      </router-link>
    </div>

    <div class="tile is-ancestor" v-for="(template, index) in templatesData.res_templates" v-if="index % 3 === 0">
      <router-link class="tile is-parent is-4"
                   :to="{ path: 'detail/'+templatesData.res_templates[index].res_template_id}" append
                   v-if="index < templatesData.res_templates.length">
        <article class="tile is-child box">
          <h4 class="title">{{ templatesData.res_templates[index].name }}</h4>
          <div class="note">{{ templatesData.res_templates[index].note }}</div>
        </article>
      </router-link>
      <router-link class="tile is-parent is-4"
                   :to="{ path: 'detail/'+templatesData.res_templates[index + 1].res_template_id}" append
                   v-if="index + 1 < templatesData.res_templates.length">
        <article class="tile is-child box">
          <h4 class="title">{{ templatesData.res_templates[index + 1].name }}</h4>
          <div class="note">{{ templatesData.res_templates[index + 1].note }}</div>
        </article>
      </router-link>
      <router-link class="tile is-parent is-4"
                   :to="{ path: 'detail/'+templatesData.res_templates[index + 2].res_template_id}" append
                   v-if="index + 2 < templatesData.res_templates.length">
        <article class="tile is-child box">
          <h4 class="title">{{ templatesData.res_templates[index + 2].name }}</h4>
          <div class="note">{{ templatesData.res_templates[index + 2].note }}</div>
        </article>
      </router-link>
    </div>

    <div class="pagecontrol right">
      <el-pagination
        layout="prev, pager, next"
        :page-size="templatesData.limit"
        :total="templatesData.total"
        @current-change="pageChange">
      </el-pagination>
    </div>
  </div>
</template>

<script>
  import {request} from '../network.js'
  import * as notification from '../notification.js'
  import { Pagination } from 'element-ui'

  export default {
    components: {
      Pagination
    },

    data () {
      return {
        templatesData: {
          total: 0,
          current_page: 0,
          limit: 0,
          res_templates: []
        }
      }
    },

    created () {
      this.loadTemplates(1)
    },

    computed: {},

    methods: {
      loadTemplates (page) {
        request('/frontend/res_template/list', {
          params: {
            current_page: page,
            limit: 9
          }
        })
          .then((response) => {
            this.templatesData = response.data
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
        this.loadTemplates(currentPage)
      }
    }
  }
</script>

<style scoped>
  .bar {
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .note {
    height: 80px;
  }

  .right {
    float: right;
  }

  .pagecontrol {
    background: #FFFFFF;
  }
</style>
