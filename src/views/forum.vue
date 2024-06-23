<template>

    <div style="margin-top: 50px; width: 100%; text-align: center" class="main-div">
        <h1>论坛</h1>
        <template v-for="(item, key) in blog_list">
            <BlogCard :blog_title="item.title" :blog_author="item.user_name" :blog_content="item.content"
                :blog_id="item.id" :is_starred="item.is_starred" />
        </template>
        <el-empty v-if="this.blog_list.length == 0" description="空空如也"></el-empty>

    </div>
</template>

<script>
import { get_blogs } from '@/service/forum_service'
import BlogCard from '@/components/blog_card.vue'
export default {
    name: 'forum',
    data() {
        return {
            //所有博客列表
            blog_list: []
        }
    },
    components: {
        BlogCard
    },
    created() {
        this._get_blogs()
    },
    mounted() {

    },
    methods: {
        _get_blogs() {
            get_blogs().then(res => {
                this.blog_list = res.data.data
            })
        }
    }
}
</script>


<style>
.main-div {
    border-radius: 15px;
}
</style>