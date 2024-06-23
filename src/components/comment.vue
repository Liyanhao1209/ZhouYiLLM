<template>
    <el-card shadow="never">
        <template #header>
            <h3 style="text-align: left">评论区</h3>
        </template>
        <template v-for="(item, index) in comment_list">
            <div class="container">
                <el-card shadow="never" class="comment-card">
                    <template #header>
                        <div class="card-header">
                            <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
                            <h4 class="author">{{ item.user_name }}</h4>
                            <div style="text-align: end; width: 100%;" class="header_item">
                                评论时间：{{ item.create_time }}
                            </div>
                        </div>
                    </template>
                    <div class="card-body">
                        {{ item.content }}
                    </div>
                </el-card>
                <div style="width: 15%;">
                    <el-button type="danger" @click="delete_comment_(item.id)" v-if="item.user_id == user_id">删除</el-button>
                </div>
            </div>
        </template>
        <el-empty v-if="this.comment_list.length == 0" description="还没有评论……"></el-empty>
    </el-card>
</template>

<script>
import { ElMessage, ElMessageBox } from 'element-plus';
import { delete_comment } from '@/service/forum_service';
export default {
    name: 'comment',
    props: {
        //存放评论列表
        comment_list: [],
        blog_id: ''
    },
    computed: {
        user_id(){
            return localStorage.getItem('user_id')
        }
    },
    methods: {
        delete_comment_(id) {
            console.log(id);
            ElMessageBox.confirm(
                '确定要删除吗？',
                '消息',
                {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                }
            ).then(() => {
                let user_id = localStorage.getItem('user_id')
                delete_comment(id, user_id, this.blog_id).then(res => {
                    if (res.data.code == 200) {
                        ElMessage({
                            type: 'success',
                            message: '删除成功'
                        })
                        this.$emit('refresh_comment_list')
                    } else {
                        ElMessage({
                            type: 'error',
                            message: res.data.msg
                        })
                    }
                })
            })
        },
    }
}

</script>

<style>
.author {
    margin-left: 20px;
    width: fit-content;
    white-space: nowrap;
}

.card-header {
    text-align: start;
    display: flex;
    height: 30px;
}

.header_item {
    margin-left: 20px;
    font-style: italic;
    font-size: small
}

.comment-card {
    width: 85%;
    margin: auto;
}

.container {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-top: 20px
}

.card-body {
    text-align: left;
    font-size: 12px;
}
</style>