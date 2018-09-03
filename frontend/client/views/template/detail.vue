<template>
  <div>
    <modal :visible="deleteTemplateModal.showModal" @close="close">
      <div class="box">
        <article>
          <div class="media-content">
            <div class="content">
              <p>
                <strong>删除该模板 <strong class="is-danger">{{ template.name }}</strong> ？</strong>
              </p>
              <button class="button is-danger is-fullwidth" @click="deleteTemplate">确认删除</button>
            </div>
          </div>
        </article>
      </div>
    </modal>
    <article class="tile is-child box">
      <h1 class="title">{{ template.name }}
      </h1>
      <div class="block">
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">MIME 类型</label>
          </div>
          <div class="control is-grouped" v-if="template.mimeType === 0">
            application/json
          </div>
          <div class="control is-grouped" v-if="template.mimeType === 1">
            text/plain
          </div>
          <div class="control is-grouped" v-if="template.mimeType === 2">
            image/jpeg
          </div>
        </div>
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">返回参数</label>
          </div>
          <div class="control">
            <pre v-highlightjs="JSON.stringify(template.responseJson, null, 4)" class="editor"><code class="javascript"></code></pre>
          </div>
        </div>
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">备注</label>
          </div>
          <div class="control">
            <textarea class="textarea" v-model="template.note" disabled></textarea>
          </div>
        </div>
        <div>
          <p class="control right">
            <button class="button is-primary" v-on:click="jumpToTemplateUpdate">编辑</button>
          </p>
          <p class="control right">
            <button class="button is-danger" v-on:click="deleteTemplateModal.showModal=true">删除</button>
          </p>
          <p class="blank">
          </p>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
  import {request} from '../network.js'
  import * as notification from '../notification.js'
  import JsonEditor from '../components/JsonEditor'
  import {Modal} from 'vue-bulma-modal'

  export default {
    components: {
      JsonEditor,
      Modal
    },

    data () {
      return {
        template: {
          name: '',
          mimeType: 0,
          note: '',
          responseJson: ''
        },
        deleteTemplateModal: {
          showModal: false
        }
      }
    },

    created () {
      this.loadTemplate()
    },

    computed: {},

    methods: {
      close () {
        this.deleteTemplateModal.showModal = false
      },

      loadTemplate () {
        request('/frontend/res_template/detail/' + this.$route.params.id, {
          method: 'get',
          params: {
            isOriginal: true
          }
        }).then((response) => {
          this.template = response.data
        }).catch((response) => {
          notification.toast({
            message: response.message,
            type: 'danger',
            duration: 2000
          })
        })
      },

      deleteTemplate () {
        request('/frontend/res_template/delete/' + this.$route.params.id, {
          method: 'get'
        }).then((response) => {
          this.close()
          notification.toast({
            message: '删除成功',
            type: 'success',
            duration: 2000
          })
          setTimeout(this.jumpToTemplateList, 100)
        }).catch((response) => {
          this.close()
          notification.toast({
            message: response.message,
            type: 'danger',
            duration: 2000
          })
        })
      },

      jumpToTemplateList () {
        this.$router.push({path: '/template'})
      },

      jumpToTemplateUpdate () {
        this.$router.push({path: '/template/update/' + this.$route.params.id})
      }
    }
  }
</script>

<style scoped>
  hr.gradient-green {
    border: 0;
    height: 1px;
    background: #333;
    background-image: linear-gradient(to right, #ddd, #5eceb3, #ddd);
    margin-top: 40px;
    margin-bottom: 40px;
  }

  hr.gradient-red {
    border: 0;
    height: 1px;
    background: #333;
    background-image: linear-gradient(to right, #ddd, #eb4c64, #ddd);
    margin-top: 40px;
    margin-bottom: 40px;
  }

  .right {
    float: right;
  }

  .title {
    font-weight: bold;
  }

  .jsoneditor {
    width: 100%;
  }

  .blank {
    height: 30px;
  }

  .button {
    width: 80px;
    margin-left: 10px;
  }

  .editor {
    width: 100%;
  }
</style>
