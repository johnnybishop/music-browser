import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App);
app.mount('#app');

const backendUrl =  'http://localhost:8080/api';

app.config.globalProperties.$backendUrl = backendUrl;
