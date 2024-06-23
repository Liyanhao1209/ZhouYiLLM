import axios from 'axios'
import { request } from './authService'
import { fileURL } from '../../config/config'

const fileRequest = axios.create({
    baseURL: fileURL,
    responseType: 'arraybuffer',
    headers: {
    }
})

function delete_kb_file(data){
    return request.post('/knowledge_base/delete-knowledge-files', data)
}

function download_file(data){
    return fileRequest.post('', data)
}


export{
    delete_kb_file,
    download_file,
}