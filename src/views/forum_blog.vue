<template>
    <div style="width: 100%;">
        <el-container>
            <el-header>
                <div style="text-align: start; display: flex">
                    <el-button type="info" @click="this.$router.back()">
                        返回
                    </el-button>
                    <h1 style="margin-left: 100px;">{{ blog.title }}</h1>
                </div>
            </el-header>
            <el-container>
                <el-main>
                    <div v-html="html"></div>
                    <el-divider />
                    <Comment :comment_list="comment_list" :blog_id="blog.id" @refresh_comment_list="get_comment_"/>
                    <el-input v-model="comment" type="textarea" style="margin-top: 50px;" placeholder="输入内容"></el-input>
                    <div style="width: 100%; text-align: end; margin-top: 20px">
                        <el-button @click="add_comment_" type="success">评论</el-button>
                    </div>
                </el-main>
            </el-container>

        </el-container>

    </div>

</template>


<script>
import MarkdownIt from 'markdown-it';
import { get_blog, get_comment_list } from '@/service/blog_service';
import { add_comment } from '@/service/forum_service';
import Comment from '@/components/comment.vue';
import { ElMessage } from 'element-plus';
export default {
    name: 'blog',
    data() {
        return {
            comment: '',
            title: '',
            vditor: '',
            html: '',
            // 保存当前blogid
            blog_id: '',
            comment_list: [],
            blog: {}
        }
    },
    components: {
        Comment
    },
    mounted() {

    },

    created() {
        ;
        this.blog_id = this.$route.query.blog_id
        this.get_blog_()
        this.get_comment_()
    },
    methods: {
        //获取博客评论
        get_comment_() {
            get_comment_list(this.blog_id).then(res => {
                this.comment_list = res.data.data.comment_list
            })
        },

        // 渲染md
        render_md(src) {
            const md = new MarkdownIt(this.md_config);
            this.html = md.render(src)
        },
        //获取blog
        get_blog_() {
            get_blog(this.blog_id).then(res => {
                this.blog = res.data.data
                this.render_md(this.blog.content)
            })
        },

        //添加评论
        add_comment_() {
            let comment_model = {
                comment: this.comment,
                user_id: localStorage.getItem('user_id'),
                blog_id: this.blog_id,
            }
            add_comment(comment_model).then(res => {
                if(res.data.code == 200){
                    ElMessage({
                        type: 'success',
                        message: '评论成功'
                    })
                    this.comment = ''
                    this.get_comment_()
                }
            })
        }
    }
}
</script>


<style>
.blog-input {
    margin: 10px;
    width: 48%;
    display: flex;
    height: 800px
}
</style>