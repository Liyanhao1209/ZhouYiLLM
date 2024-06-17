<template>
    <div style="width: 100%;">
        <el-container>
            <el-header>
                <el-row :gutter="4">
                    <el-col :span="2" :offset="21" style="margin-top: 10px;">
                        <el-button type="success" @click="new_blog">写博客</el-button>
                    </el-col>
                </el-row>
            </el-header>
            <el-container>
                <el-aside width="300px">
                    <el-menu mode="vertical" default-active="active_item_index">
                        <el-menu-item v-for="(val, key, index) in bloglist" @click="click_blog" :index="val.id">
                            <div style="width: 100%;" class="menu-div">
                                <span>{{ val.title }}</span>
                                <span>
                                    <el-button class="menu-button" type="primary" icon="Edit" circle text
                                        @click="edit_blog()" style="">
                                    </el-button>
                                    <el-button class="menu-button" type="danger" icon="Delete" circle text
                                        @click="delete_blog()" style="">
                                    </el-button>
                                </span>

                            </div>
                        </el-menu-item>

                    </el-menu>

                </el-aside>
                <el-main>
                    <h1>{{ edit_blog.title }}</h1>
                    <div v-html="html"></div>
                    <el-divider v-if="this.blog_id" />
                    <Comment v-if="this.blog_id" :comment_list="comment_list" @refresh_comment_list="get_comment_" />
                </el-main>
            </el-container>

        </el-container>

    </div>

</template>


<script>
import store from '../store'
import MarkdownIt from 'markdown-it';
import { get_blog_list, delete_blog, get_comment_list } from '@/service/blog_service';
import { ElMessageBox, ElMessage } from 'element-plus';
import Comment from '@/components/comment.vue';
import {
    Check,
    Delete,
    Edit,
    Message,
    Search,
    Star,
} from '@element-plus/icons-vue'
export default {
    name: 'blog',
    data() {
        return {
            vditor: '',
            html: '',
            // 保存当前blogid
            blog_id: '',
            bloglist: [],
            comment_list: [],
            md_config: {
                html: true,
                breaks: true,
                typographer: true,
            }
        }
    },
    components: {
        Comment,
        Check,
        Delete,
        Edit,
        Message,
        Search,
        Star,
    },
    mounted() {
        this.init_bloglist();

    },

    created() {
        this.init_bloglist();
        this.blog_id = this.$route.query.blog_id

    },
    methods: {
        //获取博客评论
        get_comment_() {
            get_comment_list(this.blog_id).then(res => {
                this.comment_list = res.data.data.comment_list
                console.log(this.comment_list);
            })
        },

        //获取博客列表
        init_bloglist() {
            //传入user_id
            let user_id = localStorage.getItem('user_id')
            get_blog_list(user_id).then(res => {
                this.bloglist = res.data.data.blog_list
            })
        },

        //添加博客
        new_blog() {
            this.$router.push('/blog_editor')
            let user_id = localStorage.getItem('user_id')
        },

        //删除博客
        delete_blog() {
            if (this.blog_id != '') {
                ElMessageBox.confirm(
                    '确定删除该博客吗',
                    'Warning',
                    {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning',
                    }
                ).then(() => {
                    delete_blog(this.blog_id).then(() => {
                        ElMessage({
                            type: 'success',
                            message: '删除成功',
                        })
                        this.init_bloglist()
                        this.blog_id = ''
                    })
                })
            }
        },
        // 选择博客
        click_blog(e) {
            // console.log('blog:click_blog:', e)
            let index = this.bloglist.findIndex(item => item.id === e.index)
            this.render_md(this.bloglist[index].content)
            this.blog_id = e.index
            this.get_comment_()
        },
        // 渲染md
        render_md(src) {
            const md = new MarkdownIt(this.md_config);
            this.html = md.render(src)
        },
        // 编辑博客
        edit_blog() {
            if (this.blog_id != '') {
                let blog = this.bloglist[this.bloglist.findIndex(item => item.id === this.blog_id)]
                this.$router.push({
                    path: '/blog_editor',
                    query: {
                        blog_id: this.blog_id,
                        content: blog.content,
                        title: blog.title
                    }
                })
            }
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

.menu-div {
    display: flex;
    /* 启用Flexbox布局 */
    justify-content: space-around;
    /* 按钮将右对齐 */
    align-items: center;
    /* 垂直居中对齐 */
}

.menu-button {
    position: relative;
    top: -10px;


}
</style>