<template>
  <el-container class="container">
    <el-main class="main">
      <!-- 选择知识库 -->
      <el-select v-model="KnowledgeValue" placeholder="请选择知识库" style="width: 240px" @focus="getKnowledgeBaseList"
      @change="changeKnowledge">
        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
      <!-- 新建知识库 -->

      <div v-if="!hasKnowledge">
        <el-input v-model="KnowledgeBaseName" style="width: 240px" placeholder="请输入知识库名称,不支持中文命名" />
        <el-input v-model="description" style="width: 240px" placeholder="请输入知识库描述" />
        <el-button type="primary" @click="newKnowledge">新建知识库</el-button>
      </div>
      <!-- 上传文件 -->
      <div v-if="hasKnowledge">
        上传知识库文件
        <el-upload ref="uploadRef" class="upload-demo" drag action="false" multiple :auto-upload="false"
          :on-change="handleFileChange" :on-remove="handleRemove" v-model="fileLists">
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">

            • HTML, HTM, MHTML, MD, JSON, JSONL, CSV, PDF, DOCX, DOC, PPT, PPTX,  <br>
            EML, MSG, RST, RTF, TXT, XML, EPUB, ODT, TSV, EML, MSG, EPUB, <br>
            XLSX, XLS, XLSD,IPYNB, PY, SRT, TOML,  ENEX<br>
            <br>
            Drop file here or <em>click to upload</em>
          </div>

          <template #tip>
            <div class="el-upload__tip">
              Limit 200MB per file <br>
            </div>
          </template>

        </el-upload>
        <el-button class="ml-3" type="success" @click="submitUpload">
          上传文件
        </el-button>
        <div style="width: 400px; ">
          <!-- 显示当前知识库文件，支持分页？算了 -->

          当前知识库已有文件：
          <el-card v-if="getFileLists !== null && getFileLists !== ' '" style="width: 400px; align-items: center;">
            <p v-for="(doc, i) in getFileLists" :key="i" class="text item">{{ doc }}</p>
          </el-card>
          <el-card v-if="getFileLists === null || getFileLists === ' '" style="width: 400px; align-items: center;">
            <p>当前知识库无文件</p>
          </el-card>
        </div>
      </div>

    </el-main>
  </el-container>
</template>

<script setup>
import { ref, reactive, onMounted, computed, nextTick, watch } from 'vue'
import { createKnowledgeBase, getUserKnowledgeBaseList, uploadKnowledgeDoc, getKnowledgeBaseDoc } from '@/service/authService.js'
import { formatDateTime } from '@/utils/utils.js'
import { useRoute, useRouter } from 'vue-router';
import { Comment } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus'
import { ElUpload } from 'element-plus'



let user_id = ref(null);
let KnowledgeBaseName = ref('');
let description = ref('');
const route = useRoute();
//   let hasKnowledge = ref(true);//false;//默认当前没有知识库

const KnowledgeValue = ref('');

//是否显示新建知识库  使用computed动态更改值
const hasKnowledge = computed(() => {
  //不等返回false，相等返回true
  return KnowledgeValue.value !== '新建知识库';

});

//初始化时，接受用户id
onMounted(() => {
  hasKnowledge.value = true;
  user_id.value = localStorage.getItem('user_id')
  //判断一下是否有传参，无传参就退出
  if (!route.query.user_id) {
    return;
  }
  //有传参

  user_id.value = route.query.user_id || '';
  console.log(user_id.value)
});



let options = ref(null);
options.value = [
  {
    value: '新建知识库',//值 加载出
    label: '新建知识库',//文本
  }
];


//TODO:
//可以现默认加载当前用户第一个知识库的界面
//没有的话直接切换到新建知识库的界面

//创建新知识库
function newKnowledge() {
  //知识库名称不为空
  if (KnowledgeBaseName.value.trim() === '') {
    ElMessage({
      message: '知识库名称不能为空',
      type: 'error'
    })
    return;
  }
  //不能为中文，后端判断吧

  //传参数据
  console.log(KnowledgeBaseName.value, description.value, user_id.value);
  let data = {
    'kb_name': KnowledgeBaseName.value,
    'desc': description.value,
    'user_id': user_id.value
  }

  createKnowledgeBase(data).then(res => {
    if (res.code === 200) {
      //创建知识库成功
      console.log("创建知识库成功");
      ElMessage({
        message: '创建知识库成功',
        type: 'success'
      })

      //TODO:
      //跳转到新建的知识库界面，然后上传文件。。。
      //知识库option中增加现在的，并且value变成新建的知识库

      //后端输出的是：{"code":200,"msg":"已新增知识库 b8066be613504f58b8383c578766676a","data":null}
      //但是这个并不是返回给前端的值，所以一定要看源码啊不然就很浪费时间。
      let knowledgeId = res.data.kb_id;
      console.log("创建知识库id为：" + knowledgeId);
      //直接强制改了,没问题，有点小问题，因为显示的变成了id，但是点击一下就好了，暂时不想改了私密马赛。
      KnowledgeValue.value=KnowledgeBaseName.value//knowledgeId;


      //清空 
      KnowledgeBaseName = null;
      description = null;

    }
    else {
      console.log(res);
      ElMessage.error(res.code, res.msg);
    }
  })
}

//更改list
const addKnowledgeBase = (knowledge_base) => {
  var currentKB = {
    //   content: replay,
    //   type: "ai",
    value: knowledge_base.id,//值 加载出的
    label: knowledge_base.name,//文本  
    kb_id: knowledge_base.id,
    kb_name: knowledge_base.name,
    create_time: knowledge_base.create_time
  };
  options.value.push(currentKB);
  nextTick(() => { });
};
//options，然后更新 用focus
function getKnowledgeBaseList() {

  let data = { 'user_id': user_id.value };
  getUserKnowledgeBaseList(data).then(res => {
    if (res.code === 200) {
      console.log('获取用户知识库成功');
      console.log(res);
      //每次获取时强制将其options还原为新建知识库
      options.value = [
        {
          value: '新建知识库',//值 加载出
          label: '新建知识库',//文本
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

//上传文件
let fileLists = ref(null);

// 监听改变文件    
function handleFileChange(file, fileList) {
  fileLists.value = fileList
  console.log('test-filelist', fileLists.value)
}
// 删除文件
function handleRemove(file, fileList) {
  fileLists.value = fileList
  console.log('test-del-filelist', fileLists.value)
}

// function handleBeforeUpload (file) {
//     //获取上传文件大小
//     let fileSize = Number(file.size / 1024 / 1024);

//     if (fileSize > 200) {
//         ElMessage({ message: '文件大小不能超过200MB，请重新上传。', type: 'warning'})
//         return false
//     }
// }

let currentKbId=  ref('');
function uploadAllFile() {
  //得到知识库id
//options.value.find(item => item.label === KnowledgeValue.value);
  console.log('当前知识库id：    '+currentKbId.value);
  //多文件上传
  for (let i = 0; i < fileLists.value.length; i++) {
    // 若是新添加文件即存在fileLists.value.raw,则调用上传接口，否则不需调用
    //一个个上传
    if (fileLists.value[i].raw) {
      let fileData = new FormData();
      console.log("当前文件", fileLists.value[i].raw)

      fileData.append('files', fileLists.value[i].raw);

      //得到当前知识库id：
      fileData.append('kb_id', currentKbId.value);
      uploadFile(fileData, fileLists.value[i].name);//上传文件
      //上传完之后一个个删除上传的文件
    }
  }


}

const uploadRef = ref(null);
const submitUpload = () => {
  let faildata='';
  console.log('禁止上传：',currentKbId.value,fileLists.value);
  //如果没有选择知识库，禁止上传
  if(!currentKbId.value===null|| currentKbId.value===''){
    faildata+='请选择知识库！';
  }
  //如果没有文件，禁止上传
  if(fileLists.value===null|| fileLists.value===''){
    faildata+='请选择上传文件！';
  }
  if(faildata!==''){
    ElMessage.error(faildata);
    return;
  }
  uploadAllFile();
  uploadRef.value.submit();
  // 清空 el-upload 组件中的文件列表 删太快啦，就这样吧
  uploadRef.value.clearFiles();
  getFileListsMethod();
};


//上传文件 在默认的文件上传前被调用，为了禁止文件上传，需要返回false
function uploadFile(fileData, name) {

  console.log("给后端的data", fileData);
  uploadKnowledgeDoc(fileData).then(res => {
    console.log(res);
    //文件名：
    if (res.code === 200) {
      res.data.failed_files;
      console.log(res.data.failed_files);
      if(Object.keys(res.data.failed_files).length===0){
        ElMessage.success('上传文件' + name + '成功');
      }
      else{
        ElMessage.error('上传失败！'+res.data.failed_files[name]);
      }
      // 从 fileLists.value 中删除当前文件
        fileLists.value = fileLists.value.filter((file) => file.name !== name);
        console.log(fileLists.value, name);

        getFileListsMethod();
    }
    else {
      ElMessage.error(res.msg);
    }
  })
}

//得到当前文件：

let getFileLists = ref(null);

const  changeKnowledge =(data)=>{
  console.log('当前： '+data);
  currentKbId.value=data;
   getFileListsMethod();
}

const getFileListsMethod =()=>{
  console.log('得到文件的当前知识库id '+currentKbId.value);

  if (KnowledgeValue.value !== '新建知识库') {
    let data = {
      'kb_id': currentKbId.value
    }
    getKnowledgeBaseDoc(data).then(res => {
      if (res.code === 200) {

        getFileLists.value = res.data;
        console.log(getFileLists);
      }
      else {
        console.log(res.msg);
      }
    })
  }
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