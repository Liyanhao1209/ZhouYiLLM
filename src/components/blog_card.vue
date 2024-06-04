<template>
    <el-card shadow="hover" body-class="card-body" class="blog-card">
        <div>
            <h3>
                <el-link :href=url>
                    {{ blog_title }}
                </el-link>
            </h3>
        </div>
        <div>
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
            return '/forum_blog?blog_id=' + this.blog_id
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
}
</style>