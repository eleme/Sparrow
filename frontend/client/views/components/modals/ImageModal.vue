<template>
  <div>
    <image-modal :visible="visible" @close="close" transition="roll">
      <p class="image" v-loading="loading"><img :src="imgUrl" class="code-image"></p>
    </image-modal>
  </div>
</template>

<script>
  import {ImageModal} from 'vue-bulma-modal'
  import {Loading} from 'element-ui'

  export default {
    components: {
      ImageModal,
      Loading
    },

    props: {
      visible: Boolean,
      imgUrl: String,
      loading: Boolean
    },

    data () {
      return {}
    },

    create () {
    },

    methods: {
      close () {
        this.visible = false
        this.$emit('close')
      }
    }

  }
</script>

<style lang="scss">
  .code-image {
    width: 100%;
    height: 100%;
  }

  .modal-content, .modal-card {
    width: 500px;
    height: 500px;
  }

</style>
