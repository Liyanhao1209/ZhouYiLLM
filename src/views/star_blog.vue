<template>
    <div style="margin-top: 50px; width: 100%; text-align: center" class="main-div">
        <h1>我的收藏</h1>
        <template v-for="(item, key) in blog_list">
            <BlogCard :blog_title="item.title" :blog_author="item.user_name" :blog_content="item.content" :blog_id="item.id" :is_starred="item.is_starred"
             />
        </template>
        <el-empty v-if="this.blog_list.length == 0" description="没有收藏的博客"></el-empty>
    </div>
</template>

<script>
import BlogCard from '@/components/blog_card.vue'
import { get_starred_blogs } from '@/service/forum_service';
export default {
    name: 'star_blog',
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
        this._get_starred_blogs()
    },
    mounted() {
    },
    methods: {
        _get_starred_blogs(){
            let user_id = localStorage.getItem('user_id')
            get_starred_blogs(user_id).then(res => {
                this.blog_list = res.data.data.star_blog_list
            })
        }
    }
}
</script>


<style>
.main-div{
    border-radius: 15px;
}

</style>