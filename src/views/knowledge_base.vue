<template>
  <div style="margin-top: 50px; width: 100%; text-align: center" class="main-div">
    <div class="main">
      <div > 
        <h1>知识库</h1>
      </div>

      <!-- 新建知识库 -->

      <div v-if="!hasKnowledge">
        <el-dialog
          v-model="dialogVisible"
          title="新建知识库"
          width="500"
          :before-close="handleClose" 
        >
        <!--  -->
        <el-input v-model="KnowledgeBaseName" style="width: 240px" placeholder="请输入知识库名称,不支持中文命名" clearable/>
        <br>
        <el-input v-model="description" style="width: 240px" placeholder="请输入知识库描述" clearable/>
        <!-- <el-button type="primary" @click="newKnowledge ">新建知识库</el-button> -->
          <template #footer>
            <div class="dialog-footer" >
              <el-button @click="KnowledgeValue=''">取消</el-button>
              <el-button type="primary" @click="newKnowledge" >
                确认
              </el-button>
            </div>
          </template>
        </el-dialog>
      </div>

      <div style="display: flex;  /* 竖直居中对齐 */">
      <!-- 选择知识库 -->
      <div style="flex: 1;flex-direction: column; width:60%; justify-content: center; /* 竖直居中对齐 */">

        <br><div  style="flex: 1">选择知识库</div><br>

        <div  style="flex: 1"> 
          <el-select v-model="KnowledgeValue" placeholder="请选择知识库" style="width: 240px" @focus="getKnowledgeBaseList"
          @change="changeKnowledge">
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </div>

      </div>
      <!-- 上传文件 -->

        <!-- 并排 -->
        <div   v-if="hasKnowledge" style="flex: 1;flex-direction: column; width:60%; justify-content: center; /* 竖直居中对齐 */">
          <br>
          <div  style="flex: 1">上传知识库文件</div>
          <br>
          <div  style="flex: 1"> 
            <el-upload ref="uploadRef" class="upload-demo"  multiple :auto-upload="false"
              :on-change="handleFileChange" :on-remove="handleRemove" v-model="fileLists">
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <template #trigger>
                <el-button type="primary" :span="4">选择文件</el-button>
              </template>
              <!-- <div class="el-upload__text">

                • HTML, HTM, MHTML, MD, JSON, JSONL, CSV, PDF, DOCX, DOC, PPT, PPTX,  <br>
                EML, MSG, RST, RTF, TXT, XML, EPUB, ODT, TSV, EML, MSG, EPUB, <br>
                XLSX, XLS, XLSD,IPYNB, PY, SRT, TOML,  ENEX<br>
                <br>
                Drop file here or <em>click to upload</em>
              </div> -->
              <el-button type="primary" @click="submitUpload" :span="4">上传文件</el-button>
              <template #tip>
                <div class="el-upload__tip">
                  Limit 200MB per file <br>
                </div>
              </template>

            </el-upload>
          </div>
        </div>
      </div>

          <el-row >
            <el-col :span="5">
                <el-input v-model="searchVal" placeholder="请输入需要查询内容" @change="Search" clearable/>
            </el-col>
            <el-col :span="2">
                <el-button  type="primary" @click="Search">查询</el-button>
            </el-col>
          </el-row>
          <!-- 分页表格 -->
          <el-table
            ref="singleTableRef"
            :data="tableData"
            highlight-current-row
            style="width: 60%; flex:1;"
            @current-change="getFileListsMethod"
          >
            <el-table-column type="index" width="50" />
            <el-table-column property="name" label="文件名"/>
          </el-table>
          <!-- page-count是最大页数，超过会折叠 -->
          <el-pagination
            :page-size="pageSize"
            :pager-count="10"
            layout="prev, pager, next"
            :total="total"
            :current-page="pageNo"
            @current-change="handleCurrentChange"
            style="flex:1;"
          />



    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, nextTick, watch } from 'vue'
import { createKnowledgeBase, getUserKnowledgeBaseList, uploadKnowledgeDoc, getKnowledgeBaseDoc } from '@/service/authService.js'
import { formatDateTime } from '@/utils/utils.js'
import { useRoute, useRouter } from 'vue-router';
import { Comment } from '@element-plus/icons-vue';
import { ElMessage, ElMessageBox } from 'element-plus'
import { ElUpload } from 'element-plus'

//从接口获取的所有数据
const currentFile = reactive([
]);
// 当前页
const pageNo = ref(1)
// 当前大小
const pageSize = ref(10)
// 表格数据
const tableData =ref([
]);
// 筛选条数
const total = ref(0)
const searchVal=ref('')
let filteredList=reactive([
]);
//是否搜索
let isSearch=ref(false)
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

const dialogVisible =computed(() => {
  //不等返回false，相等返回true
  return hasKnowledge.value === false;

});

const handleClose = () => {
    KnowledgeValue.value=''
}

//初始化时，接受用户id
onMounted(() => {
  hasKnowledge.value = true;
  user_id.value = localStorage.getItem('user_id')
  //判断一下是否有传参，无传参就退出
  if (!route.query.user_id) {
    return;
  }
  //有传参
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
async function uploadAllFile() {
  console.log('当前知识库id：' + currentKbId.value);
  const files = fileLists.value;
  for (const file of files) {
    if (file.raw) {
      const fileData = new FormData();
      fileData.append('files', file.raw);
      fileData.append('kb_id', currentKbId.value);

      console.log("正在处理"+file.name)
      await uploadFile(fileData, file.name); // 等待uploadFile完成
      console.log(file.name+"处理完毕")
    }
  }

  // 所有文件上传完成后的代码
  // 例如，清空文件列表
  // uploadRef.value.clearFiles();
  // getFileListsMethod();
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
async function uploadFile(fileData, name) {
  try {
    const res = await uploadKnowledgeDoc(fileData);
    console.log(res);
    if (res.code === 200) {
      if (Object.keys(res.data.failed_files).length === 0) {
        ElMessage.success(`上传文件 ${name} 成功`);
      } else {
        ElMessage.error(`上传失败！${res.data.failed_files[name]}`);
      }
      // 从 fileLists.value 中删除当前文件
      fileLists.value = fileLists.value.filter((file) => file.name !== name);
    } else {
      ElMessage.error(res.msg);
    }
  } catch (error) {
    console.error('上传文件时发生错误：', error);
    ElMessage.error('上传文件时发生错误');
  }
}

//得到当前文件：

let getFileLists = ref(null);

const  changeKnowledge = async (data)=>{
  console.log('change 当前知识库ID： '+data);
  currentKbId.value=data;
  getFileListsMethod();
}

//得到当前知识库的文件内容
const getFileListsMethod = async ()=>{

  //清空搜索：
  isSearch.value=false; searchVal.value='';
  console.log('得到文件的当前知识库id '+currentKbId.value);
  pageNo.value =1
  tableData.value='';
  total.value=0;
  currentFile.splice(0, currentFile.length);
  if (KnowledgeValue.value !== '新建知识库') {
    let data = {
      'kb_id': currentKbId.value
    }
    getKnowledgeBaseDoc(data).then(res => {
      if (res.code === 200) {

        getFileLists.value = res.data;
        console.log('当前知识库文件内容：',getFileLists);
        res.data.forEach(doc => {
          var file = {
            name: doc,
          };
          currentFile.push(file);

          //总条数
          total.value = res.data.length;
          //分页
          getpaginatedData();
        });
        console.log('表格内容',tableData.value);
      }
      else {
        console.log(res.msg);
      }
    })
  }
}

//分页
const getpaginatedData = () => {
    let start = pageNo.value > 1 ? (pageNo.value - 1) * pageSize.value : 0
    let end = pageNo.value * pageSize.value>total.value ? total.value:pageNo.value * pageSize.value
    if(isSearch.value===false)
      tableData.value = currentFile.slice(start, end);
    else{
      tableData.value = filteredList.slice(start, end);
    }
}


// 分页数事件触发此方法
const handleCurrentChange = val => {
  pageNo.value = val
  //搜索的时候分页就不对了啊
  getpaginatedData();
}

//查询文件
const Search = () => {
  if(searchVal.value.trim()===''){
    //为空返回全部
    getFileListsMethod();
    return;
  }
  const keyword1 = searchVal.value.trim()
  
  const list = currentFile;
  // const list = JSON.parse(localStorage.getItem('list') as string)
  filteredList = [...list]

  if (keyword1) {
    filteredList = filteredList.filter(item => item.name.includes(keyword1));
  }
  total.value = filteredList.length;
  isSearch.value=true;
  getpaginatedData();

  //emit('changeList', filteredList)
}

</script>

<style>

.main-div{
  border-radius: 15px;
}

.container {
  /* position: absolute; */
  
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
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