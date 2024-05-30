import axios from 'axios'

const request = axios.create({
    baseURL: 'http://127.0.0.1:9090/',
    timeout: 20000,
    headers: {
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

export {
    login,
    sendVerifyCode,
    register
}

