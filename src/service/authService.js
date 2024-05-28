import axios from 'axios'

const request = axios.create({
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

export{
    login,
    sendVerifyCode,
    register
}

