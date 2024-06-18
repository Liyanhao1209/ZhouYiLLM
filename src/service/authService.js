import axios from 'axios'

const url = 'http://zyllmbackend.ihk.fghk.top'
// const url = 'http://localhost:9090/'
export const request = axios.create({
    baseURL: url,
    headers: {
        'content-type': 'application/json'
    },
})

const requestGet = axios.create({
    baseURL: url,
    headers: {
    },
})

const requestFile = axios.create({
    baseURL: url,
    headers: {
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarynl6gT1BKdPWIejNq'
    },
})


function login(data) {
    return request.post('/user/login', data)
}
function register(data) {
    return request.post('/user/register', data)
}
function sendVerifyCode(data) {
    return request.post('user/send_verification_code/' + data)
}


// 创建新会话：/conversation/new-conversation
// user_id: str
// conv_name: str | None = "未命名会话"
///200 data={"conv_id": conv_id}
//要加return 不然没有返回值
function createConversion(data) {
    // 返回一个Promise  
    return new Promise((resolve, reject) => {
        request.post('conversation/new-conversation/', data)
            .then(res => {
                console.log("成功url");
                console.log(res.data);
                resolve(res.data); // 使用resolve返回数据  
            })
            .catch(e => {
                console.log(e);
                reject(e); // 使用reject抛出错误  
            });
    });
}

//请求ai回答：
// class MixChat(BaseModel):
//     conv_id: str
//     query: str
//     knowledge_base_id: str | None = "-1"
//     prompt_name: str | None = "default"
// data={
//     "answer": response["data"]["text"],
//     "docs": kb_response["data"]["docs"]
// }
async function mixChat(data) {
    try {
        const res = await request.post('conversation/mix-chat/', data)
        return res.data
    } catch (e) {
        console.log(e)
    }
}

//延时，应该用不到了
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

//获取一个用户的所有对话列表
async function getUserAllConversation(data) {
    try {
        const res = await requestGet.get('/conversation/get-user-conversation/', { params: data })
        return res.data
    } catch (e) {
        console.log(e)
    }
}

//获取一个用户的一个历史对话记录
async function getConversationRecord(data) {
    try {
        const res = await requestGet.get('/conversation/get-conversation-record/', { params: data })
        return res.data
    } catch (e) {
        console.log(e)
    }
}

//用户创建知识库
async function createKnowledgeBase(data) {
    try {
        const res = await request.post('knowledge_base/create-knowledge-base/', data)
        return res.data
    } catch (e) {
        console.log(e)
    }
}

//得到用户知识库列表
async function getUserKnowledgeBaseList(data) {
    try {
        const res = await requestGet.get('/knowledge_base/get-knowledge-base/', { params: data })
        return res.data
    } catch (e) {
        console.log(e)
    }
}

//用户上传知识库文件
async function uploadKnowledgeDoc(data) {
    try {
        const res = await requestFile.post('knowledge_base/upload-knowledge-files/', data)
        return res.data
    } catch (e) {
        console.log(e)
    }
}


//获取知识库文件
async function getKnowledgeBaseDoc(data) {
    try {
        const res = await requestGet.get('/knowledge_base/get-kb-files/', { params: data })
        return res.data
    } catch (e) {
        console.log(e)
    }
}

function update_info(data) {
    return request.post('user/update_info/', data)
}

//用户删除对话 conv_id
async function deleteConversation(data) {
    try {
        const res = await requestGet.get('/conversation/delete-conversation/', { params: data })
        return res.data
    } catch (e) {
        console.log(e)
    }
}

export {
    login,
    sendVerifyCode,
    register,
    createConversion,
    mixChat,
    delay,
    getUserAllConversation,
    getConversationRecord,
    createKnowledgeBase,
    getUserKnowledgeBaseList,
    uploadKnowledgeDoc,
    getKnowledgeBaseDoc,
    update_info,
    deleteConversation
}

