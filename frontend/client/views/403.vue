<template>
  <div class="content has-text-centered">
    <p>
      <img width="200" src="~assets/logo.svg" :alt="description">
    </p>

    <h1 class="is-title is-bold">Oops!</h1>
    <h2 class="is-title is-bold">Oops!你没有权限去该页面</h2>

    <p>你可以：</p>
    <ul>
      <li>
        <router-link class="is-3" :to="{ path: '/home'}">
          回首页
        </router-link>
      </li>
      <li>
        <router-link class="is-3" :to="{ path: '/project'}">
          回到项目列表
        </router-link>
      </li>
    </ul>


  </div>
</template>

<script>
  export default {

    data () {
      return this.$store.state.pkg
    }

  }
</script>

<style lang="scss" scoped>
  .is-title {
    text-transform: capitalize;
  }
</style>
