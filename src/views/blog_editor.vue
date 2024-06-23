<template>
    <el-container >
        <div id="container">
            <el-row style="margin-top: 30px">
                <el-form-item label="标题" prop="title">
                    <el-input v-model="title"></el-input>
                </el-form-item>
            </el-row>
            <div id="vditor" class="vditor"></div>
            <el-row>
                <el-form-item label="是否上传到知识库:">
                    <el-radio-group class="radio-group" v-model="save_to_kb">
                        <el-radio :value=true>是</el-radio>
                        <el-radio :value=false>否</el-radio>
                    </el-radio-group>
                </el-form-item>
            </el-row>
            <el-row class="footer_button">
                <el-col :span="2">
                    <el-button type="primary" @click="submit">提交</el-button>
                </el-col>
                <el-col :span="1" :offset="1">
                    <el-button type="danger" @click="cancel">取消</el-button>
                </el-col>
            </el-row>
        </div>
    </el-container>
</template>

<script>
import { add_blog } from '@/service/blog_service'
import Vditor from 'vditor';
import store from '@/store';
import { ElMessage, ElLoading } from 'element-plus';

export default {
    name: 'blogEditor',
    data() {
        return {
            vidtor: Vditor,
            title: '',
            id: '',
            content: '',
            save_to_kb: false,
            // upload_loading: false
        }
    },
    mounted() {
        this.vidtor = new Vditor('vditor', {
            "height": 500,
            "width": 1200,
            "mode": "wysiwyg",
            "cache": {
                "enable": false
            },
            "preview": {
                "markdown": {
                    "autoSpace": true
                }
            },
            "outline": {
                "enable": true
            },
            "counter": {
                "enable": true
            },
            "mode": "ir",
            "preview": {
                "mode": "both"
            },
            "value": this.content
        })

    },
    created() {
        this.id = this.$route.query.blog_id || ''
        this.content = this.$route.query.content || ''
        this.title = this.$route.query.title || ''
        // console.log('blog_editor:created:', this.id, '\n', this.content)//ok
    },
    methods: {
        async submit() {
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
                    save_to_kb: this.save_to_kb
                }
                // this.upload_loading = true
                let loading_ins = ElLoading.service({
                    target: document.getElementById('vditor'),
                    text: '文件上传中……',
                })
                // console.log('blog_editor:submit:', data);
                // 编辑和添加公用
                await add_blog(data)
                    .then(res => {
                        // console.log('blog_editor:addblog:', res);
                        if (res.data.code == 200) {
                            let msg = this.id == '' ? '添加成功' : '修改成功'
                            ElMessage({
                                message: msg,
                                type: 'success'
                            })
                        }
                        loading_ins.close()
                        // this.upload_loading = false
                        this.$router.back()
                    })
            }

        },
        cancel() {
            this.$router.back()
        }
    }
}
</script>

<style>
.vditor {
    text-align: start;
    margin: auto
}

/* .footer_button {} */
</style>