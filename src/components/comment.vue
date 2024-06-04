<template>
    <el-card shadow="hover">
        <template #header>
            <h2 style="text-align: left">评论区</h2>
        </template>
        <template v-for="(item, index) in comment_list">
            <el-card shadow="never" class="comment-card">
                <template #header>
                    <div style="text-align: start; display: flex">
                        <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
                        <h3 class="header_item" style="width: 100px">{{ item.user_name }}</h3>
                        <div style="text-align: end; width: 100%;" class="header_item">
                            {{ item.create_time }}
                        </div>
                    </div>
                </template>
                {{ item.content }}
            </el-card>
            <div style="width: 100%; text-align: end; margin-top: 5px">
                <el-button @click="delete_comment_(item.id)">删除评论</el-button>
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
.header_item {
    margin-left: 20px
}

.comment-card {
    margin-top: 30px;
}
</style>