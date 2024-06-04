import { request } from './blog_service'

//获取所有博客
function get_blogs() {
    return request.get('forum/get_all_blogs')
}

function add_comment(data) {
    return request.post('forum/add_comment', data)
}

function delete_comment(comment_id, user_id, blog_id) {
    return request.post('forum/delete_comment/' + comment_id + '/' + blog_id + '/' + user_id)
}

export {
    get_blogs,
    add_comment,
    delete_comment
}