<template>
    <div class="body" style=" height: 730px">
      <!-- <header>
        <div class="cover">
          <img
            src="../assets/background.png"
            alt=""
            style="width: 100%; height: 100%"
          />
        </div>
      </header> -->
      <main>
        <div class="container">
          <div class="right">
            <div class="top">
              {{ conv_name || '周易问答' }}  
            </div>
            <!-- 聊天框  大小待修改-->
            <div class="chat" ref="chatContainer">
              <div
                v-for="(item, i) in msgList"
                :key="i"
                :class="item.type == 'user' ? 'rightMsg' : 'leftMsg'"
              >
                <img
                  v-if="item.type == 'ai'"
                  src="../assets/bagua.png"
                  alt=""
                />
                <div class="msg">{{ item.content }}</div>
                <!-- <img
                  v-if="item.type == 'user'"
                  src="../assets/logo.png"
                  alt=""
                /> -->
              </div>
            </div>
            <div class="bottom">
              <input v-model="value" placeholder="请输入您想提问的内容" />
              <button @click="onSend" >
                <!-- <img src="	https://chatglm.cn/img/send.6d617ab7.svg" alt="发送" /> -->
                发送
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  </template>
  
  <script setup>
import { ref, reactive, nextTick , onMounted } from "vue";
import { createConversion,mixChat,getConversationRecord} from '@/service/authService.js'
import { ElMessage } from "element-plus";
import { useRoute, useRouter } from 'vue-router';



 let user_id="c3f1f73cec3c43458d6c2a6572cb327b";
  // 最开始对话id为空
  let conv_id=null;
  //默认为用户第一句
  let  conv_name=null;
  let aiCurrentChat=null;
  const value = ref("");
  const msgList = reactive([
  ]);
  
  //接受history的传参：
  // 接收路由参数
  //不能和参数的赋值写在一个函数里，会报错
  const route = useRoute();

  onMounted(() => {
    //判断一下是否有传参，无传参就退出
    if(!route.query.conv_id || !route.query.conv_name||!route.query.user_id){
      return ;
    }
    //有传参说明是历史对话
    conv_id= route.query.conv_id || '';
    conv_name = route.query.conv_name || '';
    user_id = route.query.user_id || '';
    console.log(conv_name,conv_id,user_id)

    if(conv_id!==null&&conv_name!==null){

      //加载历史聊天进入msgList
      let data = { "conv_id": conv_id };  
      console.log(data);
      //当前历史记录
      const records =ref("");

      getConversationRecord(data).then(res => {  
        if (res.code === 200) {  
          records.value = res.data.records; // 使用 .value 来更新 ref 的值  
          console.log(res); 
          records.value.forEach(chat => {  
            if(chat.is_ai) {AIReplay(chat.content);}   else{ userQuestion(chat.content);}
          }); 
          

        } else {  
          console.log(res.msg);  
        }  
      }).catch(e => {  
        console.error('获取历史对话记录失败:', e);  
      });  
    }
  });

  //有新的对话默认继续滚动，但是这里的滚动条很丑，并且滚动幅度很小，建议修改
  const scrollToNew = async () => {
    await nextTick();
    const chatContainer = document.querySelector(".chat");
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  };
  
  const userQuestion = (question) => {
    var userMsg = {
      content: question,
      type: "user",
    };
    msgList.push(userMsg);
  };
  
  const AIReplay = (replay) => {
    var autoReplyMsg = {
      content: replay,
      type: "ai",
    };
    msgList.push(autoReplyMsg);
  };
  

 
  //ai对话
  const aiChat = (query) =>{
    //发送文本
    let currentMessage ={
      "conv_id": conv_id,
      "query":  query,
      "knowledge_base_id": "faiss_zhouyi"
    }
    let jsonString =JSON.stringify(currentMessage);
    mixChat(jsonString).then(res=>{
      // delay(10000).then(()=>{
        if(res.code === 200){
          console.log(res.data);
          console.log(res.data.answer);
          aiCurrentChat= res.data.answer;//????
      //将ai回复加入list
          AIReplay(aiCurrentChat);
          
        }
        else {
          ElMessage.error(res.code,res.data.msg);
        }
      // })


      })
  }

  //点击发送回答问题
  const onSend = () => {
    if(value.value.trim() === ""){
      ElMessage({
					message: '输入内容不能为空！',
					type: 'error'
				})
      
    }
    //如果空对话，创建新对话
    //加入了onMounted后，如果不是在新建对话界面而是直接跳转就会不对
    if (conv_id === null||conv_id=== ''){
      //第一条
      let firstMessage={ 
        user_id:user_id,
        conv_name:value.value
      }
      let jsonString =JSON.stringify(firstMessage);
      console.log("第一条",jsonString)
      createConversion(jsonString).then(res=>{
        //200是数字
        if(res.code === 200){
          console.log("成功建立！")
            console.log(res);
            conv_id = res.data.conv_id;

            //将对话名命名为第一个问句
            conv_name=value.value;
            userQuestion(value.value);
            aiChat(value.value);

           
            //自动滚动
            scrollToNew();
            //置空
            value.value = "";
        }
        else {
            console.log(res);
        }
      })

    }
    else if (conv_id !== null && value.value.trim() !== "") {
      // 将用户问题加入list
      userQuestion(value.value);
      // AI回复;
      aiChat(value.value);

      // AIReplay(aiCurrentChat);
      //自动滚动
      scrollToNew();
      //置空
      value.value = "";
    }
  };
  </script>
  
   
  <style scoped lang="scss">
  .body {

    color: #fff;
    font-weight: 900;
    letter-spacing: 2px;
    width: 100%;
    height: 100%;
    background-size:center;
    display: flex;
    align-items: center;
    position: relative;
  }
  main {
    /* border: 1px solid red; */
    width: 1400px;
    height: 600px;
    margin: 100px auto;
    display: flex;
  }
  .cover {
    position: absolute;
    top: 0px;
    z-index: 0;
    height: 180px;
    width: 1483px;
    left: 50%;
    margin-left: -754px;
    overflow: hidden;
  }
  .body {
    :deep(.slick-slide) {
      text-align: center;
      height: 100%;
      line-height: 100%;
    //  background: #364d79;
      overflow: hidden;
    }
   
    :deep(.slick-arrow.custom-slick-arrow) {
      width: 25px;
      height: 25px;
      font-size: 25px;
      color: #fff;
    //  background-color: rgba(31, 45, 61, 0.11);
      transition: ease all 0.3s;
      opacity: 0.3;
      z-index: 1;
    }
   
    :deep(.slick-arrow.custom-slick-arrow:before) {
      display: none;
    }
   
    :deep(.slick-arrow.custom-slick-arrow:hover) {
      color: #fff;
      opacity: 0.5;
    }
   
    :deep(.slick-slide h3) {
      color: #fff;
    }
  }
   
  .container {
    z-index: 1;
    // border: solid 1px #bebebe;
    width: 85%;
    height: 100%;
    margin: -6px auto;
    display: flex;
    justify-content: center;
    left:30px;
   
    .right {
      flex: 1;
      // border-radius: 10px;
      background-color: rgba(147, 213, 255, 0);
      display: flex;
      flex-direction: column;
      height: 600px;
      // .top {
      //   height: 70px;
      //   background-color: rgba(147, 213, 255, 0.764);
      //   width: 100%;
      //   font-size: 22px;
      //   text-align: center;
      //   line-height: 70px;
      // }
      .top {
        height: 70px;
        background-color: rgba(147, 213, 255, 0); /* 最后一个值设置为 0，表示完全透明 */
        color:#000;
        width: 100%;
        font-size: 22px;
        text-align: center;
        line-height: 40px;
      }

      .chat {
        flex: 1;
        max-height: 580px;
        overflow-y: auto;
        padding: 10px;
        .leftMsg,
        .rightMsg {
          display: flex;
          flex-direction: row;
          justify-content: start;
          align-items: center;
          margin: 10px;
   
          img {
            width: 40px;
            height: 40px;
            border-radius: 20px;
            overflow: hidden;
            object-fit: cover;
            margin: 0 10px;
          }
   
          .msg {
            display: inline-block;
            padding: 10px;
            word-wrap: anywhere;
            max-width: 600px;
            background-color: #364d79;
            border-radius: 10px;
          }
        }
   
        .rightMsg {
          justify-content: end;
   
          .msg {
            color: black;
            background-color: #dfdfdf;
          }
        }
      }
   
      .bottom {
        height: 45px;
        display: flex;
        align-items: center;
        width: 80%;
        margin: 10px auto;
   
        input {
          width: 90%;
          border: 1px solid rgb(171, 171, 171);
          border-right: none;
          height: 40px;
          color: black;
          text-indent: 2px;
          line-height: 40px;
          border-radius: 10px 0 0 10px;
        }
   
        button {
          cursor: pointer;
          width: 10%;
          border: none;
          outline: none;
          height: 45px;
          border-radius: 0 10px 10px 0;
          background: linear-gradient(
            to right,
            rgb(146, 197, 255),
            rgb(200, 134, 200)
          );
        }
        img {
          width: 20px;
          height: 20px;
        }
      }
    }
  }
  .separator {
    color: rgb(133, 132, 132);
    text-align: center;
    font-size: 15px;
    font-weight: normal;
  }
  </style>