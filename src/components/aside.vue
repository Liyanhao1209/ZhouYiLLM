<template>

  <!-- <el-radio-group v-model="isCollapse" style="margin-bottom: 20px">
    <el-radio-button :value="false">expand</el-radio-button>
    <el-radio-button :value="true">collapse</el-radio-button>
  </el-radio-group> -->
  <!-- <h5 class="mb-2" ></h5> -->
  <el-container width="200px">
    <el-aside width="200px" height="100%">
      <template #title>
        <!-- <el-icon><document /></el-icon> -->
        周易在线大模型
      </template>
      <el-menu router :default-active="$route.path" class="el-menu-vertical-demo" :collapse="isCollapse"
        @open="handleOpen" @close="handleClose">

  <el-menu-item index="/chat" >
    
      <el-icon><document /></el-icon>
      <template #title>新建对话</template>
  </el-menu-item>

  <el-menu-item index="/history_chats" >
        
        <template #title>
          <el-icon><document /></el-icon>
          历史对话
        </template>

    </el-menu-item>



    <!-- 被禁用了 -->
    <el-menu-item index="/knowledge_base" @click="toKnowledge">
      <el-icon><document /></el-icon>
      <template #title>知识库</template>
    </el-menu-item>
    <el-menu-item index="4" >
      <el-icon><document /></el-icon>
      <template #title>博客</template>
    </el-menu-item>
    <el-menu-item index="5">
      <el-icon><setting /></el-icon>
      <template #title>个人信息</template>
    </el-menu-item>
  </el-menu>
</el-aside>
</el-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router';
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
  Upload
} from '@element-plus/icons-vue'

const router = useRouter();

const isCollapse = ref(false)
// 历史对话是否显示
// const chatIsCollapse=ref(true)
const handleOpen = (key, keyPath) => {
  console.log(key, keyPath)
}
const handleClose = (key, keyPath) => {
  console.log(key, keyPath)
}
<<<<<<< HEAD
const router = useRouter();
//传参给知识库
const toKnowledge = () =>{
  router.push({ 
    name: 'knowledge_base', 
    query: {user_id: 'c3f1f73cec3c43458d6c2a6572cb327b' }
  });
}

=======
const logout = () => {
  router.push('/login')
}
// const router = useRouter();
// router.push({ name: 'history_chats', user_id: "c3f1f73cec3c43458d6c2a6572cb327b" });
>>>>>>> f941a3da44ed53dd61068ad43c3e9c537d414510


</script>

<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 150px;
  min-height: 40px;
  height: 100%;
  overflow-x: hidden
}

.item {
  margin-bottom: 18px;
}

.el-container {
  height: 100vh;
  /* 设置容器的高度为视口高度 */
  margin: 0;
}

.el-aside {
  position: relative;
  height: 100%;
  /* 设置aside的高度为容器的高度 */
  padding: 0px;
  /* background-color: #545c64; */
}
</style>
