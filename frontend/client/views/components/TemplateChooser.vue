<template>
  <div>
    <div class="sparrow-content">
      <h1 class="title">返回模板选择器</h1>
      <div class="block is-flex">
        <tabs animation="slide" :only-fade="false">
          <tab-pane label="公共模板">
            <div class="search">
              <input type="text" placeholder="请输入关键字...">
              <div class="block is-flex">
                <collapse accordion>
                  <collapse-item :title="template.name" v-for="template in templatesData.res_templates"
                                 :key="template.res_template_id">
                    <form>
                      <label class="label">模板名称</label>
                      <p class="control has-icon has-icon-right">
                        {{ template.name }}
                      </p>
                      <label class="label">MIME 类型</label>
                      <div class="control">
                        <div v-if="template.mimeType === 0">
                          application/json
                        </div>
                        <div v-if="template.mimeType === 1">
                          text/plain
                        </div>
                        <div v-if="template.mimeType === 2">
                          image/jpeg
                        </div>
                      </div>
                      <label class="label">备注</label>
                      <p class="control">
                        {{ template.note }}
                      </p>
                      <label class="label">数据内容</label>
                      <p class="control">
                        <pre v-highlightjs="JSON.stringify(JSON.parse(template.responseJson), null, 4)"><code class="javascript"></code></pre>
                      </p>
                      <p class="control">
                        <button class="button is-primary is-fullwidth"
                                v-on:click="chooseTemplate(template)">选择
                        </button>
                      </p>
                    </form>
                  </collapse-item>
                </collapse>
              </div>
              <div class="block">
                <el-pagination
                  layout="prev, pager, next"
                  :page-size="templatesData.limit"
                  :total="templatesData.total"
                  @current-change="pageChange">
                </el-pagination>
              </div>
            </div>
          </tab-pane>
          <tab-pane label="项目内模板">Pictures Tab</tab-pane>
        </tabs>
      </div>
    </div>
  </div>
</template>

<script>
  import JsonEditor from './JsonEditor'
  import {Tabs, TabPane} from 'vue-bulma-tabs'
  import {Collapse, Item as CollapseItem} from 'vue-bulma-collapse'
  import { Pagination } from 'element-ui'
  import 'element-ui/lib/theme-chalk/index.css'
  import {request} from '../network.js'
  import * as notification from '../notification.js'

  export default {
    props: {
    },

    components: {
      JsonEditor,
      Tabs,
      TabPane,
      Collapse,
      CollapseItem,
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
          method: 'get',
          params: {
            current_page: page,
            limit: 5
          }
        }).then((response) => {
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

      chooseTemplate (template) {
        template.responseJson = JSON.parse(template.responseJson)
        this.$emit('choose-template', template)
      },

      pageChange (currentPage) {
        this.loadTemplates(currentPage)
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
