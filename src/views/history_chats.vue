<template>
    <div style="margin-top: 50px; width: 100%; text-align: center" class="main-div">
      
      <div > 
        <h1>历史对话</h1>
      </div>

      <!-- <el-scrollbar style="margin: 0; padding: 0; border: none;"> -->
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
                <el-icon class="text item" style="left: 0%;font-size: 24px;" @click="deleteCurrentChat(chat)">
                  <Delete />
                </el-icon>
              </div>
            </div>
          </div>
          </el-card>
        </div>
      <!-- </el-scrollbar> -->

      </div>
</template>

<script setup>
import { ref,reactive,onMounted} from 'vue'
import {getUserAllConversation,deleteConversation}from  '@/service/authService.js'
import { formatDateTime}  from '@/utils/utils.js'
// import Chats from './chats.vue';
import { useRoute, useRouter } from 'vue-router';
import {Comment,Delete} from '@element-plus/icons-vue';
import { ElMessage,ElMessageBox } from "element-plus";
  
let user_id = ref(null);
const route = useRoute();
//得到userid
onMounted(() => {
  // if(! localStorage.getItem('user_id')) localStorage.getItem('user_id')// 
  user_id.value= localStorage.getItem('user_id');
  console.log(route.query.user_id,localStorage.getItem('user_id'),user_id.value);

  // 调用 getChatList 函数  
  getChatList();  
});
//写死的目的是方便测试

const chatHistory = ref(null); // 使用 ref 创建一个响应式引用  

function getChatList() {  
  let data = { "user_id": user_id.value };  
  return  getUserAllConversation(data).then(res => {  
    if (res.code === 200) {  
      chatHistory.value = res.data.conversations; // 使用 .value 来更新 ref 的值  
      chatHistory.value.reverse();
      chatHistory.value.forEach(chat => {  
          chat.formattedCreateTime = formatDateTime(chat.create_time); // 添加一个新字段来保存格式化后的时间  
      }); 
      console.log(chatHistory.value);  
      return true;
    } else {  
      console.log(res.msg);  
    }  
  }).catch(e => {  
    console.error('获取对话列表失败:', e);  
  });  
}  



const router = useRouter();

const setCurrentChat = (chat) => {
    let currentChat = chat;
  // router.push('/chat');

      router.push({ name: 'chat', query: {
      conv_id:currentChat.id,
      conv_name:currentChat.conv_name,
    } });
}

const deleteCurrentChat = (chat) => {
  console.log(chat);

  ElMessageBox.confirm(
    '确认删除当前对话吗？',
    '提示',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(() => {
      // let deleteId=chat.id;
      let data={
        'conv_id':chat.id,
      }
      deleteConversation(data).then(res=>{
          if(res.code===200){
            //重新得到历史记录
            if(getChatList()){
                ElMessage({
                  type: 'success',
                  message: '成功删除！',
                })
            } 
          }
      })
      // ElMessage({
      //   type: 'success',
      //   message: '成功删除！',
      // })
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消删除！',
      })
    })

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