<template>
  <section class="hero is-bold app-navbar animated" :class="{ slideInDown: show, slideOutDown: !show }">
    <div class="hero-head">
      <nav class="nav">
        <div class="nav-left">
          <a class="nav-item is-hidden-tablet" @click="toggleSidebar({opened: !sidebar.opened})">
            <i class="fa fa-bars" aria-hidden="true" v-show="!sidebar.hidden"></i>
          </a>
        </div>
        <div class="nav-center">
          <a class="nav-item hero-brand" href="/">
            <img src="~assets/logo.svg" :alt="pkginfo.description">
            <tooltip :label="'v' + pkginfo.version" placement="right" type="success" size="small" :no-animate="true"
                     :always="true" :rounded="true">
              <div class="is-hidden-mobile">
                <span class="vue">S</span><strong class="admin">parrow</strong>
              </div>
            </tooltip>
          </a>
        </div>
        <div class="nav-right is-flex">
          <!--<router-link v-if="!$auth.check()" to="/login" class="nav-item">登录</router-link>-->
          <!--<a v-if="$auth.check()" @click="logout" class="nav-item">Logout</a>-->
          <p class="nav-item" v-if="account.status">
            <button class="button is-primary" type="submit" @click="openModalImage">客户端扫码登录</button>
          </p>
          <router-link to="/login" class="nav-item" v-if="!account.status">登录</router-link>
          <p class="nav-item" v-if="account.status">{{ accountInfo.username }}</p>
          <p v-on:click="logout" class="nav-item" v-if="account.status">注销</p>
        </div>
      </nav>
    </div>
  </section>
</template>

<script>
  import Vue from 'vue'
  import Tooltip from 'vue-bulma-tooltip'
  import {mapGetters, mapActions} from 'vuex'
  import {request} from '../../views/network.js'
  import * as notification from '../../views/notification.js'
  import {Tooltip as ElementTooltip} from 'element-ui'
  import Modal from '../../views/components/modals/Modal'
  import ImageModal from '../../views/components/modals/ImageModal'
  import QRCode from 'qrcode'

  const ImageModalComponent = Vue.extend(ImageModal)

  const openImageModal = (propsData = {
    visible: true,
    imgUrl: this.quickLoginUrl
  }) => {
    return new ImageModalComponent({
      el: document.createElement('div'),
      propsData
    })
  }

  export default {

    components: {
      Tooltip,
      ElementTooltip,
      Modal,
      QRCode
    },

    props: {
      show: Boolean
    },

    computed: mapGetters({
      pkginfo: 'pkg',
      sidebar: 'sidebar'
    }),

    data () {
      return {
        account: {
          name: '',
          status: false
        },
        accountInfo: {
          id: '',
          username: '',
          email: ''
        }
      }
    },

    created () {
      request('/frontend/account/check_status', {
        method: 'get'
      }).then((response) => {
        this.account.status = true
      }).catch((response) => {
        this.account.status = false
      })
      try {
        var accountInfoStr = window.localStorage.getItem('accountInfo')
        this.accountInfo = JSON.parse(accountInfoStr)
      } catch (err) {
      }
    },

    methods: {
      ...mapActions([
        'toggleSidebar'
      ]),
      logout () {
        request('/frontend/account/logout', {
          method: 'post'
        }).then((response) => {
          this.account.status = false
          window.localStorage.clear()
          this.$router.push({path: '/login'})
        }).catch((response) => {
          notification.toast({
            message: response.message,
            type: 'danger',
            duration: 2000
          })
        })
      },
      openModalImage () {
        const imageModal = openImageModal()
        imageModal.loading = true
        var baseUrl = window.location.protocol + '//' + window.location.host
        this.requestQRCode(baseUrl, imageModal, this.accountInfo)
        var updateQRCodeInterval = setInterval(() => {
          if (imageModal.visible) {
            imageModal.loading = true
            this.requestQRCode(baseUrl, imageModal, this.accountInfo)
          } else {
            clearInterval(updateQRCodeInterval)
          }
        }, 60000)
      },
      requestQRCode (baseUrl, imageModal, accountInfo) {
        request('/frontend/account/request_quick_login', {
          method: 'get'
        }).then((response) => {
          var verificationCode = response.data.verification_code
          var url = baseUrl + '/frontend/account/quick_login' + '?' +
            'verification_code=' + verificationCode + '&' +
          'user_id=' + accountInfo.id
          QRCode.toDataURL(url)
            .then(url => {
              imageModal.imgUrl = url
              imageModal.loading = false
              imageModal.$children[0].active()
            })
            .catch(err => {
              console.error(err)
            })
        }).catch((response) => {
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

<style lang="scss">
  @import '~bulma/sass/utilities/variables';

  .app-navbar {
    position: fixed;
    min-width: 100%;
    z-index: 1024;
    box-shadow: 0 2px 3px rgba(17, 17, 17, 0.1), 0 0 0 1px rgba(17, 17, 17, 0.1);

    .container {
      margin: auto 10px;
    }

    .nav-right {
      align-items: stretch;
      align-items: stretch;
      flex: 1;
      justify-content: flex-end;
      overflow: hidden;
      overflow-x: auto;
      white-space: nowrap;
    }

    .nav-bar-button {
      background-color: #5aceb3;
      border-color: #5aceb3;
    }
  }

  .hero-brand {
    .vue {
      margin-left: 10px;
      color: #36AC70;
    }
    .admin {
      color: #28374B;
    }
  }
</style>
