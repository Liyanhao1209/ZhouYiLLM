import axios from 'axios'

// const url = 'http://zyllmbackend.ihk.fghk.top'
const url = 'http://localhost:9090/'

export const request = axios.create({
    baseURL: url,
    timeout: 200000,
    headers: {
        'content-type': 'application/json'
    },
})


function add_blog(data) {
    return request.post('blog/add_blog', data)
}


function get_blog_list(user_id) {
    return request.get('blog/get_blog_list/' + user_id)
}

function delete_blog(blog_id) {
    return request.get('blog/delete/' + blog_id)
}

function get_comment_list(blog_id) {
    return request.get('forum/get_comment/' + blog_id)
}

function get_blog(blog_id) {
    return request.get('blog/' + blog_id)
}


export {
    add_blog,
    get_blog_list,
    delete_blog,
    get_comment_list,
    get_blog
}