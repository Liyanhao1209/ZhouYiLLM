<template>
  <el-container class="container">
    <el-main class="main">
      
      <div > 
        <h1>历史会话</h1>
      </div>

      <el-scrollbar style="margin: 0; padding: 0; border: none;">
        <div class="card-container"> <!-- 添加一个类来包裹所有的el-card -->  
          <el-card
            v-for="(chat, index) in chatHistory"
            :key="index"
            class="box-card"
            style="margin-bottom: 10px;"
          >
          <div class="card-content">
            <div class="card-header">
              <div class="left-items">
                <el-icon class="text item" style="left: 0%;font-size: 24px;">
                  <Comment />
                </el-icon>
                <span class="text item" style="text-align: left;font-size: 18px;">{{ chat.conv_name }}</span>
              </div>

              <div class="right-items">
                <div class="text item" style="font-size: 15px;right: 0%">
                  {{ chat.formattedCreateTime }}
                </div>
                <el-button class="text item" type="text" @click="setCurrentChat(chat)" style="text-align: right;" >
                  对话详情
                </el-button>
              </div>
            </div>
          </div>
          </el-card>
        </div>
      </el-scrollbar>

    </el-main>
  </el-container>
</template>

<script setup>
import { ref,reactive} from 'vue'
import {getUserAllConversation}from  '@/service/authService.js'
import { formatDateTime}  from '@/utils/utils.js'
// import Chats from './chats.vue';
import { useRoute, useRouter } from 'vue-router';
import {Comment} from '@element-plus/icons-vue'
  

//写死的目的是方便测试，因为登录注册没想明白怎么绕过菜单
// 我的建议是
const user_id = "fb18845ed0604498812f8a0135255253";  
const chatHistory = ref(null); // 使用 ref 创建一个响应式引用  

function getChatList() {  
  let data = { "user_id": user_id };  
  getUserAllConversation(data).then(res => {  
    if (res.code === 200) {  
      chatHistory.value = res.data.conversations; // 使用 .value 来更新 ref 的值  
      chatHistory.value.reverse();
      chatHistory.value.forEach(chat => {  
          chat.formattedCreateTime = formatDateTime(chat.create_time); // 添加一个新字段来保存格式化后的时间  
      }); 
      console.log(chatHistory.value);  

    } else {  
      console.log(res.msg);  
    }  
  }).catch(e => {  
    console.error('获取对话列表失败:', e);  
  });  
}  

// 调用 getChatList 函数  
getChatList();  


//稀里糊涂就传参成功了？？？？
const router = useRouter();

const setCurrentChat = (chat) => {
    let currentChat = chat;
  // router.push('/chat');

      router.push({ name: 'chat', query: {
      conv_id:currentChat.id,
      conv_name:currentChat.conv_name,
      user_id: currentChat.user_id,
    } });
}



</script>

<style>
.container {
  /* position: absolute; */
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  display: flex;
}


.main {
  flex: 1;
  padding: 0px;
}

.card-content {
  width: 60%;
  height: 30px;
  margin-top: 10px;
  margin-bottom: 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  /* gap: 10px; */
  align-items: center;
}

.left-items {
  display: flex;
  gap: 20px;
  align-items: center;
  
}

.right-items {
  display: flex;
  gap: 20px;
  align-items: center;
  
}




</style>