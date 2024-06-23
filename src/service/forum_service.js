import { request } from './authService'

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

function get_starred_blogs(user_id) {
    return request.get('forum/get_star_blog/' + user_id)
}

function star_unstar_blog(user_id, blog_id) {
    return request.post('forum/star_unstar_blog/' + user_id + '/' + blog_id)
}

export {
    get_blogs,
    add_comment,
    delete_comment,
    get_starred_blogs,
    star_unstar_blog
}