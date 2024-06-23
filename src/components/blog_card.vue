<template>
    <el-card shadow="hover" body-class="card-body" class="blog-card" style="">
        <div class="header">
            <h3>
                <el-link :href=url style="font-size: 25px; font-weight: bold;">
                    {{ blog_title }}
                </el-link>
            </h3>
        </div>
        <div class="body">
            <el-text line-clamp="2" truncated>
                {{ blog_content }}
            </el-text>
        </div>
        <div style="text-align: end">作者：{{ blog_author }}</div>
    </el-card>
</template>

<script>
export default {
    name: 'forum',
    props: {
        blog_id: String,
        blog_title: String,
        blog_author: String,
        blog_content: String,
    },
    computed: {
        url() {
            return '/forum_blog?blog_id=' + this.blog_id + '&author=' + this.blog_author
        }
    }
}

</script>

<style>
.card-body {
    height: 100px;
}

.blog-card {
    margin-top: 40px;
    width: 70%;
    margin-left: 15%;
    opacity: 0.9;
}

.header{
    text-align: center
}

.body{
    text-align: start
}
</style>