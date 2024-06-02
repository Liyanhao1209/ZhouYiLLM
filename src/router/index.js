import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Layout from "@/Layout/Layout";

const routes = [
  {
    path: '/',
    name: 'Layout',
    component: Layout,
    redirect: "chat",   //重定向，路由自动跳转，输入/自动访问home
    children: [
      {
      path: 'home',
      name: 'home',
      component: HomeView
    },
  
    {
      path: '/login',
      name: 'login',
      component: () => import('@/login.vue')
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('@/views/chat.vue')
    },
    {
      path: '/history_chats',
      name: 'history_chats',
      component: () => import('@/views/history_chats.vue')
    },
    {
      path: '/knowledge_base',
      name: 'knowledge_base',
      component: () => import('@/views/knowledge_base.vue')
    },
  ]
    
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
