<template>
  <div>
    <popup-view :visible="editorPopup.show" @close="editorPopup.show=false">
      <json-editor ref="editor" :json="editorContent"
                   v-on:verifyJson="verifyJson" class="full" :onChange="inputResponseJson"></json-editor>
      <div class="button is-primary is-fullwidth bottom-button" v-on:click="editConfirm"
           v-bind:class="{ 'is-disabled': !editorInfo.ok}">
        {{ editorInfo.message }}
      </div>
    </popup-view>
    <div class="tile is-ancestor">
      <article class="tile is-child box">
        <form @submit.prevent="submit">
          <h1 class="title">添加返回模板</h1>
          <div class="block">
            <label class="label">模板名称</label>
            <p class="control has-icon has-icon-right">
              <input v-bind:class="{ 'is-danger': !verifications.name }" class="input" type="text"
                     placeholder="请输入您的模板名称" v-model="template.name" v-on:input="verifications.name=true">
              <span class="icon is-small" v-if="!verifications.name">
               <i class="fa fa-warning"></i>
              </span>
              <span class="help is-danger" v-if="!verifications.name">{{ errorMessage.name }}</span>
            </p>
            <label class="label">MIME 类型</label>
            <p class="control">
              <span class="select">
                <select v-model.trim="template.mimeType">
                  <option value=0>application/json</option>
                </select>
              </span>
            </p>
            <label class="label">备注</label>
            <p class="control">
              <textarea class="textarea" placeholder="请输入您的备注" v-model.trim="template.note"></textarea>
            </p>
            <label class="label">返回数据</label>
            <div class="button is-primary sparrow-button" v-on:click="editorPopup.show=true">编辑</div>
            <pre v-highlightjs="JSON.stringify(JSON.parse(template.responseJson), null, 4)"><code
              class="javascript"></code></pre>
            <div>
              <p class="control right">
                <button class="button is-primary right" type="submit">确认</button>
              </p>
              <p class="blank">
              </p>
            </div>
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

  export default {
    components: {
      JsonEditor,
      PopupView
    },

    props: {},

    data () {
      return {
        template: {
          name: '',
          mimeType: 0,
          note: '',
          responseJson: '{}',
          type: 0
        },
        verifications: {
          name: true
        },
        errorMessage: {
          name: '',
          modal: ''
        },
        editorContent: {},
        editorJson: {},
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
    },

    computed: {},

    methods: {
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
          if (this.isEmpty(this.template[prop])) {
            this.verifications[prop] = false
            this.errorMessage[prop] = '不能为空'
            callback(false)
            return
          }
        }
        // 同名校验
        request('/frontend/res_template/repeat_name_verification', {
          method: 'get',
          params: {
            name: this.template.name
          }
        }).then((response) => {
          var repeatability = response.data['repeatability']
          if (repeatability) {
            this.verifications.name = false
            this.errorMessage.name = '该名称的返回模板已经存在'
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
            var formData = qs.stringify(this.template)
            console.log(this.template)
            request('/frontend/res_template/create', {
              method: 'post',
              data: formData
            }).then((response) => {
              notification.toast({
                message: '创建成功',
                type: 'success',
                duration: 2000
              })
              var model = response.data
              this.$router.push({path: '/template/detail/' + model.res_template_id})
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
        this.template.responseJson = JSON.stringify(this.editorJson, null, 4)
        this.editorContent = this.editorJson
      }
    }
  }
</script>"

<style scoped>
  .blank {
    height: 30px;
    margin-top: 10px;
  }

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
