<template>
    <div style="width: 100%;">
        <el-row>
            <el-col :span="2">
                <el-button type="primary" @click="submit">提交</el-button>
            </el-col>
            <el-col :span="2" :offset="2">
                <el-button type="danger" @click="cancel">取消</el-button>
            </el-col>
        </el-row>
        <el-row style="margin-top: 30px">
            <el-form-item label="标题" prop="title">
                <el-input v-model="title"></el-input>
            </el-form-item>
        </el-row>
        <div id="vidtor" style="margin-top: 20px;"></div>
    </div>
</template>

<script>
import { add_blog } from '@/service/blog_service'
import Vditor from 'vditor';
import store from '@/store';
import { ElMessage } from 'element-plus';
export default {
    name: 'blogEditor',
    data() {
        return {
            vidtor: Vditor,
            title: '',
            id: '',
            content: '',
        }
    },
    mounted() {
        this.vidtor = new Vditor('vidtor', {
            after: () => {
                this.vidtor.setValue(this.content)
            }
        })

    },
    created() {
        this.id = this.$route.query.blog_id || ''
        this.content = this.$route.query.content || ''
        this.title = this.$route.query.title || ''
        // console.log('blog_editor:created:', this.id, '\n', this.content)//ok
    },
    methods: {
        submit() {
            if (!this.title) {
                ElMessage({
                    message: '请填写标题',
                    type: 'error'
                })

            } else {
                let data = {
                    blog_id: this.id,
                    content: this.vidtor.getValue(),
                    title: this.title,
                    user_id: localStorage.getItem('user_id'),
                }
                // console.log('blog_editor:submit:', data);

                add_blog(data).then(res => {
                    // console.log('blog_editor:addblog:', res);

                    if (res.data.code == 200) {
                        let msg = this.id == '' ? '添加成功' : '修改成功'
                        ElMessage({
                            message: msg,
                            type: 'success'
                        })
                    }

                })
                this.$router.push('/blog')
            }

        },
        cancel() {
            this.$router.push('/blog')
        }
    }
}
</script>