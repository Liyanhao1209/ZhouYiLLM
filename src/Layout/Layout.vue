<template>
  <div>
    <!--    头部-->
    <!-- <Header/> -->

    <!--    主体-->
    <div style="display: flex">

      <!--      侧边栏-->
      <Aside></Aside>

      <!--      内容区域:-->
      <router-view s/>
    </div>
  </div>
</template>

<script>
// import Header from "@/components/Header";
import Aside from "@/components/aside";
export default {
  // name: "Layout.vue",
  components:{
    // Header,
    Aside
  }
}
</script>

<style scoped>
.rightDiv
{
    float: left;
    margin-left: 400px; /* Or whatever */
    width: 400px;
}
.leftDiv
{
    float: right;
    margin-right: 400px;
    width: 400px;
}
</style>
