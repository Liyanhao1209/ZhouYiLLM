import { createApp, Vue } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'vditor/dist/index.css'


const app = createApp(App)

router.beforeEach((to, from, next) => {
    // 没有登录状态下只允许访问register 和 login页面
    let logged_in = store.state.logged_in || localStorage.getItem('islogin')
    store.state.logged_in = localStorage.getItem('islogin')
    if (!logged_in && to?.meta?.requireLogin) {
        console.log('main.js:router:', to.name, '没有登录');
        next({ name: 'login' })
    } else {
        next()
    }
})

app.use(store).use(router).use(ElementPlus).mount('#app')