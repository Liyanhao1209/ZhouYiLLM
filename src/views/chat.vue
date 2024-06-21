<template>
    <div class="body" style="height: 730px">
      <div class="container">
        <div class="right">
          <div class="top">
            {{ conv_name || '周易问答' }}
          </div>
          <div class="chat" ref="chatContainer">
            <div v-for="(item, i) in msgList" :key="i" :class="item.type == 'user' ? 'rightMsg' : 'leftMsg'">
              <img v-if="item.type === 'ai'" src="../assets/bagua.png" alt="" />
              <div :class="changeClass(item)">{{ item.content }}</div>
            </div>
          </div>
          <div class="bottom">
            <input v-model="value" placeholder="请输入您想提问的内容" :disabled="currentAiReply"/>
            <el-button type="primary" size="large" @click="onSend">
              发送
            </el-button>
            <el-button type="danger" size="large" @click="onPause">
              暂停
            </el-button>
          </div>
        </div>
        <el-select
            v-model="KnowledgeValue"
            placeholder="请选择知识库"
            class="fixed-select"
            @focus="getKnowledgeBaseList"
            @change="changeKnowledge"
        >
          <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="{ id: item.value, name: item.label }"
          />
        </el-select>
      </div>
    </div>



</template>



<script setup>
import { ref, reactive, nextTick, onMounted } from "vue";
import { createConversion, mixChat, getConversationRecord, getUserKnowledgeBaseList } from '@/service/authService.js'
import { ElMessage } from "element-plus";
import { useRoute, useRouter } from 'vue-router';
import store from '../store';
import { fetchEventSource, EventStreamContentType } from '@microsoft/fetch-event-source';
import { url } from '../../config/config'


const KnowledgeValue = ref('');
let options = ref(null);
//初始值
options.value = [
  {
    value: "faiss_zhouyi",//值 加载出
    label: '默认知识库',//文本
  }
];

let valid = ref(true);  // 定义 valid 值
let user_id = localStorage.getItem('user_id');
// 最开始对话id为空
let conv_id =  ref(null);
//默认为用户第一句
let conv_name = ref(null);
let aiCurrentChat = null;
const value = ref("");
const msgList = reactive([
]);
let currentKB = ref('faiss_zhouyi');
const changeClass = (item)=>{
  console.log('item',item);
  if(item.aiType==='docs'){
    return 'docmsg';
  }
  else return 'msg';
}

const onPause=()=>{
  valid.value=false;
  ElMessage({
    message: '输出已暂停',
    type: 'warning'
  })
};


//知识库检索为空时，判断并删除span
function extractTextFromSpan(html) {
  // 创建一个临时的 div 元素来容纳 HTML
  var tempDiv = document.createElement('div');
  tempDiv.innerHTML = html;

  // 查找 span 元素
  var span = tempDiv.querySelector('span');

  // 如果找到了 span 元素，返回它的文本内容
  if (span) {
    return span.textContent || span.innerText;
  }

  // 如果没有找到 span 元素，返回原来的文本
  return html;
}

//接受history的传参：
// 接收路由参数
//不能和参数的赋值写在一个函数里，会报错
const route = useRoute();

onMounted(() => {
  user_id = localStorage.getItem('user_id');
  //判断一下是否有传参，无传参就退出
  if (!route.query.conv_id || !route.query.conv_name ) {

    msgList.value=([]);
    conv_name.value='周易问答';
    return ;
  }
  //有传参说明是历史对话
  conv_id.value = route.query.conv_id || '';
  conv_name.value = route.query.conv_name || '';

  console.log(conv_name, conv_id.value, user_id)

  if (conv_id.value !== '' && conv_name.value !== '') {
    console.log(conv_name.value, conv_id.value);
    //加载历史聊天进入msgList
    let data = { "conv_id": conv_id.value };
    console.log(data);
    //当前历史记录
    const records = ref("");

    getConversationRecord(data).then(res => {
      if (res.code === 200) {
        records.value = res.data.records; // 使用 .value 来更新 ref 的值
        console.log(res);
        records.value.forEach(chat => {
          if (chat.is_ai) {
            // chat.content.answer
            //解析成json格式
            let content= JSON.parse(chat.content);
            // let content= chat.content;
            // let content_1=content.answer+ '参考：'+content.docs.docs;

            if(content.docs.docs!==null&&content.docs.docs!==''){
              let docs =content.docs.docs.map(doc => {
                doc=extractTextFromSpan(doc);
                return removeHttpLinks(doc);
              });
              console.log(docs);
              extractTextFromSpan(docs)
              AIReplay('参考：\n'+docs.join(''),'docs');
              // AIReplay('参考：'+content.docs.docs,'history');
            }
            if(content.answer!==null&&content.answer!=='') AIReplay(content.answer,'text');
            //  AIReplay(chat.content);
          }
          else { userQuestion(chat.content); }
        });
        scrollToNew();

      } else {
        console.log(res.msg);
      }
    }).catch(e => {
      console.error('获取历史对话记录失败:', e);
    });
  }
  else{
    msgList.value=([]);
    conv_name.value='周易问答';
    return ;
  }

});

//有新的对话默认继续滚动，但是这里的滚动条很丑，并且滚动幅度很小，建议修改
const scrollToNew = async () => {
  await nextTick();
  const  chatContainer = document.querySelector(".chat");
  if (chatContainer) {
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }
};

const userQuestion =  async  (question) => {
  var userMsg = {
    content: question,
    type: "user",
  };
  msgList.push(userMsg);
};

//历史记录的aiReply
const AIReplay =  async (replay,aitype) => {
  var autoReplyMsg = {
    content: replay,
    type: "ai",
    aiType: aitype
  };
  msgList.push(autoReplyMsg);
};

//删除docs中的链接
function removeHttpLinks(text) {
  const urlRegex = /\((http[^)]+)\)/g;
  return text.replace(urlRegex, '');
}

//sse
const controller = new AbortController();
const signal = controller.signal;
let currentAiReply = ref(false);



const sseAiChat =  async (query) =>{
  // if (!valid.value) {
  //   currentAiReply.value=false;
  //   return;
  // }
  // 发送文本
  let resultAnswer = ref('');

  let currentMessage = {
    "conv_id": conv_id.value,
    "query": query,
    "knowledge_base_id":  currentKB.value
  }
  console.log('当前对话request',currentMessage);
  //url可替换
  fetchEventSource(url+'conversation/mix-chat', {
    method: 'POST',
    signal: signal,
    headers: {
      'Content-Type': 'application/json',
      // token: window.sessionStorage.getItem('token'),
    },
    body:JSON.stringify(currentMessage),

    async onopen(response) {
      currentAiReply.value=true;
      console.log('onopen: ' + currentAiReply.value);
      //有log，但是一开始为空
      if (response.ok && response.headers.get('content-type') === 'text/event-stream') {
        console.log(response);
        return; // everything's good
      } else if (response.status >= 400 && response.status < 500 && response.status !== 429) {
        // client-side errors are usually non-retriable:
        console.log("回应错误")
      } else {
        // throw new RetriableError();
      }
    },
    async onmessage(msg) {
      if (!valid.value) {
        currentAiReply.value=false;
        controller.abort();
        return;
      }
      //后端的返回值一定要按照对应的格式！不然无法解析
      console.log('onmessage:'+currentAiReply.value);
      currentAiReply.value=true;
      const parsedData = JSON.parse(msg.data);
      console.log(parsedData); //

      if('docs' in parsedData.data){
        let docs = parsedData.data.docs.map(doc => {
          doc=extractTextFromSpan(doc);
          return removeHttpLinks(doc);
        });
        //在doc发送前删掉上一条
        // AIReplay('大模型正在生成回答，请耐心等待','wait');
        // 将ai回复加入list
        msgList.pop();
        AIReplay('参考：\n' + docs.join(''),'docs');
      }
      else if('text' in parsedData.data){
        //如果用户继续提问就完蛋了，
        // 将ai回复加入list  确定是ai的
        //这样还是不对，直接定位最后一条好了 同时加上新的aiType判断
        let latestMsg = msgList[msgList.length - 1];

        resultAnswer.value +=parsedData.data.text;
        //如果aiType为docs,就建立新的
        if(latestMsg.aiType==='docs'){
          AIReplay(resultAnswer.value,'text');
        }
        else{
          latestMsg.content=resultAnswer.value;
        }
      }
      scrollToNew();

    },
    onerror(err) {
      currentAiReply.value=false;//暂停回答
      throw err;    //必须throw才能停止
    },
    onclose(err){
      currentAiReply.value=false;//暂停回答
      throw err; //
    }
  });

}

//原来的
//ai对话  首先得到doc 然后得到继续回答
const aiChat = (query) => {
  //发送文本
  let currentMessage = {
    "conv_id": conv_id.value,
    "query": query,
    "knowledge_base_id": "faiss_zhouyi"
  }
  let jsonString = JSON.stringify(currentMessage);
  mixChat(jsonString).then(res => {
    // delay(10000).then(()=>{
    if (res.code === 200) {
      console.log(res.data);
      console.log(res.data.answer);
      // aiCurrentChat= res.data.answer;//????
      aiCurrentChat = res.data.answer.replace(/\n/g, '<br>');
      //将ai回复加入list
      AIReplay(aiCurrentChat);

    }
    else {
      ElMessage.error(res.data);
    }
  })
}

//点击发送回答问题
//应该一发送消息就设为禁止发送
const onSend =async  () => {
  valid.value=true;
  if (value.value.trim() === "") {
    ElMessage({
      message: '输入内容不能为空！',
      type: 'error'
    })
    return;
  }
  //如果空对话，创建新对话
  //加入了onMounted后，如果不是在新建对话界面而是直接跳转就会不对
  if (conv_id.value === null || conv_id.value === '') {
    //第一条
    let firstMessage = {
      user_id: localStorage.getItem('user_id'),
      conv_name: value.value
    }
    let jsonString = JSON.stringify(firstMessage);
    console.log("第一条", jsonString)

    createConversion(jsonString).then(res => {
      //200是数字
      if (res.code === 200) {
        console.log("成功建立！")
        console.log(res);
        conv_id.value = res.data.conv_id;

        //将对话名命名为第一个问句
        conv_name = value.value;

        if(currentAiReply.value===false) {
          currentAiReply.value=true;
          userQuestion(value.value);
          //让用户等待回答！
          AIReplay('大模型正在生成回答，请耐心等待','wait');
          sseAiChat(value.value);
        }
        else{
          ElMessage({
            message: '请等待当前回答结束！',
            type: 'error'
          })
          return ;
        }

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
  else if (conv_id.value !== null && value.value.trim() !== "") {

    if(currentAiReply.value===false) {
      currentAiReply.value=true;
      // 将用户问题加入list
      userQuestion(value.value);
      //让用户等待回答！
      AIReplay('大模型正在生成回答，请耐心等待','wait');
      sseAiChat(value.value);
    }
    else{
      ElMessage({
        message: '请等待当前回答结束！',
        type: 'error'
      })
      return ;
    }

    //自动滚动
    scrollToNew();
    //置空
    value.value = "";
  }
};


//更改list
const addKnowledgeBase =async  (knowledge_base) => {
  var currentKB = {
    //   content: replay,
    //   type: "ai",
    value: knowledge_base.id,//值 加载出的
    label: knowledge_base.name,//文本
  };
  options.value.push(currentKB);
  nextTick(() => { });
};
//options，然后更新 用focus
function getKnowledgeBaseList() {

  let data = { 'user_id': user_id };
  console.log('用户id', user_id);
  getUserKnowledgeBaseList(data).then(res => {
    if (res.code === 200) {
      console.log('获取用户知识库成功');
      console.log(res);
      //每次获取时强制将其options还原为新建知识库
      options.value = [
        {
          value: "faiss_zhouyi",//值 加载出
          label: '默认知识库',//文本
        }
      ];
      res.data.user_kbs.forEach(knowledge_base => {
        addKnowledgeBase(knowledge_base);
      });
      console.log(options.value);
    }
    else {
      console.log(res);
      ElMessage.error(res.code, res.msg);
    }
  })

}

//data 为option的value绑定的对象
const changeKnowledge = (data) => {
  console.log('当前知识库', data);
  currentKB.value = data.id;
  KnowledgeValue.value = data.name;
}
</script>

<style scoped lang="scss">
.body {
  color: #fff;
  font-weight: 900;
  letter-spacing: 2px;
  width: 100%;
  height: 100%;
  background-size: contain;
  display: flex;
  align-items: center;
  position: relative;
}

main {
  width: 90%;
  max-width: 1400px;
  height: 600px;
  //margin: 100px auto;
  display: flex;
}

.container {
  z-index: 1;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  position: relative;

  .right {
    flex: 1;
    background-color: rgba(147, 213, 255, 0);
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;

    .top {
      height: 70px;
      background-color: rgba(147, 213, 255, 0);
      color: #000;
      width: 100%;
      font-size: 22px;
      text-align: center;
      line-height: 70px;
    }

    .chat {
      flex: 1;
      max-height: 100%;
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
          word-wrap: break-word;
          max-width: 600px;
          background-color: #364d79;
          border-radius: 10px;
          white-space: pre-wrap;
          text-align: left;
        }
      }

      .rightMsg {
        justify-content: end;

        .msg {
          color: black;
          background-color: #dfdfdf;
        }
      }

      .leftMsg .docmsg {
        font-size: 12px;
        display: inline-block;
        padding: 10px;
        word-wrap: break-word;
        max-width: 600px;
        background-color: #3c69bb;
        border-radius: 10px;
        white-space: pre-wrap;
        text-align: left;
      }
    }

    .bottom {
      height: 60px;
      display: flex;
      align-items: center;
      width: 100%;
      margin: 10px auto;

      input {
        flex: 1;
        border: 1px solid rgb(171, 171, 171);
        border-right: none;
        height: 35px;
        color: black;
        text-indent: 2px;
        line-height: 35px;
        border-radius: 10px 0 0 10px;
      }

      .el-button {
        width: auto;
        border-radius: 0 10px 10px 0;
      }

      img {
        width: 20px;
        height: 20px;
      }
    }
  }
}

.fixed-select {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 240px;
  z-index: 1000;
}
</style>