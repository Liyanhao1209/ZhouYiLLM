import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Layout from "@/Layout/Layout";

const routes = [
  {

    path: '/login',
    name: 'login',
    component: () => import('@/login.vue')
  }, 
  {
    path: '/',
    name: 'Layout',
    component: Layout,
    redirect: "login",   //重定向，路由自动跳转，输入/自动访问home
    children: [
      {
        path: 'home',
        name: 'home',
        component: HomeView
      },
      {
        path: '/blog',
        name: 'blog',
        component: () => import('@/views/blog.vue')
      },
      {
        path: '/blog_editor',
        name: 'blog_editor',
        component: () => import('@/views/blog_editor.vue')
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
      },]
  }


]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
