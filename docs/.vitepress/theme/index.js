import DefaultTheme from 'vitepress/theme'
import Layout from './Layout.vue'
import './style.css'
import HomeFeatures from './components/HomeFeatures.vue'
import ConceptGraphExplorer from './components/ConceptGraphExplorer.vue'

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    app.component('HomeFeatures', HomeFeatures)
    app.component('ConceptGraphExplorer', ConceptGraphExplorer)
  }
}
