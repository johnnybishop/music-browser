import { createApp } from 'vue'
import App from './App.vue'
import Ads from 'vue-google-adsense'
import ScriptX from 'vue-scriptx'

createApp(App).use(ScriptX).use(Ads.Adsense).mount('#app')
