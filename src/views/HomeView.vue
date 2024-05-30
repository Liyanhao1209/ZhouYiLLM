<template>
  <div class="home">
    <img alt="ZhouYi logo" src="../assets/bagua.png">
    <HelloWorld msg="欢迎使用周易在线" />
    <el-button @click="this.$router.push('/login')">登录/注册</el-button>
    <el-button @click="this.$router.push('/all_chats')">所有问答</el-button>
    <el-button @click="this.$router.push('/chat')">问答</el-button>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  },
  methods:{
    
  }
}
</script>
