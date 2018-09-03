<template>
  <div>
    <popup-view :visible="editorPopup.show" @close="editorPopup.show=false">
      <json-editor ref="editor" :json="editorContent"
                   v-on:verifyJson="verifyJson" class="full" :onChange="inputResponseJson"></json-editor>
      <div class="button is-primary is-fullwidth bottom-button" v-on:click="editConfirm"
           v-bind:class="{ 'is-disabled': !editorInfo.ok}">
        {{ editorInfo.message }}
      </div>
    </popup-view>s
    <popup-view :visible="templateChooser.show" @close="templateChooser.show=false">
      <template-chooser @choose-template="chooseTemplate"></template-chooser>
    </popup-view>
    <div class="tile is-ancestor">
      <article class="tile is-child box">
        <form @submit.prevent="submit">
          <h1 class="title">更新 API</h1>
          <div class="block">
            <label class="label">请求路径</label>
            <p class="control has-icon has-icon-right">
              <input v-bind:class="{ 'is-danger': !verifications.path }" class="input" type="text"
                     placeholder="输入您的 API 相对路径，先不要 / 开头" v-model.trim="api.path" v-on:input="inputingApiPath">
              <span class="icon is-small" v-if="!verifications.path">
               <i class="fa fa-warning"></i>
              </span>
              <span class="help is-danger" v-if="!verifications.path">{{ errorMessage.path }}</span>
            </p>
            <label class="label">请求类型</label>
            <p class="control">
              <span class="select">
                <select v-model.trim="api.method">
                  <option>GET</option>
                  <option>POST</option>
                  <option>PUT</option>
                  <option>DELETE</option>
                  <option>PATCH</option>
                </select>
              </span>
            </p>
            <label class="label">请求名称</label>
            <p class="control has-icon has-icon-right">
              <input v-bind:class="{ 'is-danger': !verifications.name }" class="input" type="text"
                     placeholder="请求名称可以方便您快速找到 API" v-model="api.name" v-on:input="verifications.name=true">
              <span class="icon is-small" v-if="!verifications.name">
               <i class="fa fa-warning"></i>
              </span>
              <span class="help is-danger" v-if="!verifications.name">{{ errorMessage.name }}</span>
            </p>
            <label class="label">状态</label>
            <p class="control">
              <span class="select">
                <select v-model.trim="api.status">
                  <option value="1">Mocking</option>
                  <option value="0">Disabled</option>
                </select>
              </span>
            </p>

            <label class="label">备注</label>
            <p class="control">
              <textarea class="textarea" placeholder="请输入您的备注" v-model.trim="api.note"></textarea>
            </p>

            <label class="label">返回数据</label>
            <div class="button is-primary sparrow-button" v-on:click="editorPopup.show=true">直接编辑</div>
            <div class="button is-info sparrow-button" v-on:click="templateChooser.show=true">从模板中选择</div>
            <pre v-highlightjs="JSON.stringify(JSON.parse(api.responseJson), null, 4)"><code class="javascript"></code></pre>
            <p class="control">
              <button class="button is-primary right" type="submit">更新</button>
            </p>
          </div>
        </form>
      </article>
    </div>
  </div>
</template>

<script>
  import qs from 'qs'
  import {request} from '../network.js'
  import * as notification from '../notification.js'
  import JsonEditor from '../components/JsonEditor'
  import PopupView from '../components/PopupView'
  import TemplateChooser from '../components/TemplateChooser'

  export default {
    components: {
      JsonEditor,
      PopupView,
      TemplateChooser
    },

    data () {
      return {
        api: {
          path: '',
          method: 'GET',
          name: '',
          status: 1,
          note: '',
          responseJson: '{}' // string 类型
        },
        verifications: {
          path: true,
          name: true
        },
        errorMessage: {
          path: '',
          name: ''
        },
        editorJson: {}, // json 类型
        editorContent: {},
        templateChooser: {
          show: false
        },
        editorPopup: {
          show: false
        },
        editorInfo: {
          ok: true,
          message: '确认'
        }
      }
    },

    created () {
      this.loadApi()
    },

    computed: {},

    methods: {
      inputingApiPath () {
        this.verifications.path = true
        if (this.api.path.indexOf('/', 0) === 0) {
          this.api.path = this.api.path.substring(1, this.api.path.length)
        }
      },

      chooseTemplate (template) {
        this.templateChooser.show = false
        // 公共模板不和 API 关联，仅仅内容赋值
        this.editorJson = template.responseJson
        this.api.responseJson = JSON.stringify(template.responseJson, null, 4)
      },

      loadApi () {
        request('/frontend/project/' + this.$route.params.project_id + '/api/detail/' + this.$route.params.api_id, {
          method: 'get'
        }).then((response) => {
          this.api = response.data
          this.editorJson = JSON.parse(this.api.responseJson)
          this.editorContent = this.editorJson
        }).catch((response) => {
          notification.toast({
            message: response.message,
            type: 'danger',
            duration: 2000
          })
        })
      },

      isEmpty (obj) {
        if (obj.length === 0 || obj.length === '' || obj === null) {
          return true
        } else {
          return false
        }
      },
      verify (callback) {
        // 校验空串
        for (var prop in this.verifications) {
          if (this.isEmpty(this.api[prop])) {
            this.verifications[prop] = false
            this.errorMessage[prop] = '不能为空'
            callback(false)
            return
          }
        }

        // 同名校验
        request('/frontend/project/' + this.$route.params.project_id + '/api/repeat_name_verification', {
          method: 'get',
          params: {
            path: this.api.path,
            method: this.api.method,
            api_id: this.api.api_id
          }
        }).then((response) => {
          var repeatability = response.data['repeatability']
          if (repeatability) {
            this.verifications.path = false
            this.errorMessage.path = '该路径的 API 已经存在'
            callback(false)
          }
          var finalResult = true
          for (var value in this.verifications) {
            if (this.verifications[value] === false) {
              finalResult = false
            }
          }
          callback(finalResult)
        }).catch((response) => {
          notification.toast({
            message: response.message,
            type: 'danger',
            duration: 2000
          })
        })
      },

      submit () {
        this.verify((ok) => {
          if (ok) {
            var formData = qs.stringify(this.api)

            request('/frontend/project/' + this.$route.params.project_id + '/api/update/' + this.$route.params.api_id, {
              method: 'post',
              data: formData
            }).then((response) => {
              notification.toast({
                message: '更新成功',
                type: 'success',
                duration: 2000
              })
              this.$router.push({path: '/project/' + this.$route.params.project_id + '/api/detail/' + this.$route.params.api_id})
            }).catch((response) => {
              notification.toast({
                message: response.message,
                type: 'danger',
                duration: 2000
              })
            })
          }
        })
      },

      inputResponseJson (newVal) {
        this.editorJson = newVal
      },

      verifyJson (verification) {
        if (verification) {
          this.editorInfo.message = '确定'
        } else {
          this.editorInfo.message = '格式错误'
        }
        this.editorInfo.ok = verification
      },
      editConfirm () {
        this.editorPopup.show = false
        this.api.responseJson = JSON.stringify(this.editorJson, null, 4)
        this.editorContent = this.editorJson
      }
    }
  }
</script>

<style scoped>
  .right {
    float: right;
  }

  .sparrow-button {
    margin-top: 10px;
    margin-bottom: 20px;
  }

  .full {
    width: 100%;
    position: absolute;
    bottom: 35px;
    top: 0px;
  }

  .bottom-button {
    position: absolute;
    bottom: 0px;
    height: 35px;
  }
</style>
