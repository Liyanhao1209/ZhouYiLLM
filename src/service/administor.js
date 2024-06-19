import { request, authRequest } from './authService'

function login2(data) {
    return authRequest.post('/admin/login', data)
}
function getuser(){
    return request.get('/admin/get_user')
}
function block_user(data){
    return request.post('/admin/block-user',data)
}
function relive_user(data){
    return request.post('/admin/relive-user',data)
}

export{
    login2,
    getuser,
    block_user,
    relive_user
}