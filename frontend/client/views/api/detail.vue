<template>
  <div>
    <popup-view :visible="templateChooser.show" @close="templateChooser.show=false">
      <project-chooser @choose-project="chooseProject"></project-chooser>
    </popup-view>
    <modal :visible="deleteAPIModal.showModal" @close="close">
      <div class="box">
        <article>
          <div class="media-content">
            <div class="content">
              <p>
                <strong>删除该 API <strong class="is-danger">{{ api.name }}</strong> ？</strong>
              </p>
              <button class="button is-danger is-fullwidth" @click="deleteAPI">确认删除</button>
            </div>
          </div>
        </article>
      </div>
    </modal>
    <article class="tile is-child box">
      <h1 class="title">{{ api.path }}
        <a :href="mockLink" target="_blank">[MOCK]</a>
        <button class="right icon" v-on:click="starAPI">
          <i :class="{ 'fa-heart-o': !api.star, ' fa-heart': api.star }" class="fa"></i>
        </button>
      </h1>
      <div class="block">
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">请求类型</label>
          </div>
          <div class="control is-grouped">
            {{ api.method }}
          </div>
        </div>
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">请求名称</label>
          </div>
          <div class="control">
            {{ api.name }}
          </div>
        </div>
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">状态</label>
          </div>
          <div class="control">
            <a class="button is-active is-primary" v-if="api.status == 1">Mocking</a>
            <a class="button is-active" v-if="api.status == 0">Disabled</a>
          </div>
        </div>
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">备注</label>
          </div>
          <div class="control">
            <textarea class="textarea" v-model="api.note" disabled></textarea>
          </div>
        </div>
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">请求参数</label>
          </div>
          <div class="control">
            <textarea class="textarea" disabled></textarea>
          </div>
        </div>
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">返回参数</label>
          </div>
          <div class="control">
            <pre v-highlightjs="JSON.stringify(api.responseJson, null, 4)" class="editor"><code
              class="javascript"></code></pre>
          </div>
        </div>
        <div>
          <p class="control right">
            <button class="button is-primary" v-on:click="showProjectChooser">复制</button>
          </p>
          <p class="control right">
            <button class="button is-primary" v-on:click="jumpToAPIUpdate">编辑</button>
          </p>
          <p class="control right">
            <button class="button is-danger" v-on:click="deleteAPIModal.showModal=true">删除</button>
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
  import VbSwitch from 'vue-bulma-switch'
  import PopupView from '../components/PopupView'
  import ProjectChooser from '../components/ProjectChooser'

  export default {
    components: {
      JsonEditor,
      Modal,
      VbSwitch,
      ProjectChooser,
      PopupView
    },

    data () {
      return {
        api: {
          path: '',
          method: 'GET',
          name: '',
          status: 1,
          note: '',
          responseJson: '',
          star: false
        },
        deleteAPIModal: {
          showModal: false
        },
        mockStatus: true,
        shouldRequestUpdateStatus: false,
        templateChooser: {
          show: false
        }
      }
    },

    created () {
      this.loadApi()
    },

    computed: {
      mockLink: function () {
        return 'http://' + window.location.host + '/mock/' + this.$route.params.project_id + '/' + this.api.path
      }
    },

    watch: {
      mockStatus: function (val) {
        if (val === true) {
          this.api.status = 1
        } else {
          this.api.status = 0
        }
        if (this.shouldRequestUpdateStatus === false) {
          this.shouldRequestUpdateStatus = true
        } else {
          this.updateStatus(this.api.status)
        }
      }
    },

    methods: {
      close () {
        this.deleteAPIModal.showModal = false
      },

      updateStatus (status) {
        request('/frontend/project/' + this.$route.params.project_id + '/api/' + this.$route.params.api_id + '/update_status', {
          method: 'get',
          params: {
            status: status
          }
        }).then((response) => {
          notification.toast({
            message: '更新 API 成功',
            type: 'success',
            duration: 2000
          })
        }).catch((response) => {
          notification.toast({
            message: response.message,
            type: 'danger',
            duration: 2000
          })
        })
      },

      loadApi () {
        request('/frontend/project/' + this.$route.params.project_id + '/api/detail/' + this.$route.params.api_id, {
          method: 'get',
          params: {
            isOriginal: false
          }
        }).then((response) => {
          this.api = response.data
          this.mockStatus = this.api.status === 1
        }).catch((response) => {
          notification.toast({
            message: response.message,
            type: 'danger',
            duration: 2000
          })
        })
      },

      deleteAPI () {
        request('/frontend/project/' + this.$route.params.project_id + '/api/delete/' + this.$route.params.api_id)
          .then((response) => {
            this.deleteAPIModal.showModal = false
            notification.toast({
              message: '删除成功',
              type: 'success',
              duration: 2000
            })
            setTimeout(this.jumpToAPIList, 100)
          })
          .catch((response) => {
            notification.toast({
              message: response.message,
              type: 'danger',
              duration: 2000
            })
          })
      },

      jumpToAPIUpdate () {
        this.$router.push({path: '/project/' + this.$route.params.project_id + '/api/update/' + this.$route.params.api_id})
      },

      jumpToAPIList () {
        this.$router.push({path: '/project/detail/' + this.$route.params.project_id})
      },

      starAPI () {
        request('/frontend/project/' + this.$route.params.project_id + '/api/star/' + this.$route.params.api_id, {
          method: 'get'
        }).then((response) => {
          var message = ''
          this.api.star = !this.api.star
          if (this.api.star === true) {
            message = '收藏成功'
          } else {
            message = '取消收藏成功'
          }
          notification.toast({
            message: message,
            type: 'success',
            duration: 2000
          })
        }).catch((response) => {
          notification.toast({
            message: response.message,
            type: 'danger',
            duration: 2000
          })
        })
      },

      showProjectChooser () {
        this.templateChooser.show = true
      },

      chooseProject (project) {
        request('/frontend/api/copy/' + this.api.api_id, {
          method: 'get',
          params: {
            target_project_id: project.project_id
          }
        }).then((response) => {
          this.templateChooser.show = false
          notification.toast({
            message: '复制成功',
            type: 'success',
            duration: 2000
          })
        })
          .catch((response) => {
            this.templateChooser.show = false
            notification.toast({
              message: response.message,
              type: 'danger',
              duration: 2000
            })
          })
      }
    }
  }
</script>

<style scoped>
  .title {
    font-weight: bold;
  }

  .blank {
    height: 30px;
  }

  .right {
    float: right;
  }

  .button {
    width: 80px;
    margin-left: 10px;
  }

  .icon {
    outline: none;
    width: 45px;
    height: 45px;
    border: 0px;
    -webkit-tap-highlight-color: transparent;
  }

  .editor {
    width: 100%;
  }
</style>
