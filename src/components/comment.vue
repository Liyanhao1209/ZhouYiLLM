<template>
    <el-card shadow="hover">
        <template #header>
            <h2 style="text-align: left">评论</h2>
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
    </el-card>
</template>

<script>
import { UserFilled } from '@element-plus/icons-vue'
import { formatDateTime } from '@/utils/utils';
import { ElMessage } from 'element-plus';
export default {
    name: 'comment',
    props: {
        //存放评论列表
        comment_list: [],
    },
    computed: {

    },
    methods: {
        delete_comment_(id) {
            console.log('删除评论', id);
            ElMessage({
                type: 'success',
                message: '功能没实现'
            })
            ElMessage({
                type: 'error',
                message: '没权限'
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