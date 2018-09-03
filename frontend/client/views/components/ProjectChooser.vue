<template>
  <div>
    <div class="sparrow-content">
      <h1 class="title">项目选择器</h1>
      <div id="ApiList">
        <div class="tile is-ancestor">
          <div class="tile is-parent">
            <table class="table">
              <thead>
              <tr>
                <th>项目名称</th>
                <th>备注</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="project in projectsData.projects" :key="project.project_id"
                  v-on:click="chooseProject(project)">
                <td>{{ project.name }}</td>
                <td>{{ project.note }}</td>
              </tr>
              </tbody>
              <tfoot>
              <tr>
                <th>项目名称</th>
                <th>备注</th>
              </tr>
              </tfoot>
            </table>
          </div>
        </div>
      </div>
      <div class="block">
        <el-pagination
          layout="prev, pager, next"
          :page-size="projectsData.limit"
          :total="projectsData.total"
          @current-change="pageChange">
        </el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
  import {Pagination} from 'element-ui'
  import 'element-ui/lib/theme-chalk/index.css'
  import {request} from '../network.js'
  import * as notification from '../notification.js'

  export default {
    props: {},

    components: {
      Pagination
    },

    data () {
      return {
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
          method: 'get',
          params: {
            current_page: page,
            limit: 5
          }
        }).then((response) => {
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
      chooseProject (project) {
        this.$emit('choose-project', project)
      },
      pageChange (currentPage) {
        this.loadProjects(currentPage)
      }
    }
  }
</script>

<style scoped>

  .sparrow-content {
    margin: 20px;
  }

  .search input {
    outline: none;
    width: 100%;
    height: 42px;
    padding-left: 13px;
    background-color: #FFFFFF;
    border-radius: 5px;
    border: 1px solid #DDDDDD;
  }

  .search input:focus {
    color: #555555;
    border: 1px solid #5aceb3;
  }

</style>
