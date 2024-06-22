<template>
  <el-button type="info" :icon="Back" class="bar-button" style="float: left; margin-left: 10px;" @click="goBack()">
    返回
  </el-button>
  <div class="body" style="height: 730px">
    <div class="container">
      <div class="right">
        <div class="top">
          {{ conv_name || '周易问答' }}
        </div>
        <div class="chat" ref="chatContainer">
          <div v-for="(item, i) in msgList" :key="i" :class="item.type == 'user' ? 'rightMsg' : 'leftMsg'">
            <img v-if="item.type === 'ai'" src="../../assets/bagua.png" alt="" />
            <div :class="changeClass(item)">{{ item.content }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>



</template>



<script setup>
import { ref, reactive, nextTick, onMounted } from "vue";
import { createConversion, mixChat, getConversationRecord, getUserKnowledgeBaseList } from '@/service/authService.js'
import { ElMessage } from "element-plus";
import { useRoute, useRouter } from 'vue-router';
import { Back } from '@element-plus/icons-vue';


const router = useRouter();
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
let conv_id = ref(null);
//默认为用户第一句
let conv_name = ref(null);
let aiCurrentChat = null;
const value = ref("");
const msgList = reactive([
]);


let currentKB = ref('faiss_zhouyi');
const changeClass = (item) => {
  //console.log('item',item);
  if (item.aiType === 'docs') {
    return 'docmsg';
  }
  else return 'msg';
}

const onPause = () => {
  valid.value = false;
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
  if (!route.query.conv_id || !route.query.conv_name) {
    msgList.value = ([]);
    conv_name.value = '周易问答';
    return;
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
            let content = JSON.parse(chat.content);
            // let content= chat.content;
            // let content_1=content.answer+ '参考：'+content.docs.docs;

            if (content.docs.docs !== null && content.docs.docs !== '') {
              let docs = content.docs.docs.map(doc => {
                doc = extractTextFromSpan(doc);
                return removeHttpLinks(doc);
              });
              //console.log(docs);
              extractTextFromSpan(docs)
              AIReplay('参考：\n' + docs.join(''), 'docs');
              // AIReplay('参考：'+content.docs.docs,'history');
            }
            if (content.answer !== null && content.answer !== '') AIReplay(content.answer, 'text');
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
  else {
    msgList.value = ([]);
    conv_name.value = '周易问答';
    return;
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

const userQuestion = async (question) => {
  var userMsg = {
    content: question,
    type: "user",
  };
  console.log(msgList)
  msgList.push(userMsg);
};

//历史记录的aiReply
const AIReplay = async (replay, aitype) => {
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


//更改list
const addKnowledgeBase = async (knowledge_base) => {
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

const goBack = () => {
  console.log("11232");
  router.back()
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