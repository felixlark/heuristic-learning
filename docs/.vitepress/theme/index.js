import DefaultTheme from 'vitepress/theme'
import './style.css'
import HomeFeatures from './components/HomeFeatures.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('HomeFeatures', HomeFeatures)
  }
}
