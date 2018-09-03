import Notification from 'vue-bulma-notification'
import Vue from 'vue'

const NotificationComponent = Vue.extend(Notification)

export const toast = (propsData = {
  title: '',
  message: '',
  type: '',
  direction: '',
  duration: 4500,
  container: '.notifications'
}) => {
  return new NotificationComponent({
    el: document.createElement('div'),
    propsData
  })
}
