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

        <el-menu-item index="/chat">

          <el-icon>
            <document />
          </el-icon>
          <template #title>新建对话</template>
        </el-menu-item>
        <!-- 只把这个作为标题，没有侧拉框？ -->
        <el-menu-item index="/history_chats" @click="router">

          <!-- 嵌套一个menu -->
          <template #title>
            <el-icon>
              <document />
            </el-icon>
            历史对话
          </template>
          <!-- <el-sub-menu
          default-active="2"
          class="el-menu-vertical-demo"
          :collapse="chatIsCollapse"
          @open="chatHandleOpen"
          @close="chatHandleClose"
        > -->
          <!-- 历史问答： -->
          <!-- 
        <el-card
        v-for="(chat, index) in chatHistory"
        :key="index"
        class="box-card"
        style="margin-bottom: 10px;"
      >
        <template #header>
          <div class="card-header">
            <span>{{ chat.timestamp }}</span>
            <el-button class="button" type="text">详情</el-button>
          </div>
        </template>
        <div class="text item">
          {{ chat.content }}
        </div>
      </el-card> -->
          <!-- 侧拉栏内容，搞成固定的？ -->


          <!-- <span>历史对话</span> -->

          <!-- <el-menu-item-group>
        <template #title><span>Group One</span></template>
        <el-menu-item index="1-1">item one</el-menu-item>
        <el-menu-item index="1-2">item two</el-menu-item>
      </el-menu-item-group>

      <el-menu-item-group title="Group Two">
        <el-menu-item index="1-3">item three</el-menu-item>
      </el-menu-item-group>
      <el-sub-menu index="1-4">
        <template #title><span>item four</span></template>
        <el-menu-item index="1-4-1">item one</el-menu-item>
      </el-sub-menu> -->
        </el-menu-item>

        <!-- <el-sub-menu index="2">

    </el-sub-menu> -->


        <!-- 被禁用了 -->
        <el-menu-item index="3">
          <el-icon>
            <document />
          </el-icon>
          <template #title>创建知识库</template>
        </el-menu-item>
        <el-menu-item index="/blog">
          <el-icon>
            <document />
          </el-icon>
          <template #title>博客</template>
        </el-menu-item>
        <el-menu-item index="5">
          <el-icon>
            <setting />
          </el-icon>
          <template #title>个人信息</template>
        </el-menu-item>
        <el-menu-item >
          <el-icon>
            <upload/>
          </el-icon>
          <el-button type="danger" @click="logout">登出</el-button>
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
const logout = () => {
  router.push('/login')
}
// const router = useRouter();
// router.push({ name: 'history_chats', user_id: "c3f1f73cec3c43458d6c2a6572cb327b" });


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
