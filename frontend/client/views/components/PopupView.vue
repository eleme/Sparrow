<template>
  <transition
    :name="transition"
    mode="in-out"
    appear
    :appear-active-class="enterClass"
    :enter-active-class="enterClass"
    :leave-active-class="leaveClass"
    @beforeEnter="beforeEnter"
    @afterEnter="afterEnter"
    @beforeLeave="beforeLeave"
    @afterLeave="afterLeave"
  >
    <div :class="classes" v-if="show">
      <div class="modal-background" @click="deactive"></div>
      <div class="modal-container">
        <div class="modal-content">
          <slot></slot>
        </div>
      </div>
      <button class="modal-close" @click="deactive"></button>
    </div>
  </transition>
</template>

<script>
  export default {
    props: {
      card: Boolean,
      visible: Boolean,
      transition: {
        type: String,
        default: 'fade'
      }
    },

    data () {
      return {
        show: this.visible
      }
    },
    mounted () {
      document.body.appendChild(this.$el)
    },
    methods: {
      beforeEnter () {
        this.$emit('open')
      },

      afterEnter () {
        this.$emit('opened')
      },

      beforeLeave () {
        this.$emit('before-close')
      },

      afterLeave () {
        this.$emit('close')
      },

      active () {
        this.show = true
      },

      deactive () {
        this.show = false
      }
    },

    computed: {
      classes () {
        return ['modal', 'animated', 'is-active']
      },
      enterClass () {
        return `${this.transition}In`
      },

      leaveClass () {
        return `${this.transition}Out`
      }
    },

    watch: {
      visible (val) {
        this.show = val
      }
    }
  }
</script>

<style scoped>
  .modal-container {
    width: 80%;
    height: 80%;
  }

  .modal-content {
    width: 100%;
    height: 100%;
    background-color: #FFFFFF;
    border-radius: 5px;
  }

  .modal-background {
    background-color: hsla(0, 0%, 4%, .50);
  }

  .modal-close {
    position: absolute;
    margin: auto;
    top: 0; left: 0; right: 0; bottom: 0;
    overflow: auto;
    margin-bottom: 1%;
  }
</style>
