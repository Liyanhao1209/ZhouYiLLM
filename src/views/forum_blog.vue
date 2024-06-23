<template>

    <div style="width: 100%;">
        <el-header>
            <div class="top-button">
                <el-button type="info" @click="this.$router.back()">
                    返回
                </el-button>
            </div>
            <div style="width: 100%;">
                <h1 style="margin: auto">{{ blog.title }}</h1>
            </div>
            <div style="width: 100%;">
                <h3>作者：{{ author }}</h3>
            </div>
        </el-header>

        <el-main>
            <div v-html="html" class="md-div"></div>
            <el-divider />
            <Comment :comment_list="comment_list" :blog_id="blog.id" @refresh_comment_list="get_comment_" />
            <div class="input">
                <el-input v-model="comment" type="textarea" class="comment-input" placeholder="在这输入评论"></el-input>
                <div>
                    <el-button @click="add_comment_" type="success">评论</el-button>
                </div>
            </div>
        </el-main>
        <el-affix position="bottom" :offset="100" class="affix">
            <el-button type="primary" size="large" circle icon="Top" @click="back_to_top"></el-button>
        </el-affix>
    </div>


</template>


<script>
import MarkdownIt from 'markdown-it';
import { get_blog, get_comment_list } from '@/service/blog_service';
import { add_comment } from '@/service/forum_service';
import Comment from '@/components/comment.vue';
import { ElMessage } from 'element-plus';
import { Top } from '@element-plus/icons-vue';
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
            author: '',
            comment_list: [],
            blog: {}
        }
    },
    components: {
        Comment,
        Top
    },
    mounted() {

    },

    created() {
        this.blog_id = this.$route.query.blog_id
        this.author = this.$route.query.author
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
                if (res.data.code == 200) {
                    ElMessage({
                        type: 'success',
                        message: '评论成功'
                    })
                    this.comment = ''
                    this.get_comment_()
                }
            })
        },

        back_to_top(){
            document.documentElement.scrollTop = 0
        }
    }
}
</script>


<style>
.affix{
    position: absolute;
    right: 20px
}

.top-button {
    display: flex;
    width: 100%;
    justify-content: flex-start;
}

.blog-input {
    margin: 10px;
    width: 48%;
    display: flex;
    height: 800px
}

.comment-input {
    width: 90%;
}

.input {
    margin-top: 30px;
    display: flex;
    align-items: center;
    justify-content: space-around;
}

.md-div {
    margin: auto;
    margin-top: 50px;
    width: 80%;
    text-align: start;
}
</style>