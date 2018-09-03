<template>
  <article>
    <div>
      <modal :visible="updateModal.showModal" @close="close">
        <div class="box">
          <article class="media">
            <div class="media-content">
              <div class="content">
                <p>
                  <strong>创建失败</strong>
                  <br>
                  {{ updateModal.message }}
                </p>
              </div>
            </div>
          </article>
        </div>
      </modal>
      <modal :visible="deleteModal.showModal" @close="close">
        <div class="box">
          <article>
            <div class="media-content">
              <div class="content">
                <p>
                  <strong>确认删除 <strong class="is-danger">{{ project.name }}</strong> ？</strong>
                  <br/>
                  删除后该项目内的所有 API 将会被删除
                  <br/>
                  如果您确定删除，请输入该项目的名称，防止误删除
                </p>
                <input v-bind:class="{ 'is-danger': !deleteModalVerification }" class="input" type="text"
                       placeholder="请输入您的项目名称" v-model.trim="deleteModal.inputName">
                <hr class="gradient-red"/>
                <button class="button is-danger is-fullwidth" @click="deleteProject">确认删除</button>
              </div>
            </div>
          </article>
        </div>
      </modal>
      <div class="tile is-ancestor">
        <article class="tile is-child box">
          <form @submit.prevent="updateProject">
            <h1 class="title">更新基本信息</h1>
            <div class="block">
              <label class="label">项目名称</label>
              <p class="control has-icon has-icon-right">
                <input v-bind:class="{ 'is-danger': !verifications.name }" class="input" type="text"
                       placeholder="请输入您的项目名称" v-model.trim="project.name" v-on:input="verifications.name=true">
                <span class="icon is-small" v-if="!verifications.name">
               <i class="fa fa-warning"></i>
              </span>
                <span class="help is-danger" v-if="!verifications.name" value="project.note">{{ errorMessage.name
                  }}</span>
              </p>
              <label class="label">项目权限</label>
              <p class="control">
              <span class="select">
                <select v-model.trim="project.permissionType">
                  <option value="0">所有人可见</option>
                  <option value="1">自定义权限</option>
                </select>
              </span>
              </p>
              <div v-if="project.permissionType == 1">
                <label class="label">成员列表</label>
                <el-select
                  v-model="searchSelect.value"
                  multiple
                  filterable
                  remote
                  reserve-keyword
                  size="small"
                  placeholder="搜索用户"
                  :remote-method="searchAccount"
                  :loading="searchSelect.loading">
                  <el-option
                    v-for="item in searchSelect.options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                  </el-option>
                </el-select>
                <button class="button" type="button" v-on:click="addMembers">添加
                </button>
                <table class="table">
                  <thead>
                  <tr>
                    <th>用户名</th>
                    <th></th>
                  </tr>
                  </thead>
                  <tfoot>
                  <tr>
                    <th></th>
                    <th></th>
                  </tr>
                  </tfoot>
                  <tbody>
                  <tr v-for="member in members" :key="members.id">
                    <td>
                      {{ member.username }}
                    </td>
                    <td>
                      <button class="button is-danger" type="button" v-on:click="deleteMembers(member)">移除
                      </button>
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
              <label class="label">备注</label>
              <p class="control">
                <textarea class="textarea" placeholder="请输入您的备注" v-model.trim="project.note"></textarea>
              </p>
              <div>
                <p class="control right">
                  <button class="button is-primary" type="submit">更新</button>
                </p>
                <p class="blank">
                </p>
              </div>
            </div>
          </form>
          <hr class="gradient-green"/>
          <button class="button is-danger is-fullwidth" v-on:click="deleteModal.showModal = true">删除</button>
        </article>
      </div>
    </div>
  </article>
</template>

<script>
  import qs from 'qs'
  import {Modal} from 'vue-bulma-modal'
  import {request} from '../network.js'
  import * as notification from '../notification.js'
  import {Select} from 'element-ui'

  export default {
    components: {
      Modal,
      Select
    },

    props: {
      project: {
        name: '',
        status: 1,
        permissionType: 0,
        note: ''
      }
    },

    data () {
      return {
        members: [],
        accounts: [],
        updateModal: {
          showModal: false,
          message: ''
        },
        deleteModal: {
          showModal: false,
          inputName: ''
        },
        newData: {
          name: '',
          status: 1,
          note: ''
        },
        verifications: {
          name: true
        },
        errorMessage: {
          name: ''
        },
        searchSelect: {
          options: [],
          value: [],
          loading: false
        }
      }
    },

    created () {
      this.fetchMembers()
    },

    mounted () {
    },

    computed: {
      deleteModalVerification: function () {
        return (this.deleteModal.inputName === this.project.name)
      }
    },

    methods: {
      close () {
        this.deleteModal.showModal = false
        this.updateModal.showModal = false
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
            name: this.project.name,
            project_id: this.project.project_id
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
            type: 'success',
            duration: 2000
          })
        })
      },
      updateProject () {
        this.verify((ok) => {
          if (ok) {
            var formData = qs.stringify(this.project)
            request('/frontend/project/update/' + this.$route.params.id, {
              method: 'post',
              data: formData
            }).then((response) => {
              notification.toast({
                message: '更新成功',
                type: 'success',
                duration: 2000
              })
            }).catch((response) => {
              this.updateModal.message = response.message
              this.updateModal.showModal = true
            })
          }
        })
      },
      deleteProject () {
        if (this.deleteModalVerification === true) {
          request('/frontend/project/delete', {
            method: 'get',
            params: {
              project_id: this.$route.params.id
            }
          }).then((response) => {
            this.close()
            notification.toast({
              message: '删除成功',
              type: 'success',
              duration: 2000
            })
            setTimeout(this.jumpToProjectList, 100)
          }).catch((response) => {
            this.close()
            notification.toast({
              message: response.message,
              type: 'danger',
              duration: 2000
            })
          })
        }
      },
      fetchMembers () {
        request('/frontend/project/' + this.$route.params.id + '/members', {
          method: 'get'
        }).then((response) => {
          this.members = response.data
        }).catch((response) => {
          this.close()
          notification.toast({
            message: response.message,
            type: 'danger',
            duration: 2000
          })
        })
      },
      deleteMembers (member) {
        request('/frontend/project/' + this.$route.params.id + '/members/remove/' + member.id, {
          method: 'get'
        }).then((response) => {
          var index = this.members.indexOf(member)
          this.members.splice(index, 1)
          notification.toast({
            message: '移除成功',
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
      jumpToProjectList () {
        this.$router.push({path: '/project'})
      },
      searchAccount (queryStr) {
        if (queryStr !== '') {
          this.searchSelect.loading = true
          setTimeout(() => {
            request('/frontend/account/search', {
              method: 'get',
              params: {
                'username': queryStr
              }
            }).then((response) => {
              this.searchSelect.options = response.data.map(item => {
                return {value: item['id'], label: item['username']}
              })
              this.searchSelect.loading = false
            }).catch((response) => {
              notification.toast({
                message: response.message,
                type: 'danger',
                duration: 1000
              })
            })
          }, 2000)
        } else {
          this.searchSelect.options = []
        }
      },
      addMembers () {
        request('/frontend/project/' + this.$route.params.id + '/members/add', {
          method: 'get',
          params: {
            'id': this.searchSelect.value
          }
        }).then((response) => {
          this.members = this.mergeMembers(response.data, this.members)
          notification.toast({
            message: '添加成功',
            type: 'success',
            duration: 2000
          })
        }).catch((response) => {
          notification.toast({
            message: response.message,
            type: 'danger',
            duration: 500
          })
        })
      },
      mergeMembers (arr0, arr1) {
        const arr = arr0.concat(arr1)
        let dic = {}
        arr.forEach((item) => {
          dic[item['id']] = item
        })
        var resultArr = []
        for (var prop in dic) {
          resultArr.push(dic[prop])
        }
        return resultArr
      }
    }
  }
</script>

<style scoped>
  .right {
    float: right;
  }

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

  strong.is-danger {
    color: #eb4c64;
  }

  .blank {
    height: 30px;
  }
</style>
