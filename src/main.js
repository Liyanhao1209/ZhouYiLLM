import { createApp, Vue } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'



const app = createApp(App)
//全局异常处理函数
app.config.errorHandler = (err, instance, info) => {
    console.log('err', err)
}
app.use(store).use(router).use(ElementPlus).mount('#app')