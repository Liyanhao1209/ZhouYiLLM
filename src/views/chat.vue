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
            <input v-model="value" placeholder="请输入您想提问的内容" />
            <el-button :type="button.type" size="large" @click="onSend" :disabled="button.status">
               {{ button.text }}
               <!-- primary -->
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
import { createConversion, mixChat, getConversationRecord, getUserKnowledgeBaseList,stopChat } from '@/service/authService.js'
import { ElMessage, parseDate } from "element-plus";
import { useRoute, useRouter } from 'vue-router';
import store from '../store';
import { fetchEventSource, EventStreamContentType } from '@microsoft/fetch-event-source';
import { url } from '../../config/config'


const KnowledgeValue = ref('');

//发送和暂停按钮
let button =ref(null)
button.value = 
  {
    text: '发送',//值 加载出
    type: 'primary',//文本
    status:false
  }
//用户是否终止当前回答： 默认为未终止
let isUserAbort = ref(false);
//用户最新的query
let currentQuery=ref(null);
//当前Docs
let currentDocs=ref(null);


let options = ref(null);
//初始值
options.value = [
  {
    value: "faiss_zhouyi",//值 加载出
    label: '默认知识库',//文本
  }
];

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
  //console.log('item',item);
  if(item.aiType==='docs'){
    return 'docmsg';
  }
  else return 'msg';
}




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

  //console.log(conv_name, conv_id.value, user_id)

  if (conv_id.value !== '' && conv_name.value !== '') {
    //console.log(conv_name.value, conv_id.value);
    //加载历史聊天进入msgList
    let data = { "conv_id": conv_id.value };
    //console.log(data);
    //当前历史记录
    const records = ref("");

    getConversationRecord(data).then(res => {
      if (res.code === 200) {
        records.value = res.data.records; // 使用 .value 来更新 ref 的值
        //console.log(res);
        records.value.forEach(chat => {
          if (chat.is_ai) {
            // chat.content.answer
            //解析成json格式
            let content= JSON.parse(chat.content);
            // let content= chat.content;
            // let content_1=content.answer+ '参考：'+content.docs.docs;
            if(content.docs.docs!==null&&content.docs.docs!==''&&content.docs.length!==0){
              let docs =content.docs.docs.map(doc => {
                doc=extractTextFromSpan(doc);
                return removeHttpLinks(doc);
              });
              console.log(docs);
              if(docs.length!==0){
                extractTextFromSpan(docs)
                AIReplay('参考：\n'+docs.join(''),'docs');
              }
              
              // AIReplay('参考：'+content.docs.docs,'history');
            }
            if(content.answer!==null&&content.answer!=='') AIReplay(content.answer,'text');
            //  AIReplay(chat.content);
          }
          else { userQuestion(chat.content); }
        });
        scrollToNew();

      } else {
        //console.log(res.msg);
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
  console.log(msgList)
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
let controller = ref(null);
controller.value = new AbortController();
const signal = ref(controller.value.signal);

//当前状态为ai正在回答
let currentAiReply = ref(false);


const sseAiChat =  async (query) =>{

  // 发送文本
  let resultAnswer = ref('');

  let currentMessage = {
    "conv_id": conv_id.value,
    "query": query,
    "knowledge_base_id":  currentKB.value
  }
  //console.log('当前对话request',currentMessage);
  //url可替换
  fetchEventSource(url+'conversation/mix-chat', {
    method: 'POST',
    signal: signal.value,
    headers: {
      'Content-Type': 'application/json',
      // token: window.sessionStorage.getItem('token'),
    },
    body:JSON.stringify(currentMessage),

    onopen(response) {
      currentAiReply.value=true;
      console.log('开始sse:  onopen: ' + currentAiReply.value);
      //有log，但是一开始为空
      if (response.ok && response.headers.get('content-type') === 'text/event-stream') {
        //console.log(response);
        return; // everything's good
      } else if (response.status >= 400 && response.status < 500 && response.status !== 429) {
        // client-side errors are usually non-retriable:
        //console.log("回应错误")
      } else {
        // throw new RetriableError();
      }
    },
     onmessage(msg) {
      console.log('onmessage: ' ,'isUserAbort.value:'+isUserAbort.value,msg)
      //如果用户未中断：就继续拼接
      if(isUserAbort.value===false) {

        //后端的返回值一定要按照对应的格式！不然无法解析
        console.log('onmessage:'+currentAiReply.value);
        currentAiReply.value=true;
        
        const parsedData = JSON.parse(msg.data);
        console.log(parsedData); 
        console.log(msg.data);
        //如果是文档
        if('docs' in parsedData.data){
          currentDocs.value=parsedData.data.docs;
          let docs = parsedData.data.docs.map(doc => {
            doc=extractTextFromSpan(doc);
            return removeHttpLinks(doc);
          });
          // currentDocs.value=docs;//docs.join('');
          console.log('回答的docs',currentDocs.value);
          //在doc发送前删掉上一条
          // AIReplay('大模型正在生成回答，请耐心等待','wait');
          // 将ai回复加入list
          msgList.pop();
          AIReplay('参考：\n' + docs.join(''),'docs');
        }
        //如果是回答
        else if('text' in parsedData.data){
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
      }
    },

    onerror(err) {
      
      console.error('Fetch error:', err); 
      throw err;    //必须throw才能停止
    },
    onclose(err){
      currentAiReply.value=false;//暂停回答
      changeButton(false);
      console.log(currentQuery)
      console.log('Connection closed',currentDocs); 
      throw err; //
    }
    
  }).then(
    (response) => {
      console.log('回答终止 fetchEventSource.then',response);
      //回答终止或者结束
      currentAiReply.value=false;//暂停回答

      changeButton(false);
    }
  ).catch((error) => {
    //应该显示aborterror为什么不显示呢
    console.error('回答出错 fetchEventSource.catch',error);
    currentAiReply.value=false;//暂停回答
 
      changeButton(false);
  }
  );

}

//根据 ai回答  改变button状态
const changeButton= (status) =>{
  //true表示正在发送，就停止
  if(status===true){
      button.value.text='停止';
      button.value.type='info';
  }
  //不然就变为发送
  else{
      button.value.text='发送';
      button.value.type='primary';
  }
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
      //console.log(res.data);
      //console.log(res.data.answer);
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
const onSend = async()  => {


  //先判断当前状态是ai正在回答，还是用户发送消息
  //如果是ai正在回答，就停止回答，停止sse拼接字符串
  // console.log("点击发送还是暂停",button.value.type)

  function changeWait(){
    console.log(button);
    //停止回答
    controller.value.abort(); //连接没有被完全断开欸
    signal.value=controller.value.signal;
    console.log(signal.value);

    isUserAbort.value = true; //中断回答
    console.log('isUserAbort.value',isUserAbort.value);
    //没有ai回答为什么还要继续终止？当然是因为还没有进行到
    
    
    let returnData={
      conv_id:conv_id.value,
      query:currentQuery.value,//用户当前查询的内容，不会置为空了吧
      //不可以设为null！
      current_docs:[],
      current_ans:'',
    }
    // 先找到最新的AIreply
    let latestMsg = msgList[msgList.length - 1];
    //第一种情况：没有返回值,当前的AIReplay为('大模型正在生成回答，请耐心等待','wait');
    if(latestMsg.aiType==='wait'){
      
      //有很大的延迟，关键是因为后端请求太慢了
      //这个时候可能根本就没发起请求？
    }
    //第二种情况，有docs返回，但是还没有回答生成
    else if(latestMsg.aiType==='docs'){
      returnData.current_docs=currentDocs.value;
    }
    //第三种情况，有回答生成
    else if(latestMsg.aiType==='text'){
      //要记得添加！
      returnData.current_docs=currentDocs.value;
      returnData.current_ans=latestMsg.content;
    }

    console.log('停止的返回信息',returnData);
    //调用后端接口：
    stopChat(returnData).then(res => {
      //200是数字
      if (res.code === 200) {
        console.log("成功终止当前对话！")
        console.log(res);
        if(latestMsg.aiType==='wait'){
          msgList.pop();
          AIReplay('(用户已终止对话)\n','text');
        }
        if( latestMsg.aiType==='docs'){
          AIReplay('(用户已终止对话)\n','text');
        }
        else if(latestMsg.aiType==='text'){
          latestMsg.content=latestMsg.content+'\n(用户已终止对话)\n';
        }
        currentAiReply.value=false;
        changeButton(false);
        console.log("停止完成");
        button.value.status=false;
        
        if(currentAiReply.value===false) isUserAbort.value=false;
        //自动滚动
        scrollToNew();

        //删除之前的sse的controller
        //直接断掉上一层的sse连接！！！
        controller.value= new AbortController();
        signal.value =controller.value.signal;
      }
      else{
        console.log(res);
        ElMessage({
          message: '无法结束当前对话！',
          type: 'error'
        })
        return ;
      }
       
      
    })

    
  }
  if(button.value.type==='info'){

    button.value.status=true;
    changeWait();

    return ;
  }

  //如果用户再次点击发送，再在用户中断设为false
  else  isUserAbort.value===false;

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
        //console.log(res);
        conv_id.value = res.data.conv_id;

        //将对话名命名为第一个问句
        conv_name = value.value;

        if(currentAiReply.value===false) {
          // currentAiReply.value=true;
          currentQuery.value=value.value;
          userQuestion(value.value);
          //让用户等待回答！
          AIReplay('大模型正在生成回答，请耐心等待','wait');
          
          //开始回答时更改字体为 停止
          changeButton(true);

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
        //console.log(res);
      }

    })

  }
  //不是第一条回答
  else if (conv_id.value !== null && value.value.trim() !== "") {

    //当前ai没有进行回答，也就是onclose没结束
    if(currentAiReply.value===false) {
      // currentAiReply.value=true;
      // 将用户问题加入list
      userQuestion(value.value);
      currentQuery.value=value.value;
      //让用户等待回答！
      AIReplay('大模型正在生成回答，请耐心等待','wait');

      //开始回答时更改字体为 停止
      changeButton(true);

      sseAiChat(value.value);
    }
    else{
      ElMessage({
        message: '目前流量高峰期,过会儿再来试试吧！',
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
  //console.log('用户id', user_id);
  getUserKnowledgeBaseList(data).then(res => {
    if (res.code === 200) {
      //console.log('获取用户知识库成功');
      //console.log(res);
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
      //console.log(options.value);
    }
    else {
      //console.log(res);
      ElMessage.error(res.code, res.msg);
    }
  })

}

//data 为option的value绑定的对象
const changeKnowledge = (data) => {
  //console.log('当前知识库', data);
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