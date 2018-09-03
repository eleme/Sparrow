<template>
  <div class="content has-text-centered">
    <h1 class="is-title is-bold">登录</h1>

    <div class="columns is-vcentered">
      <div class="column is-6 is-offset-3">
        <div class="box">
          <div v-show="error" style="color:red; word-wrap:break-word;">{{ error }}</div>
          <form v-on:submit.prevent="login">
            <label class="label">Email</label>
            <p class="control">
              <input v-model="data.username" class="input" type="text" placeholder="email@example.org">
            </p>
            <label class="label">Password</label>
            <p class="control">
              <input v-model="data.password" class="input" type="password" placeholder="请输入密码">
            </p>
            <hr>
            <p class="control">
              <button type="submit" class="button is-primary is-fullwidth">登录</button>
            </p>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

  import {request} from '../network.js'
  import * as notification from '../notification.js'
  import qs from 'qs'

  export default {

    data () {
      return {
        data: {
          username: null,
          password: null,
          rememberMe: false
        },
        error: null
      }
    },
    mounted () {
    },
    methods: {
      login () {
        var formData = qs.stringify(this.data)
        request('/frontend/account/login', {
          method: 'post',
          data: formData
        }).then((response) => {
          this.$router.push({path: '/project'})
          var accountInfoStr = JSON.stringify(response.data)
          window.localStorage.setItem('accountInfo', accountInfoStr)
        }).catch((data) => {
          notification.toast({
            message: data['message'],
            type: 'danger',
            duration: 2000
          })
        })
      }
    }
  }
</script>

<style lang="scss" scoped>
  .is-title {
    text-transform: capitalize;
  }
</style>
