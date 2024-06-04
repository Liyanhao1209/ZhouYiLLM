import axios from 'axios'

const request = axios.create({
    baseURL: 'http://127.0.0.1:9090/',
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


export {
    add_blog,
    get_blog_list,
    delete_blog,
    get_comment_list
}