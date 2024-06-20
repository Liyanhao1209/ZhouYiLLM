import { createApp, Vue } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import ElementPlus, { ElMessage } from 'element-plus'
import 'element-plus/dist/index.css'
import 'vditor/dist/index.css'
import { request } from './service/authService'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import axios from 'axios'


const app = createApp(App)
const except_path = ['/admin']
router.beforeEach((to, from, next) => {
    // 没有登录状态下只允许访问register 和 login页面
    let logged_in = store.state.logged_in || localStorage.getItem('islogin') == 'true'
    if (except_path.includes(to.path)) {
        next()
    }
    else
        if (!logged_in && to.meta.requireLogin) {
            console.log('main.js:router:', to.name, '没有登录');
            ElMessage({
                message: '请登录',
                type: 'error'
            })
            next({ name: 'login' })
        } else {
            next()
        }
})

request.interceptors.request.use(function (config) {
    if (localStorage.getItem('token') && localStorage.getItem('token') != "")
        config.headers["Authorization"] = "Bearer " + localStorage.getItem('token')
    return config
})

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}


app.use(store).use(router).use(ElementPlus).mount('#app')