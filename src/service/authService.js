import axios from 'axios'

const request = axios.create({
    baseURL: 'http://127.0.0.1:9090/',
    timeout: 20000,
    headers: {
        'content-type': 'application/json'
    },
})

const requestGet = axios.create({
    baseURL: 'http://127.0.0.1:9090/',
    timeout: 20000,
    headers: {
    },
})



function login(data){
    request.post('/user/login', data).then(res=>{
        return res
    }).catch(e =>{
        console.log(e);
    })
}

function register(data){
    request.post('/user/register', data).then(res=>{
        return res
    }).catch(e =>{
        console.log(e);
    })
}

function sendVerifyCode(data){
    request.post('user/send_verification_code/'+data).then(res=>{
        return res;
    }).catch(e =>{
        console.log(e);
    })
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
function mixChat(data){
    return request.post('conversation/mix-chat/',data).then(res=>{
        return res.data;
    }).catch(e =>{
        console.log(e);
    })
}

//延时，应该用不到了
function delay(ms) {  
    return new Promise(resolve => setTimeout(resolve, ms));  
}  
  
//获取一个用户的所有对话列表
function getUserAllConversation(data){
    return requestGet.get('/conversation/get-user-conversation/',{params:data}).then(res=>{
        return res.data;
    }).catch(e =>{
        console.log(e);
    })
}

//获取一个用户的一个历史对话记录
function getConversationRecord(data){
    return requestGet.get('/conversation/get-conversation-record/',{params:data}).then(res=>{
        return res.data;
    }).catch(e =>{
        console.log(e);
    })
}

export{
    login,
    sendVerifyCode,
    register,
    createConversion,
    mixChat,
    delay,
    getUserAllConversation,
    getConversationRecord
}

