import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { vScrollReveal } from './directives/scrollReveal'

const app = createApp(App)
app.directive('scroll-reveal', vScrollReveal)
app.use(router)
app.mount('#app')

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => {})
  })
}
