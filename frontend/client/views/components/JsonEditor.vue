<template>
  <div ref="jsoneditor">
  </div>
</template>

<script>
  import JSONEditor from 'jsoneditor'
  import 'jsoneditor/dist/jsoneditor.min.css'

  export default {
    data () {
      return {
        editor: null
      }
    },
    props: {
      json: {
        required: true
      },
      editable: {
        type: Boolean,
        default: () => {
          return true
        }
      },
      options: {
        type: Object,
        default: () => {
          return {}
        }
      },
      onChange: {
        type: Function
      }
    },
    watch: {
      json: {
        handler (newJson) {
          if (this.editor) {
            this.editor.set(newJson)
          }
        },
        deep: true
      }
    },
    created () {
    },
    methods: {
      _onChange () {
        if (this.onChange && this.editor) {
          try {
            this.$emit('verifyJson', true)
            this.onChange(this.editor.get())
          } catch (err) {
            this.$emit('verifyJson', false)
          }
        }
      },
      _editable (node) {
        if (!node.path) {
          return this.editable
        }
      }
    },
    mounted () {
      const container = this.$refs.jsoneditor
      var options = {
        mode: 'code',
        modes: ['code', 'view'], // allowed modes
        onError: function (err) {
          console.log(err.toString())
        },
        onEditable: this._editable,
        onModeChange: function (newMode, oldMode) {
          console.log('Mode switched from', oldMode, 'to', newMode)
        },
        onChange: this._onChange
      }
      this.editor = new JSONEditor(container, options)
      this.editor.set(this.json)
    },
    beforeDestroy () {
      if (this.editor) {
        this.editor.destroy()
        this.editor = null
      }
    }
  }
</script>

<style>

</style>
