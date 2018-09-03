<template>
  <div>
    <div class="tile is-ancestor">
      <article class="tile is-child box">
        <form @submit.prevent="submit">
          <h1 class="title">添加项目</h1>
          <div class="block">
            <label class="label">项目名称</label>
            <p class="control has-icon has-icon-right">
              <input v-bind:class="{ 'is-danger': !verifications.name }" class="input" type="text"
                     placeholder="请输入您的项目名称" v-model="project.name" v-on:input="verifications.name=true">
              <span class="icon is-small" v-if="!verifications.name">
               <i class="fa fa-warning"></i>
              </span>
              <span class="help is-danger" v-if="!verifications.name">{{ errorMessage.name }}</span>
            </p>
            <label class="label">项目权限<span class="regular-font">（创建后可以在『项目设置』中配置可见用户）</span></label>
            <p class="control">
              <span class="select">
                <select v-model.trim="project.permissionType">
                  <option value="0">所有人可见</option>
                  <option value="1">自定义权限</option>
                </select>
              </span>
            </p>
            <label class="label">备注</label>
            <p class="control">
              <textarea class="textarea" placeholder="请输入您的备注" v-model.trim="project.note"></textarea>
            </p>
            <p class="control">
              <button class="button is-primary right" type="submit">确认</button>
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

  export default {
    components: {},

    props: {},

    data () {
      return {
        project: {
          name: '',
          permissionType: 0,
          status: 1,
          note: ''
        },
        verifications: {
          name: true
        },
        errorMessage: {
          name: '',
          modal: ''
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
          if (this.isEmpty(this.project[prop])) {
            this.verifications[prop] = false
            this.errorMessage[prop] = '不能为空'
            callback(false)
            return
          }
        }
        // 同名校验
        request('/frontend/project/repeat_name_verification', {
          method: 'get',
          params: {
            name: this.project.name
          }
        }).then((response) => {
          var repeatability = response.data['repeatability']
          if (repeatability) {
            this.verifications.name = false
            this.errorMessage.name = '该名称的项目已经存在'
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
            var formData = qs.stringify(this.project)
            request('/frontend/project/create', {
              method: 'post',
              data: formData
            }).then((response) => {
              notification.toast({
                message: '创建成功',
                type: 'success',
                duration: 2000
              })
              var model = response.data
              this.$router.push({path: '/project/detail/' + model.project_id})
            }).catch((response) => {
              notification.toast({
                message: response.message,
                type: 'danger',
                duration: 2000
              })
            })
          }
        })
      }
    }
  }
</script>

<style scoped>
  .right {
    float: right;
  }

  .regular-font {
    font-size: 13px;
    font-weight: normal
  }
</style>
