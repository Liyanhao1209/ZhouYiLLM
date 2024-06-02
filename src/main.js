import { createApp, Vue } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'vditor/dist/index.css'


const app = createApp(App)



app.use(store).use(router).use(ElementPlus).mount('#app')