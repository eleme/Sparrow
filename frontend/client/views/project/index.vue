<template>
  <div>
    <div class="bar">
      <router-link class="is-3" :to="{ path: '/project/create'}">
        <button class="button is-primary">添加</button>
      </router-link>
    </div>

    <div class="tile is-ancestor" v-for="(project, index) in projectsData.projects" v-if="index % 4 === 0">
      <router-link class="tile is-parent is-3" :to="{ path: 'detail/'+projectsData.projects[index].project_id}" append
                   v-if="index < projectsData.projects.length">
        <article class="tile is-child box">
          <h4 class="title">{{ projectsData.projects[index].name }}</h4>
          <div class="note">{{ projectsData.projects[index].note }}</div>
        </article>
      </router-link>
      <router-link class="tile is-parent is-3" :to="{ path: 'detail/'+projectsData.projects[index + 1].project_id}"
                   append
                   v-if="index + 1 < projectsData.projects.length">
        <article class="tile is-child box">
          <h4 class="title">{{ projectsData.projects[index + 1].name }}</h4>
          <div class="note">{{ projectsData.projects[index + 1].note }}</div>
        </article>
      </router-link>
      <router-link class="tile is-parent is-3" :to="{ path: 'detail/'+projectsData.projects[index + 2].project_id}"
                   append
                   v-if="index + 2 < projectsData.projects.length">
        <article class="tile is-child box">
          <h4 class="title">{{ projectsData.projects[index + 2].name }}</h4>
          <div class="note">{{ projectsData.projects[index + 2].note }}</div>
        </article>
      </router-link>
      <router-link class="tile is-parent is-3" :to="{ path: 'detail/'+projectsData.projects[index + 3].project_id}"
                   append
                   v-if="index + 3 < projectsData.projects.length">
        <article class="tile is-child box">
          <h4 class="title">{{ projectsData.projects[index + 3].name }}</h4>
          <div class="note">{{ projectsData.projects[index + 3].note }}</div>
        </article>
      </router-link>
    </div>
    <div class="pagecontrol right">
      <el-pagination
        layout="prev, pager, next"
        :page-size="projectsData.limit"
        :total="projectsData.total"
        @current-change="pageChange">
      </el-pagination>
    </div>
  </div>
</template>

<script>
  import Chart from 'vue-bulma-chartjs'
  import {request} from '../network.js'
  import * as notification from '../notification.js'
  import { Pagination } from 'element-ui'

  export default {
    components: {
      Chart,
      Pagination
    },

    data () {
      return {
        hello: 'hello',
        projectsData: {
          total: 0,
          current_page: 0,
          limit: 0,
          projects: []
        }
      }
    },

    created () {
      this.loadProjects(1)
    },

    computed: {},

    methods: {
      loadProjects (page) {
        request('/frontend/project/list', {
          params: {
            current_page: page,
            limit: 12
          }
        })
          .then((response) => {
            this.projectsData = response.data
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
        this.loadProjects(currentPage)
      }
    }
  }
</script>

<style scoped>
  .right {
    float: right;
  }

  .bar {
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .note {
    height: 80px;
  }

  .pagecontrol {
    background: #FFFFFF;
  }
</style>
